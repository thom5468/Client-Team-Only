'''
Created on Nov 28, 2013

@author: Sean
'''

import os
import sys
import math
import pygame
import environments
import buttons

pygame.init()


def main(setupinfo=None):
    screensize = (1024, 720)
    screen = pygame.display.set_mode(screensize)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)
    animate = True
    running = True

    background, background_rect = load_image("stars.jpg")
    screen.blit(background, background_rect)
    mouse_ptr = MouseCursor("pointer2.png")
    mouse_sel = MouseCursor("selected2.png")
    mouse = pygame.sprite.RenderUpdates((mouse_ptr))
    mouse.draw(screen)
    pygame.display.flip()
    #===========================================================================
    # Object Initialization:
    #===========================================================================
    star_system = System(screen, background, animate)
    selected_unit = None

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if not mouse_ptr.down:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                    print "SPACE BAR"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_ptr.pressed = mouse_sel.pressed = True
                        mouse_ptr.released = mouse_sel.released = False
                        selected_unit = left_mouse_select_check(mouse_ptr, star_system)
                        # while the mouse button is down, change its cursor
                        mouse.remove(mouse_ptr)
                        mouse.add(mouse_sel)
                    elif event.button == 3:
                        key_mod = pygame.key.get_mods()
                        if key_mod == 4097 or key_mod == 1:

                            print "SHIFT RIGHT CLICK"
                        else:

                            print "RIGHT CLICK"

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_ptr.released = mouse_sel.released = True
                selected_unit = left_mouse_unselect_check(mouse, selected_unit, star_system)
                # while the mouse button is up, change its cursor
                mouse.remove(mouse_sel)
                mouse.add(mouse_ptr)

        screen.blit(background, background_rect)
        star_system.update()
        if selected_unit:
            selected_unit.update(True)
        mouse.update()
        star_system.draw()
        mouse.draw(screen)
        pygame.display.flip()


def left_mouse_select_check(mouse, star_system):
    for unit in star_system.unit_list:
        if unit.rect.collidepoint(mouse.pos) and unit.visible == 1:
            return unit
    for planet in star_system.planet_list:
        if planet.rect.collidepoint(mouse.pos):
            star_system.planets_move(planet)
            return None


def left_mouse_unselect_check(mouse, selected_unit, star_system):
    if selected_unit:
        for planet in star_system.planet_list:
            if planet.collide_rect.colliderect(selected_unit.rect):
                #response = client.root.move(stack_id=selected_unit.id, game_name=gamename, location_id=(star_system.id * 10 + planet.id) * 10)
                selected_unit.loc_id = (star_system.id * 10 + planet.id) * 10 ##process response
                return None
            for environ in planet.environment.environ_list:
                for point in environ.collision_points:
                    if selected_unit.rect.colliderect(pygame.Rect((point), (10, 10))):
                        #response = client.root.move(stack_id=selected_unit.id, game_name=gamename, location_id=(star_system.id * 10 + planet.id) * 10 + environ.id)
                        selected_unit.loc_id = (star_system.id * 10 + planet.id) * 10 + environ.id ##process response
                        return None
        


class System():
    def __init__(self, screen, background, animate=None):
        self.screen = screen
        self.background = background
        self.id = 1
        self.animate = animate
        self.move_dir = None
        #=======================================================================
        # Planet Population
        #=======================================================================
        purple = Planet(self, 1, "purple", "left", "purple_planet.png")
        earth = Planet(self, 2, "earth", "center", "earth_planet.png")
        blue = Planet(self, 3, "blue", "right", "blue_planet.png")
        self.planet_list = pygame.sprite.LayeredUpdates((purple, earth, blue))
        #=======================================================================
        # Unit Population
        #=======================================================================
        cis = Unit("cis", 110, 5466, "rebel_cis.jpg")
        megathron = Unit("megathron", 123, 5467, "rebel_megathron.jpg")
        vagabond = Unit("vagabond", 123, 5468, "imperial_vagabond.jpg")
        viper = Unit("viper", 130, 5469, "imperial_viper.jpg")
        self.unit_list = [cis, megathron, vagabond, viper]
        self.stack_manager = StackManager(self, self.unit_list)
        
    def update(self):
        for planet in self.planet_list:
            planet.update()
            planet.environment.update(self.unit_list)
        self.stack_manager.update_unit_location()
        for unit in self.unit_list:
            unit.update()

    def draw(self):
        self.planet_list.draw(self.screen)
        for planet in self.planet_list:
            if planet.orient is "center":
                planet.environment.draw(self.screen)
                break
        self.stack_manager.draw()

    def planets_move(self, planet):
        self.move_dir = None
        # Move planets to the right
        if planet.orient is "left":
            self.move_dir = "right"
            self.planet_list.move_to_front(planet)
            for planet in self.planet_list:
                planet.update(self.move_dir, self.animate)
        # Move planets to the left
        elif planet.orient is "right":
            self.move_dir = "left"
            self.planet_list.move_to_front(planet)
            for planet in self.planet_list:
                planet.update(self.move_dir, self.animate)
        if self.move_dir and self.animate:
            self._planets_animate()

    def _planets_animate(self):
        # These need to be set in the singleton screen class
        cur_frame = 0    # <--
        frames = 64      # <--

        if self.move_dir is "right":
            while cur_frame < frames:
                for planet in self.planet_list:
                    if planet.prev_orient is "left":
                        planet.rect.move_ip(8, 0)
                    elif planet.prev_orient is "center":
                        planet.rect.move_ip(8, 0)
                    elif planet.prev_orient is "right":
                        planet.rect.move_ip(-16, 0)
                self.screen.blit(self.background, (0, 0))
                self.planet_list.draw(self.screen)
                pygame.display.flip()
                cur_frame += 1
        elif self.move_dir is "left":
            while cur_frame < frames:
                for planet in self.planet_list:
                    if planet.prev_orient is "left":
                        planet.rect.move_ip(16, 0)
                    elif planet.prev_orient is "center":
                        planet.rect.move_ip(-8, 0)
                    elif planet.prev_orient is "right":
                        planet.rect.move_ip(-8, 0)
                self.screen.blit(self.background, (0, 0))
                self.planet_list.draw(self.screen)
                pygame.display.flip()
                cur_frame += 1
        self.update()

    def _update_unit_location(self):
        for unit in self.unit_list:
            loc_id = unit.loc_id
            unit.visible = 1
            while loc_id:
                digits = int(math.log10(loc_id)) + 1
                if digits >= 3:
                    environ_id = loc_id % 10
                elif digits >= 2:
                    planet_id = loc_id % 10
                elif digits >= 1:
                    self.system_id = loc_id % 10
                loc_id /= 10
            for planet in self.planet_list:
                if planet.id == planet_id:
                    if environ_id == 0:
                        unit.pos = None
                        unit.loc = planet.collide_rect
                    else:
                        if planet.orient is "center":
                            for point in planet.environment.environ_list[environ_id - 1].collision_points:
                                if unit.rect.colliderect(pygame.Rect((point), (2, 2))):
                                    unit.pos = point
                                    unit.loc = None
                                    unit.update()
                                    break
                                else:
                                    if len(self.unit_list.get_sprites_at(point)) == 0:
                                        unit.pos = point
                                        unit.loc = None
                                        unit.update()
                                        break
                        else:
                            unit.visible = 0
                            break


class Planet(pygame.sprite.Sprite):
    def __init__(self, parent_system, planet_id, planet_name, planet_orientation, image):
        self.parent = parent_system
        self.id = planet_id
        self.name = planet_name
        self.orient = planet_orientation
        self.prev_orient = None
        if self.orient is "left":
            self.pos = self.parent.screen.get_rect().midleft
        elif self.orient is "center":
            self.pos = self.parent.screen.get_rect().center
        elif self.orient is "right":
            self.pos = self.parent.screen.get_rect().midright
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.collide_rect = self.rect.inflate(-50, -50)
        #=======================================================================
        # Environment Population
        #=======================================================================
        self.environment = environments.EnvironBox(self, self.rect)
        self.environment.addEnviron(1, 'W', 2, "Humans", "Animals", 'C')
        self.environment.addEnviron(2, 'U', 1, "Bricktons", "Animals", 'C')
        self.environment.addEnviron(3, 'F', 3, "Corruptons", "Animals", 'A')

    def update(self, move_dir=None, animate=None):
        self.prev_orient = self.orient
        if move_dir is "right":
            if self.orient is "left":
                self.pos = self.parent.screen.get_rect().center
                self.orient = "center"
            elif self.orient is "center":
                self.pos = self.parent.screen.get_rect().midright
                self.orient = "right"
            elif self.orient is "right":
                self.pos = self.parent.screen.get_rect().midleft
                self.orient = "left"
            if not animate:
                self.rect.center = self.pos
                self.collide_rect.center = self.pos
        elif move_dir is "left":
            if self.orient is "left":
                self.pos = self.parent.screen.get_rect().midright
                self.orient = "right"
            elif self.orient is "center":
                self.pos = self.parent.screen.get_rect().midleft
                self.orient = "left"
            elif self.orient is "right":
                self.pos = self.parent.screen.get_rect().center
                self.orient = "center"
            if not animate:
                self.rect.center = self.pos
                self.collide_rect.center = self.pos
        else:
            self.rect.center = self.pos
            self.collide_rect.center = self.pos
'''
class Stack():
    def __init__(self, stack_id, stack_location_id, unit_list, unit_ids)
        self.id = stack_id
        self.loc_id = stack_location_id
        self.unit_list = unit_list
        self.unit_ids = unit_ids
        self.units = pygame.sprite.LayeredDirty(unit_list)
        self.units.empty()
        self.set_attributes()
        self.pos = None
        self.loc = None
        self.rect = None
        
    def set_attributes(self):
        self.prev_pos = self.pos
        self.pos = units.sprites[0].pos
        self.prev_loc = self.loc
        self.loc = units.sprites[0].loc
        self.prev_rect = self.rect
        self.rect = units.sprites[0].rect
    
    def update_units(self, unit_ids ):
        for unit in self.units.sprites():
            if not unit_ids.contains(unit.id):
                self.units.remove(unit)
        for id in unit_ids:
            for unit in self.unit_list.sprites:
                if unit.id == id:
                    if not self.units.has(unit)
                        self.units.add(unit)
            
    def cascadechanges(self):
        if self.prect is not self.rect:
            self.prect = self.rect
            self.rect = units[0].rect
        if self.ppos is not self.pos:
            self.ppos = self.pos
            for unit in self.units.sprites():
                unit.pos = self.pos
        if self.ploc is not self.loc:
            self.ploc = self.loc
            for unit in self.units.sprites():
                unit.loc = self.loc
            
    def update(self, unit_ids = self.unitids):
        self.updateunits(unit_ids)
        self.setattributes()
        self.cascadechanges()
        
    def draw(screen):
        self.units.draw()           
    
'''
class StackManager():
    def __init__(self, parent, stack_list):
        self.parent = parent
        self.screen = self.parent.screen
        self.stack_list =[]
        self.loc = None
        for stack_num, unit in enumerate(stack_list):
            stack_num = pygame.sprite.LayeredDirty((unit))
            self.stack_list.append(stack_num)

    def update_unit_location(self):
        for stack in self.stack_list:
            for unit in stack:
                loc_id = unit.loc_id
                unit.visible = 1
                while loc_id:
                    digits = int(math.log10(loc_id)) + 1
                    if digits >= 3:
                        environ_id = loc_id % 10
                    elif digits >= 2:
                        planet_id = loc_id % 10
                    elif digits >= 1:
                        self.parent.system_id = loc_id % 10
                    loc_id /= 10
                for planet in self.parent.planet_list:
                    if planet.id == planet_id:
                        if environ_id == 0:
                            unit.pos = None
                            unit.loc = planet.collide_rect
                        else:
                            if planet.orient is "center":
                                for point in planet.environment.environ_list[environ_id - 1].collision_points:
                                    if unit.rect.colliderect(pygame.Rect((point), (2, 2))):
                                        unit.pos = point
                                        unit.loc = None
                                        unit.update()
                                        break
                                    else:
                                        if len(stack.get_sprites_at(point)) == 0:
                                            unit.pos = point
                                            unit.loc = None
                                            unit.update()
                                            break
                            else:
                                unit.visible = 0
                                break
                stack.draw(self.screen)
                break

    def draw(self):
        for stack in self.stack_list:
            stack.draw(self.screen)
            


class Unit(pygame.sprite.DirtySprite):
    def __init__(self, unit_name, unit_location_id, unit_id, image):
        self.name = unit_name
        self.id = unit_id
        self.loc_id = unit_location_id
        self.pos = None
        self.loc = None
        pygame.sprite.DirtySprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.dirty = 2

    def update(self, selected=None, animate=None):
        if selected:
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
        else:
            try:
                if self.loc:
                    self.rect.clamp_ip(self.loc)
                else:
                    self.rect.center = self.pos
            except:
                print "ERROR:", self.name, "is drifting"
                return


class MouseCursor(pygame.sprite.Sprite):
    def __init__(self, name):
        self.screen = pygame.display.get_surface()
        self.pos = self.screen.get_rect().center
        self.pressed = False
        self.down = False
        self.released = False
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name, -1)
        self.rect.center = self.pos

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.rect.midtop = self.pos
        if self.pressed:
            self.down = True
            self.rect.move_ip(-10, -10)
        if self.released:
            self.down = False
            self.pressed = False


def load_image(image, colorkey=None):
    path = os.path.join('Data', image)
    print path
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print 'Can not load image:', image
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)  # pygame.RLEACCEL can improve performance
    return image, image.get_rect()

if __name__ == '__main__':
    main()

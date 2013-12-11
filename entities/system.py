import pygame
from math import log10
from unit import Unit
from planet import Planet

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
        #cis = Unit("cis", 110, 5466, 9, "rebel_cis.jpg")
        #megathron = Unit("megathron", 123, 5467, 9, "rebel_megathron.jpg")
        #agabond = Unit("vagabond", 123, 5468, 9, "imperial_vagabond.jpg")
        #iper = Unit("viper", 130, 5469, 9, "imperial_viper.jpg")
        self.unit_list = pygame.sprite.LayeredDirty()

    def addunit (self, unitdict):
        newunit = Unit(unitdict)
        for unit in self.unit_list:
            if newunit.stack_id == unit.stack_id:
                unit.add_unit(newunit)
                break
            else:
                self.unit_list.add(newunit)
        
    def update(self):
        for planet in self.planet_list:
            planet.update()
            planet.environment.update()
        self._update_unit_location()
        for unit in self.unit_list:
            unit.update()

    def draw(self):
        self.planet_list.draw(self.screen)
        for planet in self.planet_list:
            if planet.orient is "center":
                planet.environment.draw(self.screen)
                break
        self.unit_list.draw(self.screen)

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
                digits = int(log10(loc_id)) + 1
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
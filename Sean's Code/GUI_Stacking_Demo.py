import os
import sys
import pygame

pygame.init()

def main():
    clock = pygame.time.Clock()

    screensize = (1024, 800)
    screen = pygame.display.set_mode(screensize)
    starbg = pygame.image.load("stars.jpg")
    starbg = pygame.transform.scale(starbg, (screensize))
    pygame.mouse.set_visible(0)

    screen.blit(starbg, (0, 0))
    mouseptr = MouseCursor('pointer2.png')
    mousesel = MouseCursor('selected2.png')
    controls = pygame.sprite.RenderUpdates((mouseptr))
    controls.draw(screen)
    pygame.display.flip()

    #######################################
    # Game Control Handling:
    #######################################
    selection = pygame.sprite.LayeredUpdates(())
    unitstack = Stack()
    animate = True
    mouse_update = False
    prev_pos = -1
    
    #######################################
    # Object Initialization:
    #######################################
    purple = Planet('purple', 'purple_planet.png', 'center')
    earth = Planet('earth', 'earth_planet.png', 'left')
    blue = Planet('blue', 'blue_planet.png', 'right')
    cis = Ship('cis', 'rebel_cis.jpg', (100, 200))
    megathron = Ship('megathron', 'rebel_megathron.jpg', (100, 250))
    vagabond1 = Ship('vagabond', 'imperial_vagabond.jpg', (100, 500))
    vagabond2 = Ship('vagabond', 'imperial_vagabond.jpg', (250, 600))
    viper = Ship('viper', 'imperial_viper.jpg', (400, 500))

    planets = pygame.sprite.LayeredUpdates((earth, purple, blue))
    #imperialships = pygame.sprite.LayeredUpdates((vagabond1, vagabond2))
    rebelships = pygame.sprite.LayeredUpdates((cis, megathron, viper, vagabond1, vagabond2))
    
    #######################################
    # TEST CODE FOR STACKING
    #######################################
    print '###GROUP###:', unitstack
    
    while 1:
        clock.tick(60)
        #######################################
        # Event Handling:
        #######################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if not mouseptr.down:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    print 'SPACE DOWN'         
                    #######################################
                    # TEST CODE FOR EMPIRE SHIP PLACEMENT
                    #######################################
                    for ship in imperialships:
                        print ship.pos
                        if ship.pos[0] <= 100:
                            for planet in planets:
                                if planet.orient is "left":
                                    ship.loc = planet.colliderect
                        elif ship.pos[0] <= 200:
                            for planet in planets:
                                if planet.orient is "center":
                                    ship.loc = planet.colliderect
                        elif ship.pos[0] <= 300:
                            for planet in planets:
                                if planet.orient is "right":
                                    ship.loc = planet.colliderect
                        elif ship.pos[0] <= 400:
                            for planet in planets:
                                if planet.orient is "center":
                                    ship.loc = planet.colliderect
                    #######################################
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouseptr.pressed = mousesel.pressed = True
                        mouseptr.released = mousesel.released = False
                        # check to see if anything has been selected
                        mouse_update, prev_pos = select_check(rebelships, planets, mouseptr, selection, unitstack)
                        # while the mouse is down, change its cursor
                        controls.remove(mouseptr)
                        controls.add(mousesel)
                    else:
                        mod = pygame.key.get_mods()
                        if mod == 4097:
                            print 'SHIFT RIGHT CLICK'
                            left_select_check(rebelships, mouseptr, selection, unitstack, True)
                        else:
                            left_select_check(rebelships, mouseptr, selection, unitstack, False)
                            for val in unitstack.list:
                                print val
                    
            if event.type == pygame.MOUSEBUTTONUP:
                mouseptr.released = mousesel.released = True
                # check to see if something was selected
                if mouse_update and prev_pos == -1: # planet was selected
                    planet_move(planets, selection, animate, screen, starbg)
                elif mouse_update: # a mobile unit was selected
                    unit_unselect_check(rebelships, planets, mousesel, prev_pos, selection, unitstack)  
                mouse_update = False
                prev_pos = -1
                         
                controls.remove(mousesel)
                controls.add(mouseptr)
        
        controls.update()

        planets.update(None, animate)
        #imperialships.update(None, animate)
        rebelships.update(None, animate)
        selection.update(mouse_update, animate)
        
        #unitstack.update(mouseptr, mouse_update, animate)
        
        screen.blit(starbg, (0, 0))

        planets.draw(screen)
        #imperialships.draw(screen)
        rebelships.draw(screen)
        #unitstack.draw(screen)
        if unitstack.refresh:
            for stack in unitstack.list:
                stack.draw(screen)
        selection.draw(screen)
        controls.draw(screen)

        pygame.display.flip()

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

class Planet(pygame.sprite.DirtySprite):
    def __init__(self, name, image, orientation):
        self.name = name
        self.orient = orientation
        self.poreint = orientation
        self.screen = pygame.display.get_surface()
        if self.orient is 'left':
            self.pos = self.screen.get_rect().midleft
        elif self.orient is 'center':
            self.pos = self.screen.get_rect().center
        elif self.orient is 'right':
            self.pos = self.screen.get_rect().midright
        pygame.sprite.DirtySprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.rect.center = self.pos
        self.colliderect = self.rect.inflate(-50, -50)
        self.colliderect.normalize()
    def update(self, movedir, animate):
        self.porient = self.orient
        if movedir is 'right':
            #print 'MOVING', movedir, self.name # Testing
            if self.orient is 'left':
                self.pos = self.screen.get_rect().center
                self.orient = 'center'
            elif self.orient is 'center':
                self.pos = self.screen.get_rect().midright
                self.orient = 'right'
            elif self.orient is 'right':
                self.pos = self.screen.get_rect().midleft
                self.orient = 'left'
            if not animate:
                self.rect.center = self.pos
                self.colliderect.center = self.pos
        elif movedir is 'left':
            #print 'MOVING', movedir, self.name # Testing
            if self.orient is 'left':
                self.pos = self.screen.get_rect().midright
                self.orient = 'right'
            elif self.orient is 'center':
                self.pos = self.screen.get_rect().midleft
                self.orient = 'left'
            elif self.orient is 'right':
                self.pos = self.screen.get_rect().center
                self.orient = 'center'
            if not animate:
                self.rect.center = self.pos
                self.colliderect.center = self.pos
        else: # is this okay? or should it be an elif?
        #elif movedir is 'redraw' and animate:
            self.rect.center = self.pos
            self.colliderect.center = self.pos

class Ship(pygame.sprite.DirtySprite):
    def __init__(self, name, image, position):
        self.name = name
        self.pos = position
        self.loc = None
        pygame.sprite.DirtySprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.rect.center = self.pos
    def update(self, selected, animate): # ship animation will be added later
        if selected:
            #print 'UPDATING: ', self.name # Testing
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
        else:
            try:
                self.rect.clamp_ip(self.loc)
            except:
                animate = True
                #print self.name, 'drifting'
                
class Stack():
    def __init__(self):
        self.screen = pygame.display.get_surface() # needed?
        self.list = []
        self.refresh = False
    def make(self, unit):
        print 'MAKING NEW STACK'
        sprite_group = pygame.sprite.LayeredUpdates((unit))
        self.list.append(sprite_group)
        return sprite_group
    def add(self, unit, unitstack):
        for stack in self.list:
            if stack.has(unitstack):
                stack.add(unit)
    def remove(self, unit):
        for stack in self.list:
            if stack.has(unit):
                print 'REMOVING'
                sprite = stack.get_top_sprite()
                sprite.rect.move_ip(0, -50)
                stack.remove(sprite)
                if len(stack) == 1:
                    self.list.remove(stack)
    def has(self, unit):
        for stack in self.list:
            if stack.has(unit):
                return True    
    def top(self, unit):
        for stack in self.list:
            if stack.has(unit):
                sprite = stack.get_top_sprite()
                print sprite.name
    def cycle(self, unit):
        for stack in self.list:
            if stack.has(unit):
                sprite = stack.get_top_sprite()
                stack.move_to_back(sprite)
                self.refresh = True
    def sprites(self, unit):
        for stack in self.list:
            if stack.has(unit):
                return stack.sprites()
    #def update(self, mouse, selected, animate): # This is hella broken - still thinking about how and what this should do
    def update(self, unit, location):
        for stack in self.list:
            if stack.has(unit):
                self.refresh = True
                for sprite in stack:
                    sprite.loc = location # set the location of the ship to the planet !!
                    sprite.rect.clamp_ip(location)
        #if selected and self.list:
        #    for stack in self.list:
        #        print "!!!!!", stack
        #        if pygame.sprite.spritecollide(mouse, stack, False):
        #            break
        #    stack.update(selected, animate)
                # Update on screen stack information
                #for collision in pygame.sprite.spritecollide(mouse, stack, False):
                #    print 'MOUSE OVER >>>', collision.name
                #    stack.update(selected, animate)         
    def draw(self, screen):
        if self.refresh:
            print 'REDRAWING'
            for stack in self.list:
                stack.draw(screen)
            self.refresh = False

def select_check(shiplist, planetlist, mouse, selectionlist, unitstack):
    for ship in shiplist:
        if ship.rect.collidepoint(mouse.pos):
            if unitstack.has(ship):
                selectionlist.add(unitstack.sprites(ship))
                print 'SELECTED STACK: ', selectionlist, mouse.pos # Testing
                return True, ship.rect.center
            else:
                selectionlist.add(ship)
                print 'SELECTED: ', selectionlist, mouse.pos # Testing
                shiplist.remove(ship)
                return True, ship.rect.center
    for planet in planetlist:
        #print '--->', planet.name # Testing
        if planet.rect.collidepoint(mouse.pos):
            print 'SELECTED: ', planet.name # Testing
            selectionlist.add(planet) # the planet may not even need...
            planetlist.remove(planet) # to be added to the selection list 
            return True, -1
    return False, -1

def left_select_check(shiplist, mouse, selectionlist, unitstack, breakstack):
    if breakstack:
        for ship in shiplist:
            if ship.rect.collidepoint(mouse.pos):
                if unitstack.has(ship):
                    unitstack.top(ship)
                    unitstack.remove(ship)
                    return True
    else:
        for ship in shiplist:
            if ship.rect.collidepoint(mouse.pos):
                unitstack.top(ship)
                unitstack.cycle(ship)
                return True

def unit_unselect_check(shiplist, planetlist, mouse, prev_pos, selectionlist, unitstack):  
    for unit in selectionlist:
        if unitstack.has(unit):
            print 'UNSELECTING STACK:'
            for planet in planetlist:
                if planet.rect.collidepoint(mouse.pos):
                    print 'STACK LANDING ON:', planet.name
                    print unitstack.sprites(unit)
                    unitstack.update(unit, planet.colliderect)
                    selectionlist.empty()
                    return True
    
    for unit in selectionlist:
        print 'UNSELECTING SINGLE'
        #print unit.groups()
        #print 'UNSELECTING: ', unit.name, mouse.pos # Testing
        #print '--->', unitstack.list
        if _unit_stack_check(shiplist, unit, selectionlist, unitstack):
                #print '<---', unitstack.list
                return True
        for planet in planetlist:
            if planet.rect.collidepoint(mouse.pos):
                print 'SINGLE LANDING ON:', planet.name
                unit.loc = planet.colliderect # set the location of the ship to the planet !!
                unit.rect.clamp_ip(planet.colliderect)
                shiplist.add(unit)
                selectionlist.empty()
                return True
            
        unit.pos = prev_pos
        unit.rect.center = unit.pos
        shiplist.add(unit)
        #selectionlist.remove(selected)
        selectionlist.empty()
        return False

def _unit_stack_check(shiplist, unit, selectionlist, unitstack):
    # if there are stacks present on the stack list, is the unit joining one of these existing stacks?
    for stack in unitstack.list:
        for collision in pygame.sprite.spritecollide(unit, stack, False):
            print '>>>>'
            unit.pos = collision.pos
            unit.rect.move_ip(unit.pos)
            unit.rect.clamp_ip(collision.rect)
            #stack.add(unit)
            unitstack.add(unit, stack)
            shiplist.add(unit)
            selectionlist.empty()
            unitstack.update(unit, collision.rect)
            unitstack.cycle(unit)
            return True
    # if the unit is not joining an existing stack, create a new stack and append the stack onto the stack list.
    for ship in shiplist:
        if unit.rect.colliderect(ship.rect):
            print '<<<<'
            unit.pos = ship.pos
            unit.rect.clamp_ip(ship.rect)
            #unitstack.make(unit)
            unitstack.add(ship, unitstack.make(unit))
            shiplist.add(unit)
            selectionlist.empty()
            unitstack.update(unit, ship.rect)
            unitstack.cycle(unit)
            return True
    # else no stacking
    return False
        # ???
        #shiplist.add(unit)
        #selectionlist.empty()
           
def planet_move(planetlist, selectionlist, animate, screen, background): # the screen and background need to be members of a singleton
    movedir = None
    for selectedplanet in selectionlist:
        #Move Right
        if selectedplanet.orient is 'left':
            movedir = 'right'
            selectedplanet.update(movedir, animate)
            for planet in planetlist:
                planet.update(movedir, animate)
        #Move Left
        elif selectedplanet.orient is 'right':
            movedir = 'left'
            selectedplanet.update(movedir, animate)
            for planet in planetlist:
                planet.update(movedir, animate)
    planetlist.add(selectedplanet)
    selectionlist.empty()
    
    if animate and movedir:
        _planet_animate(planetlist, movedir, screen, background)
    
def _planet_animate(planetlist, movedir, screen, background):
    # These need to be set in the screen class
    curframe = 0    # <--
    frames = 64     # <--
    width = 512     # <--
    
    # Can this be cleaned up?
    offset = -1     # <--
    offsetadj = -1  # <--
    fill = -1       # <--
    filladj = -1    # <--
    
    #Move Right
    if movedir is 'right':
        while curframe < frames:
            for planet in planetlist:
                if planet.porient is 'left':
                    planet.rect.move_ip(8, 0)
                elif planet.porient is 'center':
                    planet.rect.move_ip(8, 0)
                elif planet.porient is 'right':
                    planet.rect.move_ip(-16, 0)
            screen.blit(background, (0, 0))
            planetlist.draw(screen)
            pygame.display.flip()
            curframe += 1
    
    #Move Left
    elif movedir is 'left':
        while curframe < frames:
            for planet in planetlist:
                if planet.porient is 'left':
        
                    offset = planet.rect.midright[0] - planet.rect.center[0]
                    fill = width - 2*offset
                    
                    if planet.rect.midright[0] >= 0 and planet.rect.midleft[0] < width:
                        planet.rect.move_ip(-8, 0)
                        filladj = fill
                    elif filladj >= 0:
                        #print 'FILLADJ', filladj
                        filladj -= 8
                        planet.rect.midleft = screen.get_rect().midright
                        offsetadj = offset
                    elif offsetadj >= 0:
                        #print 'OFFSET ADJ', offsetadj
                        offsetadj -= 8
                        planet.rect.move_ip(-8, 0) 
                
                elif planet.porient is 'center':
                    planet.rect.move_ip(-8, 0)
                elif planet.porient is 'right':
                    planet.rect.move_ip(-8, 0)
            screen.blit(background, (0, 0))
            planetlist.draw(screen)
            pygame.display.flip()
            curframe += 1
        
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
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey) #pygame.RLEACCEL can improve performance
    return image, image.get_rect()

if __name__ == '__main__': main()
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
    selection = pygame.sprite.RenderUpdates(())
    animate = True
    mouse_update = False
    prev_pos = -1
    
    #######################################
    # Object Initialization:
    #######################################
    purple = Planet('purple', 'purple_planet.png', 'center')
    earth = Planet('earth', 'earth_planet.png', 'left')
    blue = Planet('blue', 'blue_planet.png', 'right')
    cis = Ship('cis', 'rebel_cis.jpg', None, (100, 200))
    megathron = Ship('megathron', 'rebel_megathron.jpg', None, (100, 250))
    vagabond1 = Ship('vagabond', 'imperial_vagabond.jpg', None, (100, 500))
    vagabond2 = Ship('vagabond', 'imperial_vagabond.jpg', None, (250, 600))
    viper = Ship('viper', 'imperial_viper.jpg', None, (400, 500))

    planets = pygame.sprite.LayeredUpdates((earth, purple, blue))
    imperialships = pygame.sprite.LayeredUpdates((vagabond1, vagabond2, viper))
    rebelships = pygame.sprite.LayeredUpdates((cis, megathron))
    
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
                                    #ship.pos = ship.loc.center
                        elif ship.pos[0] <= 200:
                            for planet in planets:
                                if planet.orient is "center":
                                    ship.loc = planet.colliderect
                                    #ship.pos = ship.loc.center
                        elif ship.pos[0] <= 300:
                            for planet in planets:
                                if planet.orient is "right":
                                    ship.loc = planet.colliderect
                                    #ship.pos = ship.loc.center
                        elif ship.pos[0] <= 400:
                            for planet in planets:
                                if planet.orient is "center":
                                    ship.loc = planet.colliderect
                                    #ship.pos = ship.loc.center
                    #######################################
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseptr.pressed = mousesel.pressed = True
                    mouseptr.released = mousesel.released = False
                    # check to see if anything has been selected
                    mouse_update, prev_pos = select_check(rebelships, planets, mouseptr, selection)
                    # while the mouse is down, change its cursor
                    controls.remove(mouseptr)
                    controls.add(mousesel)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                mouseptr.released = mousesel.released = True
                # check to see if something was selected
                if mouse_update and prev_pos == -1: # planet was selected
                    planet_move(planets, selection, animate, screen, starbg)
                elif mouse_update: # a mobile unit was selected
                    unit_unselect_check(rebelships, planets, mousesel, prev_pos, selection)  
                mouse_update = False
                prev_pos = -1
                         
                controls.remove(mousesel)
                controls.add(mouseptr)
        
        controls.update()

        planets.update(None, animate)
        imperialships.update(None, animate)
        rebelships.update(None, animate)
        selection.update(mouse_update, animate)
        
        screen.blit(starbg, (0, 0))

        planets.draw(screen)
        imperialships.draw(screen)
        rebelships.draw(screen)
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
    def __init__(self, name, image, location, position):
        self.name = name
        self.loc = location
        if self.loc:
            self.pos = self.loc
        else:
            self.pos = position
        pygame.sprite.DirtySprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.rect.center = self.pos
    def update(self, selected, animate): # ship animation will be added later
        if selected:
            #print 'UPDATING: ', self.name # Testing
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
        else:
            if self.loc:
                self.rect.clamp_ip(self.loc)

class Stack(pygame.sprite.DirtySprite):
    def __init__(self, name, location, position, stack_rectangle):
        self.name = name
        self.loc = location
        if self.loc:
            self.pos = self.loc
        else:
            self.pos = position
        self.rect = stack_rectangle
        self.rect.center = self.pos
    def update(self, selected, special, animate): # special is key to break stack
        
        if selected:
            #print 'UPDATING: ', self.name # Testing
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
        else:
            if self.loc:
                self.rect.clamp_ip(self.loc)
            
def select_check(shiplist, planetlist, mouse, selectionlist):
    for ship in shiplist:
        if ship.rect.collidepoint(mouse.pos):
            print 'SELECTED: ', ship.name, mouse.pos # Testing
            selectionlist.add(ship)
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

def unit_unselect_check(shiplist, planetlist, mouse, prev_pos, selectionlist):
    for unit in selectionlist:
        print 'UNSELECTING: ', unit.name, mouse.pos # Testing
        if _unit_stack_check(shiplist, planetlist, mouse, prev_pos, unit, selectionlist):
            return True
        for planet in planetlist:
            if planet.rect.collidepoint(mouse.pos):
                print 'LANDING ON:', planet.name
                unit.loc = planet.colliderect # set the location of the ship to the planet
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

def _unit_stack_check(shiplist, planetlist, mouse, prev_pos, unit, selectionlist):
    for ship in shiplist:
        if unit.rect.colliderect(ship.rect):
            print 'WE HAVE A STACK'
            shiplist.add(unit)
            selectionlist.empty()
            return True
    return False

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
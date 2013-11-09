#@PydevCodeAnalysisIgnore
import os
import sys
import pygame
import environs
import threading

pygame.init()

#Global notification log stack
LogStack = []
class GUI (threading.Thread):
    def __init__ (self):
        self.clock = pygame.time.Clock()
        self.screensize = (1024, 800)
        self.screen = pygame.display.set_mode(self.screensize)
        self.starbg = pygame.image.load("stars.jpg")
        self.starbg = pygame.transform.scale(self.starbg, (self.screensize))
        pygame.mouse.set_visible(0)

        self.screen.blit(self.starbg, (0, 0))
        mouseptr = MouseCursor('pointer2.png')
        mousesel = MouseCursor('selected2.png')
        self.controls = pygame.sprite.RenderUpdates((mouseptr))
        self.controls.draw(self.screen)
        pygame.display.flip()

        #===========================================================================
        # Game Control Handling:
        #===========================================================================
        self.selection = pygame.sprite.LayeredUpdates(())
        self.unitstack = Stack()
        self.animate = True
        self.mouse_update = False
        self.prev_pos = None
        self.prev_loc = None

        #===========================================================================
        # Object Initialization:
        #===========================================================================
        self.purple = Planet('purple', 'purple_planet.png', 'left')
        self.earth = Planet('earth', 'earth_planet.png', 'center')
        self.blue = Planet('blue', 'blue_planet.png', 'right')
        self.cis = Ship('cis', 'rebel_cis.jpg', (100, 200))
        self.megathron = Ship('megathron', 'rebel_megathron.jpg', (100, 250))
        self.vagabond1 = Ship('vagabond', 'imperial_vagabond.jpg', (100, 500))
        self.vagabond2 = Ship('vagabond', 'imperial_vagabond.jpg', (250, 600))
        self.viper = Ship('viper', 'imperial_viper.jpg', (400, 500))

        self.planets = pygame.sprite.LayeredUpdates((self.earth, self.purple, self.blue))
        #imperialships = pygame.sprite.LayeredUpdates((vagabond1, vagabond2))
        self.rebelships = pygame.sprite.LayeredUpdates((self.cis, self.megathron, self.viper, self.vagabond1, self.vagabond2))

        self.starsystem = System('star system', self.planets, self.starbg, self.animate)
        
        #Buttons
        self.LogFlag = False
        self.DetailsFlag = False
        self.MissionFlag = False
        self.HelpFlag = False
        self.LogButton = Button()
        self.CloseLogButton = Button()
        self.DetailsButton = Button()
        self.CloseDetailsButton = Button()
        self.MissionButton = Button()
        self.CloseMissionButton = Button()
        self.HelpButton = Button()
        self.CloseHelpButton = Button()
        #Mission Buttons
        self.MissionCoup = Button()
        self.MissionGI = Button()
        self.MissionDip = Button()
        self.MissionAssas = Button()
        self.MissionSubvert = Button()
        self.MissionScavenge = Button()
        self.MissionCamp = Button()
        self.MissionRebelion = Button()
        #Initialize the hidden buttons
        self.CloseLogButton.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.CloseDetailsButton.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.CloseMissionButton.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.CloseHelpButton.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.MissionCoup.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.MissionGI.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.MissionDip.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.MissionAssas.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.MissionSubvert.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.MissionScavenge.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.MissionCamp.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        self.MissionRebelion.create_button(self.screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            self.clock.tick(60)
            
            #=======================================================================
            # Event Handling:
            #=======================================================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if not mouseptr.down:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        print 'PRINTING UNIT STACK:'  # Testing
                        for sprite_group in self.unitstack.list:
                            print sprite_group
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouseptr.pressed = mousesel.pressed = True
                            mouseptr.released = mousesel.released = False
                            # check to see if anything has been selected
                            mouse_update, prev_pos, prev_loc = select_check(rebelships, planets, mouseptr, self.selection, self.unitstack)
                            # while the mouse button is down, change its cursor
                            self.controls.remove(mouseptr)
                            self.controls.add(mousesel)
                        elif event.button == 3:
                            key_mod = pygame.key.get_mods()
                            if key_mod == 4097 or key_mod == 1:
                                left_select_check(rebelships, mouseptr, self.selection, self.unitstack, True)
                            else:
                                left_select_check(rebelships, mouseptr, self.selection, self.unitstack, False)
                                
                        #If the self.Log button is pressed, then display the window
                        if self.LogButton.pressed(pygame.mouse.get_pos()):
                            self.LogFlag = True
                        elif self.CloseLogButton.pressed(pygame.mouse.get_pos()):
                            self.LogFlag = False
                        elif self.DetailsButton.pressed(pygame.mouse.get_pos()):
                            self.DetailsFlag = True
                        elif self.CloseDetailsButton.pressed(pygame.mouse.get_pos()):
                            self.DetailsFlag = False
                        elif self.HelpButton.pressed(pygame.mouse.get_pos()):
                            self.HelpFlag = True
                        elif self.CloseHelpButton.pressed(pygame.mouse.get_pos()):
                            self.HelpFlag = False    		
                        elif self.MissionButton.pressed(pygame.mouse.get_pos()):
                            self.MissionFlag = True
                        elif self.CloseMissionButton.pressed(pygame.mouse.get_pos()):
                            self.MissionFlag = False   
                        elif self.MissionCoup.pressed(pygame.mouse.get_pos()):
                            #Send off request to Backend
                            self.LogStack.insert(0,"Coup Mission Selected")
                        elif self.MissionGI.pressed(pygame.mouse.get_pos()):
                            #Send off request to Backend
                            self.LogStack.insert(0,"Gather Information Mission Selected")
                        elif self.MissionDip.pressed(pygame.mouse.get_pos()):
                            #Send off request to Backend
                            self.LogStack.insert(0,"Diplomacy Mission Selected")
                        elif self.MissionAssas.pressed(pygame.mouse.get_pos()):
                            #Send off request to Backend
                            self.LogStack.insert(0,"Assasination Mission Selected")
                        elif self.MissionSubvert.pressed(pygame.mouse.get_pos()):
                            #Send off request to Backend
                            self.LogStack.insert(0,"Subvert Troops Mission Selected")
                        elif self.MissionScavenge.pressed(pygame.mouse.get_pos()):
                            #Send off request to Backend
                            self.LogStack.insert(0,"Scavenge Mission Selected")
                        elif self.MissionCamp.pressed(pygame.mouse.get_pos()):
                            #Send off request to Backend
                            self.LogStack.insert(0,"Start Rebel Camp Mission Selected")
                        elif self.MissionRebelion.pressed(pygame.mouse.get_pos()):
                            #Send off request to Backend
                            self.LogStack.insert(0,"Start/Stop Rebelion Mission Selected")
                        

                if event.type == pygame.MOUSEBUTTONUP:
                    mouseptr.released = mousesel.released = True
                    # check to see if something was selected
                    if self.mouse_update and self.prev_pos is None:  # planet was selected
                        self.starsystem.planet_move(self.selection)
                    elif self.mouse_update:  # a unit was selected
                        unit_unselect_check(self.rebelships, self.planets, mousesel, self.prev_pos, self.prev_loc, self.selection, self.unitstack)
                    self.mouse_update = False
                    # while the mouse button is up, change its cursor
                    self.controls.remove(mousesel)
                    self.controls.add(mouseptr)

            # Update where the ships are in relation to planets; update self.controls and self.selection movement
            self.planets.update()
            self.rebelships.update()
            self.controls.update()
            self.selection.update(self.mouse_update, self.animate)

            # Refresh the screen
            self.screen.blit(self.starbg, (0, 0))
            self.planets.draw(self.screen)
            for planet in self.planets.sprites():
                planet.environment.draw(self.screen)
            self.rebelships.draw(self.screen)
            for stack in self.unitstack.list:
                stack.draw(self.screen)
            #self.unitstack.draw(self.screen) # Not working as intended
            self.selection.draw(self.screen)
            
            #Draw menus and buttons based off of flag values
            if(self.LogFlag == True):
                #If self.LogFlag is set, then display the text window
                #Format the output string
                if(len(self.LogStack) > 10):
                    self.LogStack.pop()
                self.Log_Message = ""    
                for item in self.LogStack:
                    self.Log_Message = self.Log_Message + str(item)+"\n"
                self.log_font = pygame.font.Font(None, 15)
                self.Log_rect = pygame.Rect((0, 650, 300, 150))
                rendered_text = render_textrect(self.Log_Message, self.Log_font, self.Log_rect, (216, 216, 216), (48, 48, 48), 0)
                self.screen.blit(rendered_text, self.Log_rect.topleft)
                #Parameters:                 surface, color,       x,   y,  length, height, width, text,  text_color
                self.CloseLogButton.create_button(self.screen, (255, 0, 0), 285,  655,    10,    10,   10,    "X", (0, 0, 0))
            else:
                self.LogButton.create_button(self.screen, (0, 255, 0), 10,  750,  100,  30,   0,  "Log   ", (255,255,255))
            if(self.DetailsFlag == True):
                self.details_rect = pygame.Rect((724, 650, 300, 150))
                pygame.draw.rect(self.screen,(48, 48, 48),details_rect )
                self.details_sub_rect = pygame.Rect((724, 635, 300, 135))
                self.detailScreen = self.screen.subsurface(details_sub_rect)
                self.tmpSel = self.selection.sprites()
                
                #details_font = pygame.font.Font(None, 20)
                #rendered_text = render_textrect("Details Placeholder", details_font, details_rect, (216, 216, 216), (48, 48, 48), 0)
                #self.screen.blit(rendered_text, details_rect.midtop)
                #Parameters:                     surface, color,       x,   y,   length, height, width, text,       text_color
                self.CloseDetailsButton.create_button(self.screen, (255, 0, 0), 1010,  655,    10,    10,   10,    "X", (0, 0, 0))
            else:
                self.DetailsButton.create_button(self.screen, (0, 255, 0), 900,  750,    100,    30,   0,  "Details", (255,255,255))
            if(self.MissionFlag == True):
                self.mission_rect = pygame.Rect((330,650,350,150))
                pygame.draw.rect(self.screen,(48, 48, 48),self.mission_rect )
                #Draw the mission select buttons
                #Parameters:              surface, color,       x,   y,   length, height, width, text,       text_color
                self.MissionCoup.create_button(self.screen, (0, 255, 0), 340,  665,    100,    30,   0,  "Coup   ", (255,255,255))
                self.MissionGI.create_button(self.screen, (0, 255, 0), 455,  665,    100,    30,   0,  "Gather Info", (255,255,255))
                self.MissionDip.create_button(self.screen, (0, 255, 0), 565,  665,    100,    30,   0,  "Diplomacy", (255,255,255))
                self.MissionAssas.create_button(self.screen, (0, 255, 0), 340,  715,    100,    30,   0,  "Assasination", (255,255,255))
                self.MissionSubvert.create_button(self.screen, (0, 0, 255), 455,  715,    100,    30,   0,  "Subvert ", (255,255,255))
                self.MissionScavenge.create_button(self.screen, (0, 0, 255), 565,  715,    100,    30,   0,  "Scavenge", (255,255,255))
                self.MissionCamp.create_button(self.screen, (0, 0, 255), 340,  755,    100,    30,   0,  "Start Camp", (255,255,255))
                self.MissionRebelion.create_button(self.screen, (0, 255, 0), 455,  755,    210,    30,   0,  "Start/Stop Rebelion", (255,255,255))
                self.CloseMissionButton.create_button(self.screen, (255, 0, 0), 665,  655,    10,    10,   10,    "X", (0, 0, 0))
            else:
                self.MissionButton.create_button(self.screen, (0, 255, 0), 475,  745,    100,    30,   20,  "Missions", (255,255,255))
            if(self.HelpFlag == True):
                self.Help_Message = "This text will change based on the current player phase" 
                self.help_bg = pygame.Rect((0,0,300,30))
                self.pygame.draw.rect(self.screen,(48, 48, 48),help_bg)   
                self.help_font = pygame.font.Font(None, 15)
                self.help_rect = pygame.Rect((0, 20, 300, 280))
                self.rendered_text = render_textrect(self.Help_Message, self.help_font, self.help_rect, (216, 216, 216), (48, 48, 48), 0)
                self.screen.blit(self.rendered_text, help_rect.topleft)
                #Parameters:                 surface, color,       x,   y,  length, height, width, text,  text_color
                self.CloseHelpButton.create_button(self.screen, (255, 0, 0), 285,  5,    10,    10,   10,    "X", (0, 0, 0))
            else:
                self.HelpButton.create_button(self.screen, (0, 255, 0), 5,  5,  100,  30,   0,  "Help  ", (255,255,255))
            
            self.controls.draw(self.screen)

            pygame.display.flip()
		
def main():
    interface = GUI()
    interface.start()


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


class System():
    def __init__(self, name, planetlist, background, animate=None):
        self.name = name
        self.screen = pygame.display.get_surface()
        self.background = background
        self.planets = planetlist
        self.movedir = None
        self.animate = animate

    def planet_move(self, selectionlist):
        print 'SYSTEM - SELECTION:', selectionlist
        self.movedir = None
        for selectedplanet in selectionlist:
            # Move planets to the right
            if selectedplanet.orient is 'left':
                self.movedir = 'right'
                selectedplanet.update(self.movedir, self.animate)
                for planet in self.planets:
                    planet.update(self.movedir, self.animate)
            # Move planets to the left
            elif selectedplanet.orient is 'right':
                self.movedir = 'left'
                selectedplanet.update(self.movedir, self.animate)
                for planet in self.planets:
                    planet.update(self.movedir, self.animate)
            self.planets.add(selectedplanet)
            selectionlist.empty()
        if self.movedir and self.animate:
            self._planet_animate()

    def _planet_animate(self):
        # These need to be set in the singleton screen class
        curframe = 0    # <--
        frames = 64     # <--
        width = 512     # <--

        # Can this be cleaned up? Yes and it will
        offset = -1     # <--
        offsetadj = -1  # <--
        fill = -1       # <--
        filladj = -1    # <--

        # Move right - wrap around effect
        if self.movedir is 'right':
            while curframe < frames:
                for planet in self.planets:
                    if planet.porient is 'left':
                        planet.rect.move_ip(8, 0)
                    elif planet.porient is 'center':
                        planet.rect.move_ip(8, 0)
                    elif planet.porient is 'right':
                        planet.rect.move_ip(-16, 0)
                self.screen.blit(self.background, (0, 0))
                self.planets.draw(self.screen)
                pygame.display.flip()
                curframe += 1

        # Move left - slide from off screen effect
        elif self.movedir is 'left':
            while curframe < frames:
                for planet in self.planets:
                    if planet.porient is 'left':
                        offset = planet.rect.midright[0] - planet.rect.center[0]
                        fill = width - 2 * offset
                        if planet.rect.midright[0] >= 0 and planet.rect.midleft[0] < width:
                            planet.rect.move_ip(-8, 0)
                            filladj = fill
                        elif filladj >= 0:
                            filladj -= 8
                            planet.rect.midleft = self.screen.get_rect().midright
                            offsetadj = offset
                        elif offsetadj >= 0:
                            offsetadj -= 8
                            planet.rect.move_ip(-8, 0)
                    elif planet.porient is 'center':
                        planet.rect.move_ip(-8, 0)
                    elif planet.porient is 'right':
                        planet.rect.move_ip(-8, 0)
                self.screen.blit(self.background, (0, 0))
                self.planets.draw(self.screen)
                pygame.display.flip()
                curframe += 1
        self.planets.update()


class Planet(pygame.sprite.Sprite):
    def __init__(self, name, image, orientation):
        self.name = name
        self.orient = orientation  # Where the planet is in relation to the screen
        self.poreint = orientation  # Previous orientation
        self.screen = pygame.display.get_surface()
        if self.orient is 'left':
            self.pos = self.screen.get_rect().midleft
        elif self.orient is 'center':
            self.pos = self.screen.get_rect().center
        elif self.orient is 'right':
            self.pos = self.screen.get_rect().midright
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.rect.center = self.pos
        self.colliderect = self.rect.inflate(-50, -50)
        self.colliderect.normalize()
        self.environment = environs.EnvironBox(self.rect)
        self.environment.addEnviron(1, 'W', 4, "Humans", 4, "Animals", 'C' )
        self.environment.addEnviron(2, 'U', 4, "Humans", 4, "Animals", 'C' )
        self.environment.addEnviron(3, 'F', 3, "H", 2, "A", 'A')

    def update(self, movedir=None, animate=None):  # Update planet orientation
        self.porient = self.orient
        if movedir is 'right':
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
        else:
            self.rect.center = self.pos
            self.colliderect.center = self.pos
        self.environment.update()
           


class Ship(pygame.sprite.Sprite):
    def __init__(self, name, image, position):
        self.name = name
        self.pos = position
        self.loc = None
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.rect.center = self.pos

    def update(self, selected=None, animate=None):  # ship animation will be added later
        if selected:
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
        else:
            try:
                self.rect.clamp_ip(self.loc)
            except:
                #print 'WARNING:', self.name, 'is drifting - put it on a planet'
                return


class Stack():
    def __init__(self):
        self.list = []
        self.refresh = False

    def make(self, unit):
        print 'MAKING NEW STACK'  # Testing
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
                print 'REMOVING'  # Testing
                sprite = stack.get_top_sprite()
                sprite.rect.move_ip(0, -50)
                stack.remove(sprite)
                if len(stack) == 1:
                    self.list.remove(stack)

    def has(self, unit):
        for stack in self.list:
            if stack.has(unit):
                return True

    def cycle(self, unit):
        for stack in self.list:
            if stack.has(unit):
                sprite = stack.get_top_sprite()
                stack.move_to_back(sprite)
                self.refresh = True
                return

    def sprites(self, unit):
        for stack in self.list:
            if stack.has(unit):
                return stack.sprites()

    def update(self, unit, location):
        for stack in self.list:
            if stack.has(unit):
                self.refresh = True
                for sprite in stack:
                    sprite.loc = location
                    sprite.rect.clamp_ip(location)

    def draw(self, screen):
        if self.refresh:
            print 'REDRAWING'  # Testing
            for stack in self.list:
                print stack
                stack.draw(screen)
            self.refresh = False

    def highlight(self, mouse):
        for stack in self.list:
            for collision in pygame.sprite.spritecollide(mouse, stack, False):
                print collision.name


# Will be added to the mouse class
def select_check(unitlist, planetlist, mouse, selectionlist, unitstack):
    for unit in unitlist:
        if unit.rect.collidepoint(mouse.pos):
            if unitstack.has(unit):
                selectionlist.add(unitstack.sprites(unit))
                print 'SELECTED STACK: ', selectionlist, mouse.pos  # Testing
                #Update notification log
                LogStack.insert(0,"Ship: "+str(selectionlist)+" selected")
                return True, unit.rect.center, unit.loc
            else:
                selectionlist.add(unit)
                print 'SELECTED: ', selectionlist, mouse.pos  # Testing
                LogStack.insert(0,"Ship: "+str(selectionlist)+" selected")
                unitlist.remove(unit)
                return True, unit.rect.center, unit.loc
    for planet in planetlist:
        if planet.rect.collidepoint(mouse.pos):
            print 'SELECTED: ', planet.name  # Testing
            selectionlist.add(planet)
            planetlist.remove(planet)
            LogStack.insert(0,"Planet: "+planet.name+" selected")
            return True, None, None
    return False, None, None


# Will be added to the mouse class
def left_select_check(unitlist, mouse, selectionlist, unitstack, breakstack):
    if breakstack:
        for unit in unitlist:
            if unit.rect.collidepoint(mouse.pos):
                if unitstack.has(unit):
                    unitstack.remove(unit)
                    return True
    else:
        for unit in unitlist:
            if unit.rect.collidepoint(mouse.pos):
                unitstack.cycle(unit)
                return True


# Will be added to the mouse class
def unit_unselect_check(unitlist, planetlist, mouse, prev_pos, prev_loc, selectionlist, unitstack):
    for unit in selectionlist:
        if unitstack.has(unit):
            print 'UNSELECTING STACK'  # Testing
            for planet in planetlist:
                if planet.environment.addstack(unitstack) != 0:
                    selectionlist.empty()
                    return True
                if planet.rect.collidepoint(mouse.pos):
                    print 'STACK LANDING ON:', planet.name  # Testing
                    unitstack.update(unit, planet.colliderect)
                    selectionlist.empty()
                    return True
            unit.pos = prev_pos
            unit.rect.center = unit.pos
            unit.loc = prev_loc
            selectionlist.empty()
        else:
            print 'UNSELECTING SINGLE'  # Testing
            if _unit_stack_check(unitlist, unit, selectionlist, unitstack):
                    return True
            for planet in planetlist:
                if planet.environment.addstack(unitstack) != 0:
                    selectionlist.empty()
                    return True
                if planet.rect.collidepoint(mouse.pos):
                    print 'SINGLE LANDING ON:', planet.name  # Testing
                    unit.loc = planet.colliderect  # set the location of the ship to the planet !!
                    unit.rect.clamp_ip(planet.colliderect)
                    unitlist.add(unit)
                    selectionlist.empty()
                    return True
            unit.pos = prev_pos
            unit.rect.center = unit.pos
            unit.loc = unit.loc
            unitlist.add(unit)
            selectionlist.empty()
            return False


# Will be added to the mouse class
def _unit_stack_check(unitlist, selunit, selectionlist, unitstack):
    # if there are stacks present on the stack list, is the unit joining one of these existing stacks?
    for stack in unitstack.list:
        for collision in pygame.sprite.spritecollide(selunit, stack, False):
            selunit.pos = collision.pos
            selunit.loc = collision.loc
            selunit.rect.clamp_ip(collision.rect)
            unitstack.add(selunit, stack)
            unitlist.add(selunit)
            selectionlist.empty()
            unitstack.cycle(selunit)
            return True
    # if the unit is not joining an existing stack, create a new stack and append the stack onto the stack list.
    for unit in unitlist:
        if selunit.rect.colliderect(unit.rect):
            selunit.pos = unit.rect.center
            selunit.loc = unit.loc
            selunit.rect.clamp_ip(unit.rect)
            unitstack.add(unit, unitstack.make(selunit))
            unitlist.add(selunit)
            selectionlist.empty()
            unitstack.cycle(selunit)
            return True
    return False


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

class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//(len(text)*0.7))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 3, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):           
        #for i in range(1,10):
        s = pygame.Surface((length,height))
        s.fill(color)
        #alpha = (255/(i+2))
        #if alpha <= 0:
        #    alpha = 1
        #s.set_alpha(alpha)
        pygame.draw.rect(s, color, (x,y,length,height), width)
        #surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        #pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        #print "Some button was pressed!"
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    #import pygame
    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        #if accumulated_height + font.size(line)[1] >= rect.height:
            #raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface

if __name__ == '__main__':
    main()

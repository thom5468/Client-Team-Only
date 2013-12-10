#@PydevCodeAnalysisIgnore
import pygame, sys, os

from pygame.locals import *

pygame.init()

basepost = (0,0)
x = basepost[0]
y = basepost[1]
systemname = "Egrix"
planetname = "NameofPlanet"
planet1name = "Quibron"
planet2name = "Angoff"
planet3name = "Charkhan"
planet4name = "test1"
planet5name = "test2"
planetposition = (600, 70)
pdbupcolor = (52, 243, 14)
pdbdowncolor = (243,14,14)
backgroundcolor = (100,150,200) 
menubarcolor = (146,149,145)
planettextcolor = (0,0,0)
menubarposandsize = (x, y, 620, 150)
pdbbox = (x+10,y+30,100,100)
loyaltybox = (x+300, y+40, 300, 50)
planetnameposition = (x+350,y+100)
pdbboxpostion = (x+10,y+30)
loyaltycolor = (255,255,255)
loyaltytext = "Patriotic   Loyal   Neutral   Dissent   Unrest"
loyaltytextboxposition = (x+300,y+20,100,100)
loyaltytextcolor = (50,50,50)
loyaltyposition1 = (x+325,y+50)
loyaltyposition2 = (x+380,y+50)
loyaltyposition3 = (x+435,y+50)
loyaltyposition4 = (x+500,y+50)
loyaltyposition5 = (x+560,y+50)
loyaltymarkercolor = (0,0,0)
loyaltymarkersize = (25,25)
loyaltymarker5 = pygame.Rect(loyaltyposition5, loyaltymarkersize)
pdbstatustextcolor = (34,34,34)
pdbstatustextposition = (x+17,y+10)
pdbdowntext = "PDB Down"
pdbdowntextcolor = (0,0,0)
pdbdowntextpostition = (x+16,y+70)
pdbdowntextrect = pygame.font.Font(None, 25)
pdbdowntextsurface = pdbdowntextrect.render(pdbdowntext,1,pdbdowntextcolor)

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

class MenuBar():
    def __init__(self, planetname, planetnametextcolor, loyaltystate, pdbcontrol, backgroundcolor, position, pdbrect, PDBstatus=None):
        self.planetname = planetname
        self.planetnametextcolor = planetnametextcolor
        self.loyaltystate = loyaltystate
        self.pdbup = True
        self.pdbcontrol = "Rebel"
        self.backgroundcolor = backgroundcolor
        self.planetboxcolor = (255,200,200)
        self.buttoncolor = (50,102,255)
        self.position = (10,10)
        self.planetFontSurface = "Planet Surface"
        
    def draw(self, screen, menubar):
        #screen.fill(self.backgroundcolor)
        pygame.draw.rect(screen, menubarcolor, menubar, 0)
        #pygame.draw.rect(screen, pdbdowncolor, pdbrect,0)
        pygame.draw.rect(screen, loyaltycolor, loyaltyrect, 0)
        #pygame.draw.circle(screen, (45,45,45), planetposition, 50, 0)
        #pygame.image.load("earth.png")
        pygame.transform.scale(starbg, (screensize))
        screen.blit(planetFontSurface, planetnameposition) #planetname position
        screen.blit(pdbfontsurface,pdbboxpostion)
        screen.blit(loayaltytextsurface, loyaltytextboxposition)
        screen.blit(pdbstatustexsurface, pdbstatustextposition)
        if self.pdbup == True:
            screen.blit(pdb_image, pdbboxpostion)
        else:
            pygame.draw.rect(screen, pdbdowncolor, pdbdownrect, 0)
            screen.blit(pdbdowntextsurface, pdbdowntextpostition)
        if self.loyaltystate == 1:
            print "Loyalty State is 1"
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker1, 0)
        elif self.loyaltystate == 2:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker2, 0)            
            print "Loyalty State == 2"
        elif self.loyaltystate == 3:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker3, 0)            
            print "Loyalty State == 3"
        elif self.loyaltystate == 4:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker4, 0)            
            print "Loyalty State == 4"
        elif self.loyaltystate == 5:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker5, 0)            
            print "Loyalty State == 5"
        else:
            print "Undefined Loyalty State"
            
        #pygame.display.flip()
        
    def update(self, planetname, loyaltystate, pdbup, systemname):
        self.planetname = planetname
        self.loyaltystate = loyaltystate
        self.pdbup = pdbup
        self.systemname = systemname
        
if __name__ == '__main__':
    screensize = (800,600)
    screen = pygame.display.set_mode(screensize)
    starbg = pygame.image.load("stars.jpg")
    starbg = pygame.transform.scale(starbg, (screensize))
    
    menubar = pygame.Rect(menubarposandsize)
    pdbdownrect = pygame.Rect(pdbbox)
    #pdbrect = pygame.Rect(pdbbox)
    pdb_image, pdbrect = load_image("pdbup.png", None)
    pdbrect.topleft = pdbboxpostion
    loyaltyrect = pygame.Rect(loyaltybox)
    loyaltytextrect = pygame.Rect(loyaltytextboxposition)
    loyaltymarker1 = pygame.Rect(loyaltyposition1, loyaltymarkersize)
    loyaltymarker2 = pygame.Rect(loyaltyposition2, loyaltymarkersize)
    loyaltymarker3 = pygame.Rect(loyaltyposition3, loyaltymarkersize)
    loyaltymarker4 = pygame.Rect(loyaltyposition4, loyaltymarkersize)

    
    
    PlanetName = pygame.font.Font(None, 60)
    pdbtextrect = pygame.font.Font(None, 25)
    loyaltytextrectfont = pygame.font.Font(None, 20)
    
    
    
    planetname = planet1name
    pdbstatustext = "PDB Status"
    pdbstatustextrect = pygame.font.Font(None, 20)

    
    
    
    pdbfontsurface = pdbtextrect.render(pdbstatustext, 1, (255,255,255))
    planetFontSurface = PlanetName.render(planetname, 1, planettextcolor)
    loayaltytextsurface = loyaltytextrectfont.render(loyaltytext, 1, loyaltytextcolor)
    pdbstatustexsurface = pdbstatustextrect.render(pdbstatustext, 1, (255,255,255))

    menu = MenuBar(planet1name, (25,47,69), 1, "Up", backgroundcolor, (10,10), pdbrect)
    
    
    while 1:
        #refresh process
        #do updating
        
        
        #draw proccess
        #def update(self, planetname, loyaltystate, pdbup, systemname):
        screen.blit(starbg, (0,0))
        menu.draw(screen, menubar)
        print menu.planetname
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet1name:
                menu.update(planet2name, 3, True, "Shiny Star")
                print menu.planetname
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet2name:
                menu.update(planet3name, 4, False, "Shiny Star")
                print menu.planetname
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet3name:
                menu.update(planet4name, 5, True, "Shiny Star")
                print menu.planetname
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet4name:
                menu.update(planet5name, 1, True, "Shiny Star")
                print menu.planetname
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet5name:
                menu.update(planet1name, 2, True, "Shiny Star")
                print menu.planetname
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()        
















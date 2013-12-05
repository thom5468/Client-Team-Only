#@PydevCodeAnalysisIgnore
import pygame, sys, os

from pygame.locals import *

pygame.init()
basepost = (0,0)

x = basepost[0]
y = basepost[1]
systemname = "Egrix"
planet1name = "Quibron"
planet2name = "Angoff"
planet3name = "Charkhan"
planetposition = (600, 70)
pdbupcolor = (52, 243, 14)
pdbdowncolor = (243,14,14)
backgroundcolor = (100,150,200) 
menubarcolor = (146,149,145)
planettextcolor = (0,0,0)
menubarposandsize = (200, 10, 620, 150)
pdbbox = (210,50,100,100)
loyaltybox = (500, 50, 300, 50)
planetnameposition = (550,110)
pdbboxpostion = (210,20)
loyaltycolor = (255,255,255)
loyaltytext = "Patriotic   Loyal   Neutral   Dissent   Unrest"
loyaltytextboxposition = (500,30,100,100)
loyaltytextcolor = (50,50,50)


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
	def __init__(self, planetname, planetnametextcolor, loyaltyrank, pdbcontrol, backgroundcolor, position, pdbrect, PDBstatus=None):
		self.planetname = planetname
		self.planetnametextcolor = planetnametextcolor
		self.loyaltyrank = loyaltyrank
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
		#pygame.display.flip()

	def update(self, planetname):
		self.planetname = planetname
	#def update(self)	

	
if __name__ == '__main__':
	screensize = (800,600)
	screen = pygame.display.set_mode(screensize)
	starbg = pygame.image.load("stars.jpg")
	starbg = pygame.transform.scale(starbg, (screensize))
	
	menubar = pygame.Rect(menubarposandsize)
	#pdbrect = pygame.Rect(pdbbox)
	pdb_image, pdbrect = load_image("pdbup.png", None)
	pdbrect.topleft = (210, 50)
	loyaltyrect = pygame.Rect(loyaltybox)
	loyaltytextrect = pygame.Rect(loyaltytextboxposition)
	
	
	PlanetName = pygame.font.Font(None, 60)
	pdbtextrect = pygame.font.Font(None, 25)
	loyaltytextrectfont = pygame.font.Font(None, 20)
	
	
	
	planetname = planet1name
	pdbtext = "PDB Status"

	
	
	
	pdbfontsurface = pdbtextrect.render(pdbtext, 1, (255,255,255))
	planetFontSurface = PlanetName.render(planetname, 1, planettextcolor)
	loayaltytextsurface = loyaltytextrectfont.render(loyaltytext, 1, loyaltytextcolor)

	menu = MenuBar("Egrix", (25,47,69), 5, "Up", backgroundcolor, (10,10), pdbrect)
	
	
	while 1:
		#refresh process
		#do updating
		
		
		#draw proccess
		
		screen.blit(starbg, (0,0))
		menu.draw(screen, menubar)
		screen.blit(pdb_image, (0, 0))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and planetname == planet1name:
				menu.update(planet2name)
				planetname = planet2name
				planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
			elif event.type == pygame.MOUSEBUTTONDOWN and planetname == planet2name:
				menu.update(planet3name)
				planetname = planet3name
				planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
			elif event.type == pygame.MOUSEBUTTONDOWN and planetname == planet3name:
				menu.update(planet1name)
				planetname = planet1name
				planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()
		

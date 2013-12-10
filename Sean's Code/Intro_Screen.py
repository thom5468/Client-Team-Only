import pygame, string
import New_Dumb_GUI
import rpyc
from fitg.backend.service import ClientService

pygame.init()

class my_textbox:
    def __init__(self, title):
        self.title = title
        self.text = []
        self.input = ''
        self.default_color = (100,100,100)
        self.font_color = (220, 220, 20)
        self.obj = None
        self.nextchar = "_"
    
    def switchchar (self):
        if self.nextchar == "_":
            self.nextchar = chr(9)
        else:
            self.nextchar ="_"
        
    def label(self, text):
        font = pygame.font.Font(None, 20)
        return font.render(text, 1, self.font_color)
        
    def addkey (self, inkey):
        if inkey == pygame.K_BACKSPACE:
            self.text = self.text[0:-1]
        elif inkey == pygame.K_MINUS:
            self.text.append("-")
        elif inkey <= 127:
            if len(self.text) < 30:
                self.text.append(chr(inkey))
        self.input = string.join(self.text,"")
    
    def draw (self, screen, rect_coord):
        label_coord = (rect_coord[0]+4, rect_coord[1]+4)
        self.obj = pygame.draw.rect(screen, self.default_color, rect_coord)
        screen.blit(self.label(self.title), (label_coord[0], label_coord[1]))
        screen.blit(self.label(self.input+self.nextchar), (label_coord[0], label_coord[1]+20))
        pygame.draw.line(screen, self.font_color, (label_coord[0], label_coord[1]+33),(label_coord[0]+242, label_coord[1]+33))

class my_button:
    def __init__(self, text, alttext='', fontsize = 40):
        self.text = text
        self.alttext = alttext
        self.is_alt = False
        self.is_hover = False
        self.fontsize = fontsize
        self.default_color = (100,100,100)
        self.hover_color = (204,102, 0)
        self.font_color = (220, 220, 20)
        self.obj = None
        
    def switch_text(self):
        self.is_alt = not self.is_alt
        
    def label(self):
        font = pygame.font.Font(None, self.fontsize)
        if self.is_alt:
            return font.render(self.alttext, 1, self.font_color)
        else:
            return font.render(self.text, 1, self.font_color)
        
    def color(self):
        if self.is_hover:
            return self.hover_color
        else:
            return self.default_color
            
    def draw(self, screen, mouse, rect_coord, label_coord):
        self.obj  = pygame.draw.rect(screen, self.color(), rect_coord)
        screen.blit(self.label(), label_coord)
        self.check_hover(mouse)
        
    def check_hover(self, mouse):
        if self.obj.collidepoint(mouse):
            self.is_hover = True 
        else:
            self.is_hover = False
    
class gamelistingbox:
    def __init__ (self):
        self.obj = None
        self.default_color = (50,50,50)
        self.hover_color = (204,102, 0)
        self.font_color = (220, 220, 20)
        self.fontsize = 20
        self.joinbutton = my_button("Join", fontsize = self.fontsize)
        self.cancelbutton = my_button("Cancel", fontsize = self.fontsize)
        self.refreshbutton = my_button("Refresh", fontsize = self.fontsize)
        self.visible = False
        self.scenarioflag = False
        self.x = 30
        self.y = 275
        self.width = 475
        self.height = 250
        self.selectedgame = None
        self.selectedindex = None
        self.gamelist = []
        self.namelist = []
        self.playerlist = []
        self.scenariolist = []
        self.sidelist = []
        self.gamebox = pygame.Rect(self.x, self.y+self.fontsize, self.width, self.fontsize*len(self.namelist))
        self.loadingtext = self.label("Loading", 60)
        
    def label(self, text, font_size):
        font = pygame.font.Font(None, font_size)
        return font.render(text, 1, self.font_color)
            
    def draw(self, screen, mouse):
        if self.visible:
            #if self.response is not None:
            #    if self.response.ready:
            #        self.processresponse()
            #        self.response = None
            self.obj = pygame.draw.rect(screen, self.default_color, (self.x, self.y, self.width, self.height))
            self.joinbutton.draw(screen, mouse, (self.x+30, self.y+225, 100, self.fontsize), (self.x+65, self.y+225+4))
            self.cancelbutton.draw(screen, mouse, (self.x+self.width-130, self.y+225, 100, self.fontsize), (self.x+self.width-130+25, self.y+225+4))
            self.refreshbutton.draw(screen, mouse, ((self.x+(self.width-100)/2), self.y+225, 100, self.fontsize), ((self.x+(self.width-100)/2)+25, self.y+225+4))
            
            screen.blit(self.label("Game Name", self.fontsize), (self.x+34, self.y+4))
            screen.blit(self.label("Player Name", self.fontsize), (self.x+184, self.y+4))
            screen.blit(self.label("Player Side", self.fontsize), (self.x+313, self.y+4))
            screen.blit(self.label("Scenario", self.fontsize), (self.x+408, self.y+4))
            
            pygame.draw.line(screen, self.font_color, (self.x+150, self.y+4), (self.x+150, self.y+220))
            pygame.draw.line(screen, self.font_color, (self.x+300, self.y+4), (self.x+300, self.y+220))
            pygame.draw.line(screen, self.font_color, (self.x+400, self.y+4), (self.x+400, self.y+220))
            pygame.draw.line(screen, self.font_color, (self.x+4, self.y+self.fontsize), (self.x+467, self.y+self.fontsize))
            pygame.draw.line(screen, self.font_color, (self.x+4, self.y+220), (self.x+467, self.y+220))
            
            if self.selectedindex is not None:
                pygame.draw.rect(screen, self.hover_color, (self.x+4, self.y+(self.fontsize*(self.selectedindex+1)), 467, self.fontsize))
            
            for name in self.namelist:
                screen.blit(name[0], name[1])
            for player in self.playerlist:
                screen.blit(player[0], player[1])
            for scenario in self.scenariolist:    
                screen.blit(scenario[0], scenario[1])
            for side in self.sidelist:    
                screen.blit(side[0], side[1])
            
    def drawloading(self, screen):
        screen.blit(self.loadingtext, (self.x+100, self.y+100))
    
    def checkclick(self, mouse):
        if mouse[0] > self.x and mouse[0] < self.x+self.width:
            self.selectedindex = int((mouse[1]-self.y-self.fontsize)/self.fontsize)
            self.selectedgame = self.gamelist[self.selectedindex]
            if self.selectedgame["scenario"] == "egrix":
                self.scenarioflag = False
            else:
                self.scenarioflag = True
            #if self.selectedgame["allegiance"] == "rebel":
            #    self.sideflag = True
    
    def setgamelist(self, gamedict):
        print "Stuff"
        self.gamelist = []
        self.namelist = []
        self.playerlist = []
        self.scenariolist = []
        self.sidelist = []
        for index, game in enumerate(gamedict['response']['games']):
            if index < 10:
                self.gamelist.append(game)
                self.namelist.append((self.label(game["name"], self.fontsize), (self.x+4, self.y+4+((index+1)*self.fontsize))))
                self.playerlist.append((self.label(game["player1"], self.fontsize), (self.x+154, self.y+4+((index+1)*self.fontsize))))
                self.scenariolist.append((self.label(game["scenario"], self.fontsize), (self.x+404, self.y+4+((index+1)*self.fontsize))))
                #self.sidelist.append((self.label(game["allegiance"], self.fontsize), (self.x+304, self.y+4+((index+1)*self.fontsize)))
        self.gamebox = pygame.Rect(self.x, self.y+self.fontsize, self.width, self.fontsize*len(self.namelist))
        
            
        
def setscenario(scenarioflag):
    if scenarioflag is False:
        return 'egrix'
    else:
        return 'powder keg'
        
def setplayer( sideflag):
    if sideflag:
        return 'rebel'
    else:
        return 'imperial'
   
            
if __name__ == '__main__':

    client = rpyc.connect("elegantgazelle.com", 55889, ClientService)

    background = pygame.image.load("freedom_galaxy.jpg")
    #background = pygame.transform.scale(background, (389, 489))

    start = my_button('Start Game')
    join = my_button('Join Game')
    allegiance = my_button('Rebel', 'Empire')
    single_player = my_button('Play AI', '2 Player')
    scenario = my_button('Flight', 'Powder')
    exit = my_button('Exit Game')
    gametextbox = my_textbox('Game Name')
    playertextbox = my_textbox('Your Name')
    screen = pygame.display.set_mode((536,720))
    listingbox = gamelistingbox()
    
    playerside = ''
    playerscenario = ''

    pygame.mixer.music.load('starwars-maintheme.mp3') 
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    redrawscreen = False
    screen.blit(background, background.get_rect())
    pygame.display.flip()
    
    gamelistasync = rpyc.async(client.root.list_games)
    
    selectedtextbox = None
    
    run = True
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if selectedtextbox is not None:
                    if event.key == 9:
                        if selectedtextbox == gametextbox:
                            selectedtextbox.switchchar()
                            selectedtextbox = playertextbox
                            selectedtextbox.switchchar()
                        elif selectedtextbox == playertextbox:
                            selectedtextbox.switchchar()
                            selectedtextbox = gametextbox
                            selectedtextbox.switchchar()
                    else:
                        selectedtextbox.addkey(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start.obj.collidepoint(mouse):
                    run = False
                    #pygame.mixer.music.stop()
                    playerscenario = setscenario(scenario.is_alt)
                    playerside = setplayer( allegiance.is_alt)
                    gamesetup = client.root.start_game(name=gametextbox.input, player=playertextbox.input) #, scenario=playerscenario, ai=single_player.is_alt)
                    print("Getting state of planets")
                    planet = client.root.get_state(object_id=1, object_type="Planet")
                    print planet
                    print gamesetup
                    New_Dumb_GUI.main(gamesetup)
                    #fire request to server
                    print('my_button start game clicked')
                elif join.obj.collidepoint(mouse):
                    listingbox.visible = True
                    gamelisting = gamelistasync()
                    print('my_button join game clicked')
                elif allegiance.obj.collidepoint(mouse):
                    allegiance.switch_text()
                    if single_player.is_alt is False:
                        allegiance.is_alt = False
                    print('my_button rebel clicked')
                elif single_player.obj.collidepoint(mouse):
                    single_player.switch_text()
                    if single_player.is_alt is False:
                        allegiance.is_alt = False
                    print('my button player vs AI clicked')
                elif scenario.obj.collidepoint(mouse):
                    scenario.switch_text()
                    print('my button scenario clicked')
                elif exit.obj.collidepoint(mouse):
                    run = False
                    print('my button exit clicked')
                elif gametextbox.obj.collidepoint(mouse):
                    if selectedtextbox is not None:
                        selectedtextbox.switchchar()
                    selectedtextbox = gametextbox
                    selectedtextbox.switchchar()
                elif playertextbox.obj.collidepoint(mouse):
                    if selectedtextbox is not None:
                        selectedtextbox.switchchar()
                    selectedtextbox = playertextbox
                    selectedtextbox.switchchar()
                elif listingbox.visible is True:
                    if listingbox.obj.collidepoint(mouse):
                        if listingbox.cancelbutton.obj.collidepoint(mouse):
                            redrawscreen = True
                            listingbox.visible = False
                        elif listingbox.joinbutton.obj.collidepoint(mouse):
                            run = False
                            #pygame.mixer.music.stop()
                            playerscenario = setscenario(scenario.is_alt)
                            playerside = setplayer( allegiance.is_alt)
                            gamesetup = client.root.join_game(name=gametextbox.input, player=playertextbox.input) #scenario=playerscenario
                            print gamesetup
                            New_Dumb_GUI.main(gamesetup)
                        elif listingbox.refreshbutton.obj.collidepoint(mouse):
                            gamelisting = gamelistasync()
                        elif listingbox.gamebox.collidepoint(mouse):
                            listingbox.checkclick(mouse)
                            
                        
        if redrawscreen is True:
            screen.blit(background, background.get_rect())
            pygame.display.flip()
            redrawscreen = False
        
        if listingbox.visible is True:
            listingbox.draw(screen, mouse)
            if gamelisting is not None:
                if gamelisting.ready:
                    listingbox.setgamelist(gamelisting.value)
                    gamelisting = None
                else:
                    listingbox.drawloading(screen)
            single_player.is_alt = True
            if listingbox.selectedgame is not None:
                gametextbox.input = listingbox.selectedgame["name"]
                gametextbox.text = list(gametextbox.input)
                scenario.is_alt = listingbox.scenarioflag
                
        
        start.draw(screen, mouse, (13,650,170,40), (18,658))
        join.draw(screen, mouse, (196,650,155,40), (201,658))
        exit.draw(screen, mouse, (364,650,155,40), (369,658))
        
        single_player.draw(screen, mouse, (13,607,170,40), (18,611))
        allegiance.draw(screen, mouse, (196,607,155,40), (201,611))
        scenario.draw(screen, mouse, (364,607,155,40), (369,611))
        
        gametextbox.draw(screen, (13,560,250,42))
        playertextbox.draw(screen, (270,560,250,42))
        
        

        pygame.display.update()
        clock.tick(60)
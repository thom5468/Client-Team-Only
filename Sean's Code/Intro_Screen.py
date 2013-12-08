import pygame, string
import New_Dumb_GUI
import rpyc
import fitg.backend.service as service
#import Demo2

pygame.init()

class my_textbox:
    def __init__(self, title):
        self.title = title
        self.text = []
        self.input = ''
        self.default_color = (100,100,100)
        self.font_color = (220, 220, 20)
        self.obj = None
        
    def label(self, text):
        font = pygame.font.Font(None, 20)
        return font.render(text, 1, self.font_color)
        
    def addkey (self, inkey):
        if inkey == pygame.K_BACKSPACE:
            self.text = self.text[0:-1]
        elif inkey == pygame.K_MINUS:
            self.text.append("_")
        elif inkey <= 127:
            self.text.append(chr(inkey))
        self.input = string.join(self.text,"")
    
    def draw (self, screen, rect_coord):
        label_coord = (rect_coord[0]+4, rect_coord[1]+4)
        self.obj = pygame.draw.rect(screen, self.default_color, rect_coord)
        screen.blit(self.label(self.title), (label_coord[0], label_coord[1]))
        screen.blit(self.label(self.input), (label_coord[0], label_coord[1]+20))
        pygame.draw.line(screen, self.font_color, (label_coord[0], label_coord[1]+42),(label_coord[0]+242, label_coord[1]+42))

class my_button:
    def __init__(self, text, alttext=''):
        self.text = text
        self.alttext = alttext
        self.is_alt = False
        self.is_hover = False
        self.default_color = (100,100,100)
        self.hover_color = (204,102, 0)
        self.font_color = (220, 220, 20)
        self.obj = None
        
    def switch_text(self):
        self.is_alt = not self.is_alt
        
    def label(self):
        font = pygame.font.Font(None, 40)
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

    client = rpyc.connect("elegantgazelle.com", 55889, service.ClientService)

    background = pygame.image.load("freedom_galaxy.jpg")
    #background = pygame.transform.scale(background, (389, 489))

    start = my_button('Start Game')
    join = my_button('Join Game')
    #option = my_button('Option')
    allegiance = my_button('Rebel', 'Empire')
    #imperial = my_button('Imperials')
    single_player = my_button('Play AI', '2 Player')
    #two_player = my_button('Player vs Player')
    scenario = my_button('Flight', 'Powder')
    exit = my_button('Exit Game')
    gametextbox = my_textbox('Game Name')
    playertextbox = my_textbox('Your Name')
    #demo = my_button('PROTOTYPE')
    #screen = pygame.display.set_mode((298,389))
    screen = pygame.display.set_mode((536,720))
    
    playerside = ''
    playerscenario = ''

    pygame.mixer.music.load('starwars-maintheme.mp3') 
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    screen.blit(background, background.get_rect())
    pygame.display.flip()
    
    selectedtextbox = None
    
    run = True
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if selectedtextbox is not None:
                    selectedtextbox.addkey(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start.obj.collidepoint(mouse):
                    run = False
                    #pygame.mixer.music.stop()
                    playerscenario = setscenario(scenario.is_alt)
                    playerside = setplayer( allegiance.is_alt)
                    gamesetup = client.root.start_game(name=gametextbox.input, player=playertextbox.input,  ai=single_player.is_alt) #scenario=playerscenario
                    print gamesetup
                    New_Dumb_GUI.main(gamesetup)
                    #fire request to server
                    print('my_button start game clicked')
                elif join.obj.collidepoint(mouse):
                    #client.root.list_games()
                    print('my_button join game clicked')
                elif allegiance.obj.collidepoint(mouse):
                    allegiance.switch_text()
                    if single_player.is_alt is False:
                        allegiance.is_alt = False
                    print('my_button rebel clicked')
#               elif imperial.obj.collidepoint(mouse):
#                   print('my_button imperials clicked')
                elif single_player.obj.collidepoint(mouse):
                    single_player.switch_text()
                    if single_player.is_alt is False:
                        allegiance.is_alt = False
                    print('my button player vs AI clicked')
#               elif two_player.obj.collidepoint(mouse):
#                   print('my button player vs player clicked')
                elif scenario.obj.collidepoint(mouse):
                    scenario.switch_text()
                    print('my button scenario clicked')
                elif exit.obj.collidepoint(mouse):
                    run = False
                    print('my button exit clicked')
                elif gametextbox.obj.collidepoint(mouse):
                    selectedtextbox = gametextbox
                elif playertextbox.obj.collidepoint(mouse):
                    selectedtextbox = playertextbox
                #elif demo.obj.collidepoint(mouse):
                    #run = False
                    #Demo2.main()

        #start.draw(screen, mouse, (90,300,120,22), (115,303))
        #option.draw(screen, mouse, (90,330,120,22), (125,333))
        #exit.draw(screen, mouse, (90,360,120,22), (115,363))

        start.draw(screen, mouse, (13,650,170,40), (18,658))
        join.draw(screen, mouse, (196,650,155,40), (201,658))
        exit.draw(screen, mouse, (364,650,155,40), (369,658))
        
        single_player.draw(screen, mouse, (13,607,170,40), (18,611))
        allegiance.draw(screen, mouse, (196,607,155,40), (201,611))
        scenario.draw(screen, mouse, (364,607,155,40), (369,611))
        
        gametextbox.draw(screen, (13,550,250,50))
        playertextbox.draw(screen, (270,550,250,50))
        
        #demo.draw(screen, mouse, (162,651,215,40), (188,654))

        pygame.display.update()
        clock.tick(60)
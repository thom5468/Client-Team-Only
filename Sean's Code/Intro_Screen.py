import pygame
import New_Dumb_GUI
#import Demo2

pygame.init()

class my_button:
   def __init__(self, text):
      self.text = text
      self.is_hover = False
      self.default_color = (100,100,100)
      self.hover_color = (204,102, 0)
      self.font_color = (220, 220, 20)
      self.obj = None
      
   def label(self):
      font = pygame.font.Font(None, 40)
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
         
if __name__ == '__main__':

   background = pygame.image.load("freedom_galaxy.jpg")
   #background = pygame.transform.scale(background, (389, 489))

   start = my_button('Start Game')
   #option = my_button('Option')
   rebel = my_button('Rebels')
   imperial = my_button('Imperials')
   single_player = my_button('Player vs AI')
   two_player = my_button('Player vs Player')
   exit = my_button('Exit Game')
   #demo = my_button('PROTOTYPE')
   #screen = pygame.display.set_mode((298,389))
   screen = pygame.display.set_mode((536,720))

   pygame.mixer.music.load('starwars-maintheme.mp3') 
   pygame.mixer.music.play(-1)

   clock = pygame.time.Clock()

   screen.blit(background, background.get_rect())
   pygame.display.flip()
   
   run = True
   while run:
      mouse = pygame.mouse.get_pos()
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
         elif event.type == pygame.MOUSEBUTTONDOWN:
            if start.obj.collidepoint(mouse):
               run = False
               #pygame.mixer.music.stop()
               New_Dumb_GUI.main()
               #fire request to server
               print('my_button start game clicked')
            elif rebel.obj.collidepoint(mouse):
               print('my_button rebel clicked')
            elif imperial.obj.collidepoint(mouse):
               print('my_button imperials clicked')
            elif single_player.obj.collidepoint(mouse):
               print('my buttom player vs AI clicked')
            elif two_player.obj.collidepoint(mouse):
               print('my button player vs player clicked')
            elif exit.obj.collidepoint(mouse):
               run = False
               print('my button exit clicked')
            #elif demo.obj.collidepoint(mouse):
               #run = False
               #Demo2.main()

      #start.draw(screen, mouse, (90,300,120,22), (115,303))
      #option.draw(screen, mouse, (90,330,120,22), (125,333))
      #exit.draw(screen, mouse, (90,360,120,22), (115,363))

      start.draw(screen, mouse, (162,475,215,40), (202,478))
      rebel.draw(screen, mouse, (51,519,215,40), (115,522))
      imperial.draw(screen, mouse, (270,519,215,40), (315,522))
      single_player.draw(screen, mouse, (51,563,215,40), (80,566))
      two_player.draw(screen, mouse, (270,563,215,40), (272,566))
      exit.draw(screen, mouse, (162,607,215,40), (207,610))
      #demo.draw(screen, mouse, (162,651,215,40), (188,654))

      pygame.display.update()
      clock.tick(60)
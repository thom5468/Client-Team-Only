import pygame

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
      font = pygame.font.Font(None, 22)
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
         
   start = my_button('Start game')
   option = my_button('Option')
   exit = my_button('Exit game')
   
   screen = pygame.display.set_mode((289,389))
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
            if my_button_.obj.collidepoint(mouse):
               print('my_button start clicked')
            elif my_button_2.obj.collidepoint(mouse):
               print('my_button option clicked')
            elif my_button_3.obj.collidepoint(mouse):
               print('my_button exit clicked')
      
      start.draw(screen, mouse, (90,300,120,22), (115,303))
      option.draw(screen, mouse, (90,330,120,22), (125,333))
      exit.draw(screen, mouse, (90,360,120,22), (115,363))
      
      pygame.display.update()
      clock.tick(50)

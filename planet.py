import pygame
import environments
from loadimage import load_image


class Planet(pygame.sprite.Sprite):
    def __init__(self, parent_system, planet_id, planet_name, planet_orientation, image):
        self.parent = parent_system
        self.id = planet_id
        self.name = planet_name
        self.orient = planet_orientation
        self.prev_orient = None
        if self.orient is "left":
            self.pos = self.parent.screen.get_rect().midleft
        elif self.orient is "center":
            self.pos = self.parent.screen.get_rect().center
        elif self.orient is "right":
            self.pos = self.parent.screen.get_rect().midright
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.collide_rect = self.rect.inflate(-50, -50)
        #=======================================================================
        # Environment Population
        #=======================================================================
        self.environment = environments.EnvironBox(self, self.rect)
        self.environment.addEnviron(1, 'W', 2, "Humans", "Animals", 'C')
        self.environment.addEnviron(2, 'U', 1, "Bricktons", "Animals", 'C')
        self.environment.addEnviron(3, 'F', 3, "Corruptons", "Animals", 'A')

    def update(self, move_dir=None, animate=None):
        self.prev_orient = self.orient
        if move_dir is "right":
            if self.orient is "left":
                self.pos = self.parent.screen.get_rect().center
                self.orient = "center"
            elif self.orient is "center":
                self.pos = self.parent.screen.get_rect().midright
                self.orient = "right"
            elif self.orient is "right":
                self.pos = self.parent.screen.get_rect().midleft
                self.orient = "left"
            if not animate:
                self.rect.center = self.pos
                self.collide_rect.center = self.pos
        elif move_dir is "left":
            if self.orient is "left":
                self.pos = self.parent.screen.get_rect().midright
                self.orient = "right"
            elif self.orient is "center":
                self.pos = self.parent.screen.get_rect().midleft
                self.orient = "left"
            elif self.orient is "right":
                self.pos = self.parent.screen.get_rect().center
                self.orient = "center"
            if not animate:
                self.rect.center = self.pos
                self.collide_rect.center = self.pos
        else:
            self.rect.center = self.pos
            self.collide_rect.center = self.pos
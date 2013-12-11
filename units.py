import pygame
from loadimage import load_image


class Unit(pygame.sprite.DirtySprite):
    def __init__(self, unit_name, unit_location_id, unit_id, stack_id, image):
        self.name = unit_name
        self.id = unit_id
        self.stack_id = stack_id
        self.loc_id = unit_location_id
        self.pos = None
        self.loc = None
        pygame.sprite.DirtySprite.__init__(self)
        self.image, self.rect = load_image(image)
        self.prev_image = self.image
        self.dirty = 2
        self.stack_list = list()
        self.stack_list.append(self)

    def set_stack_id (self, new_stack_id):
        for unit in self.stack_list:
            unit.stack_id = new_stack_id
    
    def cycle_unit(self):
        if len(self.stack_list) > 1:
            sprite = self.stack_list.pop()
            self.stack_list.insert(0, sprite)
            if sprite == self:
                self.image = self.prev_image
            else:
                self.image = sprite.image

    def add_unit(self, sprite):
        #sprite.visible = 0
        #sprite.loc_id = self.loc_id
        #sprite.pos = self.pos
        #sprite.loc = self.loc
        sprite.set_stack_id(self.stack_id)
        self.stack_list.extend(sprite.stack_list)
        sprite.stack_list = list()
        for sprite in self.stack_list:
            sprite.image = sprite.prev_image

    def remove_unit(self):
        if len(self.stack_list) > 1:
            sprite = self.stack_list.pop()
            if sprite == self:
                self.stack_list.insert(0, self)
                sprite = self.stack_list.pop()
            if len(self.stack_list) == 1:
                self.image = self.prev_image
            sprite.visible = 1
            sprite.loc_id = self.loc_id
            sprite.pos = self.pos
            sprite.loc = self.loc
            sprite.stack_list.append(sprite)
            return sprite
        else:
            return None

    def update(self, selected=None, animate=None):
        if selected:
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
        else:
            try:
                if self.loc:
                    self.rect.clamp_ip(self.loc)
                else:
                    self.rect.center = self.pos
            except:
                print "ERROR:", self.name, "is drifting"
                return
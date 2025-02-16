import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super.__init__(self)

        self.game = game
        self.layer = P_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * pixels
        self.y = y * pixels
        self.width = pixels
        self.height = pixels

        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass

    def movekeys(self):
        pass


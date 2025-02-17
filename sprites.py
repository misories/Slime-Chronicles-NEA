import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)

        self.game = game
        self.game.all_sprites.change_layer(self, P_layer)
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Set Sprite to 32x32
        self.x = x * pixels
        self.y = y * pixels
        self.width = pixels
        self.height = pixels

        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Movement
        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.movekeys()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        # Reset Values
        self.x_change = 0
        self.y_change = 0

    def movekeys(self):

        # Checking Input
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            self.x_change -= speed
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            self.x_change += speed
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.y_change -= speed
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.y_change += speed

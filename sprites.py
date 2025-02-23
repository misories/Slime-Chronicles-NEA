import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)

        self.game = game
        self._layer = P_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Set Sprite to 32x32
        self.x = x * pixels
        self.y = y * pixels
        self.w = pixels
        self.h = pixels

        imageload1 = pygame.image.load("Pics/Sprite/slime2.png")
        self.image = pygame.Surface([self.w,self.h])
        self.image.set_colorkey(BLACK)
        self.image.blit(imageload1,(0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Movement
        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.movekeys()
        self.rect.x += self.x_change
        self.collision("x")
        self.rect.y += self.y_change
        self.collision("y")

        # Reset Values
        self.x_change = 0
        self.y_change = 0

    def movekeys(self):

        # Checking Input
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            self.y_change -= speed
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            self.y_change += speed
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.x_change -= speed
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.x_change += speed

    def collision(self, direction):
        if direction == "x":
            collide = pygame.sprite.spritecollide(self,self.game.blocks, False)
            if collide:
                if self.x_change > 0:
                    self.rect.right = collide[0].rect.left
                if self.x_change < 0:
                    self.rect.left = collide[0].rect.right

        if direction == "y":
            collide = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if collide:
                if self.y_change > 0:
                    self.rect.bottom = collide[0].rect.top
                if self.y_change < 0:
                    self.rect.top = collide[0].rect.bottom

    def animation(self):
        down_ani = [self]

class Walls(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = W_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * pixels
        self.y = y * pixels
        self.w = pixels
        self.h = pixels

        self.image = self.game.terrain.get_one(544,352, self.w, self.h)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Grounds(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = G_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * pixels
        self.y = y * pixels
        self.w = pixels
        self.h = pixels

        self.image = self.game.terrain.get_one(64, 352, self.w, self.h)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()
        self.load = pygame.image.load

    def get_one(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
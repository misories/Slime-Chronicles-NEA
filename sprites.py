import pygame
from config import *
import math

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

        self.load = pygame.image.load
        self.down1 = self.load("Pics/Sprite/slime2.png")
        self.image = pygame.Surface([self.w,self.h])
        self.image.set_colorkey(BLACK)
        self.image.blit(self.down1,(0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Movement
        self.x_change = 0
        self.y_change = 0
        self.facing = "down"
        self.ani_loop = 1

        self.camx = 0
        self.camy = 0
        # Right Animation
        self.right1 = self.load("Pics/Sprite/slime2right1.png")
        self.right2 = self.load("Pics/Sprite/slime2right2.png")
        self.right3 = self.load("Pics/Sprite/slime2right3.png")

        # Left Animation
        self.left1 = self.load("Pics/Sprite/slime2left1.png")
        self.left2 = self.load("Pics/Sprite/slime2left2.png")
        self.left3 = self.load("Pics/Sprite/slime2left3.png")

        # Up Animation
        self.up1 = self.load("Pics/Sprite/slime2up1.png")
        self.up2 = self.load("Pics/Sprite/slime2up2.png")
        self.up3 = self.load("Pics/Sprite/slime2up3.png")

        # Down Animation
        self.down2 = self.load("Pics/Sprite/slime2down2.png")
        self.down3 = self.load("Pics/Sprite/slime2down3.png")

    def update(self):
        self.movekeys()
        self.animation()

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
            self.facing = "up"

        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            self.y_change += speed
            self.facing = "down"

        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.x_change -= speed
            self.facing = "left"

        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.x_change += speed
            self.facing = "right"

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
        right_ani = [self.right1,
                     self.right2,
                     self.right3]
        left_ani = [self.left1,
                    self.left2,
                    self.left3]
        up_ani = [self.up1,
                  self.up2,
                  self.up3]
        down_ani = [self.down1,
                    self.down2,
                    self.down3]

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.right1
            else:
                self.image = right_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1
                if self.ani_loop >= len(right_ani):
                    self.ani_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.left1
            else:
                self.image = left_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1
                if self.ani_loop >= len(left_ani):
                    self.ani_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.up1
            else:
                self.image = up_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1
                if self.ani_loop >= len(up_ani):
                    self.ani_loop = 1
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down1
            else:
                self.image = down_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1
                if self.ani_loop >= len(down_ani):
                    self.ani_loop = 1

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

    def get_one(self, x, y, width, height):
        terrain = pygame.Surface([width, height])
        terrain.blit(self.sheet, (0,0), (x, y, width, height))
        terrain.set_colorkey(BLACK)
        return terrain
import pygame
from sprites import *
from config import *
import sys


class Gameplay:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("pokefont.ttf", 32)
        self.running = True
        self.playing = False

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()


    def new(self):
        self.playing = True
        self.all_sprites.empty()
        self.blocks.empty()

    def update(self):

    def draw(self):

    def main(self):

    def game_over(self):

    def intro(self):


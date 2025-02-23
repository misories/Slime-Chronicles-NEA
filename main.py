import pygame.mixer

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
        self.player = None

        pygame.mixer.init()
        self.music = pygame.mixer.music

    def createwallmap(self):
        for n, row in enumerate(wallmap):
            for m, column in enumerate(row):
                if column == "X":
                    Walls(self, m, n)
                if column == "P":
                    Player(self, m, n)

    def new(self):
        self.playing = True
        self.all_sprites.empty()
        self.blocks.empty()

        self.createwallmap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def mainloop(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def game_over(self):
        pass

    def intro(self):
        pass

    def playmusic(self):
        self.music.load("heart and soul.mp3")
        self.music.play(-1)
        self.music.set_volume(0.2)

g = Gameplay()
g.intro()
g.new()
g.playmusic()
while g.running:
    g.mainloop()
    g.game_over()
pygame.quit()
sys.exit()
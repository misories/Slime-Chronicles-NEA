import pygame.mixer
from requests.utils import select_proxy

from sprites import *
from config import *
import sys
from groups import *


class Gameplay:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
        pygame.display.set_caption("Slime Chronicles")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("pokefont.ttf", 32)
        self.running = True
        self.playing = False

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.player = None
        self.npc = None
        self.camera = None
        self.menu = MenuFrame(self)

        self.terrain = Spritesheet("Pics/Sprite/terrain.png")

        pygame.mixer.init()
        self.music = pygame.mixer.music

    def createwallmap(self):
        for n, row in enumerate(wallmap):
            for m, column in enumerate(row):
                Ground(self, m, n)
                if column == "X":
                    Walls(self, m, n)
                if column == "P":
                    self.player = Player(self, m, n)
                if column == "N":
                    self.npc = NPC(self, m, n)

    def new(self):
        self.playing = True
        self.all_sprites.empty()
        self.blocks.empty()

        self.createwallmap()
        print(f"player: {self.player.rect.x}, {self.player.rect.y}")
        self.camera = Camera(world_w, world_h, self.player.rect.x, self.player.rect.y)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.player.rect.colliderect(self.npc.rect):
                        self.npc.interact()
        if self.menu.pause:
            self.menu = MenuFrame(self, 0,0)

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.clock.tick(FPS)
        pygame.display.flip()

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
        self.music.set_volume(0.5)

g = Gameplay()
g.intro()
g.new()
g.playmusic()
while g.running:
    g.mainloop()
    g.game_over()
pygame.quit()
sys.exit()
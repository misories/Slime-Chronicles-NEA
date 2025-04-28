import pygame.mixer
from requests.utils import select_proxy

from sprites import *
from config import *
import sys

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
        self.show_dialogue = False
        self.dialogue_text = ""

        self.pause = False

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

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.player.rect.colliderect(self.npc.rect):
                        self.npc.interact()
                if event.key == pygame.K_e:
                    pass
                if self.show_dialogue and event.key == pygame.K_SPACE:
                    self.show_dialogue = False


    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            if isinstance(sprite, NPC):
                self.screen.blit(sprite.name_surface, sprite.name_rect)
        if self.show_dialogue:
            textbox_rect = pygame.Rect(50, 500, 860, 120)
            pygame.draw.rect(self.screen, (50, 50, 50), textbox_rect)
            pygame.draw.rect(self.screen, WHITE, textbox_rect, 3)

            font = pygame.font.Font("pokefont.ttf", 24)
            text_surface = font.render(self.dialogue_text, True, WHITE)
            self.screen.blit(text_surface, (textbox_rect.x + 10, textbox_rect.y + 10))
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
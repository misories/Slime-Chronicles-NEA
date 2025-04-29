import math

import pygame.mixer
from requests.utils import select_proxy

from sprites import *
from config import *
import sys


def interact_R(player, npc, radius=75):
    dx = player.rect.centerx - npc.rect.centerx
    dy = player.rect.centery - npc.rect.centery
    distance = math.hypot(dx, dy)
    return distance <= radius

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
        self.npcs = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.player = None
        self.npc = None
        self.camera = None
        self.show_dialogue = False
        self.dialogue_text = ""
        self.dialogue_index = 0
        self.choice_list = []
        self.selected_index = 0
        self.showing_choices = False

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
                    for npc in self.npcs:
                        if interact_R(self.player, npc):
                            npc.interact()
                            break

            if self.show_dialogue:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.show_dialogue = False

            if self.showing_choices:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.choice_list)
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.choice_list)
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        _, func = self.choice_list[self.selected_index]
                        func()
                        self.showing_choices = False

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
            pygame.draw.rect(self.screen, WHITE, textbox_rect, 2)

            font = pygame.font.Font("pokefont.ttf", 16)
            text_surface = font.render(self.dialogue_text, True, WHITE)
            self.screen.blit(text_surface, (textbox_rect.x + 10, textbox_rect.y + 10))

        if self.showing_choices:
            textbox_rect = pygame.Rect(50, 500, 860, 120)
            pygame.draw.rect(self.screen, (50, 50, 50), textbox_rect)
            pygame.draw.rect(self.screen, WHITE, textbox_rect, 2)

            font = pygame.font.Font("pokefont.ttf", 16)
            for idx, (text, func) in enumerate(self.choice_list):
                colour = WHITE
                if idx == self.selected_index:
                    colour = (255, 255, 0)

            text_surface = font.render(self.dialogue_text, True, WHITE)
            self.screen.blit(text_surface, (textbox_rect.x + 20, textbox_rect.y + 20 + idx * 30))
        self.clock.tick(FPS)
        pygame.display.flip()

    def show_choices(self, choices):
        self.choice_list = choices
        self.selected_index = 0
        self.showing_choices = True

    def end_convo(self):
        self.dialogue_text = ["'And stay down...' he mumbled."]
        self.dialogue_index = 0
        self.show_dialogue = True
        self.showing_choices = False

    def mainloop(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def intro(self):
        pass

    def battle(self):
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
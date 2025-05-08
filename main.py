import math

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
        self.state = "game"

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.player = None
        self.npc = None
        self.camera = None
        self.show_dialogue = False
        self.dialogue_text = ""
        self.dialogue_choices = []
        self.choice_index = 0
        self.in_choice_mode = False

        self.pause = False

        self.terrain = Spritesheet("Pics/Sprite/terrain.png")

        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.song_list = ["meow.mp3", "heart and soul.mp3"]
        self.sound = self.song_list[0] #Deafult Song
        self.v = 0.5 #Deafult Value

        self.battle_run = False

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
                if event.key == pygame.K_e and self.state == "game":
                    for npc in self.npcs:
                        if interact_R(self.player, npc):
                            npc.interact()
                            break

            if self.show_dialogue:
                if event.type == pygame.KEYDOWN:
                    if self.in_choice_mode:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.choice_index = ((self.choice_index - 1) % len(self.dialogue_choices))
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.choice_index = ((self.choice_index + 1) % len(self.dialogue_choices))
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            self.select_choice()
                    else:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            self.show_dialogue = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.state == "game":
                    self.state = "settings"
                else:
                    self.state = "game"

    def select_choice(self):
        selected = self.dialogue_choices[self.choice_index]
        print(f"You selected: {selected}")
        if selected == "Y":
            self.dialogue_text = "Stand ready..."
        elif selected == "N":
            self.dialogue_text = "You aren't ready for its arrival.\n Not yet..."
        self.in_choice_mode = False

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

            font = pygame.font.Font("pokefont.ttf", 12)

            if self.in_choice_mode:
                question_surface = font.render(self.dialogue_text, True, WHITE)
                self.screen.blit(question_surface, (textbox_rect.x + 10, textbox_rect.y + 10))

                for i, choice in enumerate(self.dialogue_choices):
                    colour = (255, 255, 0) if i == self.choice_index else WHITE
                    choice_surface = font.render(choice, True, colour)
                    self.screen.blit(choice_surface, (textbox_rect.x + 20, textbox_rect.y + 40 + i * 30))
            else:
                text_surface = font.render(self.dialogue_text, True, WHITE)
                self.screen.blit(text_surface, (textbox_rect.x + 10, textbox_rect.y + 10))

        if self.battle_run:
            self.screen.blit(battleimg, (0,0))
        if self.state == "game":
            pass
        elif self.state == "settings":
            s.update()
            s.draw(self.screen)
            action = s.event()
            if action == "+1":
                self.v = self.v + 0.1
                if self.v > 1:
                    self.v = 1
            if action == "-1":
                self.v = self.v - 0.1
                if self.v < 0:
                    self.v = 0
            self.music.set_volume(self.v)
            pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.flip()

    def mainloop(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def intro(self):
        pass

    def battle(self):
        battleimg = pygame.image.load("Pics/battle.png").convert_alpha()
        pass



    def playmusic(self):
        self.music.load("meow.mp3")
        self.music.play(-1)
        self.music.set_volume(self.v)

class SettingsMenu:
    def __init__(self, screen):
        self.tfont = pygame.font.Font("pokefont.ttf", 39)
        self.font = pygame.font.Font("pokefont.ttf", 16)
        self.screen = None
        self.page = pygame.image.load("Pics/page.png").convert_alpha()
        self.page = pygame.transform.scale(self.page, (960, 640))
        self.vol = 5

        self.btn_font = pygame.font.Font("pokefont.ttf", 18)
        self.rects = pygame.image.load("Pics/rect.png")
        self.rects = pygame.transform.scale(self.rects, (30,30))
        self.volbtn1 = Button(image=self.rects, pos=(200, 300), text_input="+", font=self.btn_font, base_color=WHITE, hovering_color=YELLOW)
        self.volbtn2 = Button(image=self.rects, pos=(100, 300), text_input="-", font=self.btn_font, base_color=WHITE, hovering_color=YELLOW)

        self.rectm = pygame.image.load("Pics/rect.png")
        self.rectm = pygame.transform.scale(self.rectm, (90,40))


    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.volbtn1.changeColor(mouse_pos)
        self.volbtn2.changeColor(mouse_pos)
        self.sound1.changeColor(mouse_pos)

    def draw(self, screen):
        self.screen = screen
        self.screen.fill(RED)
        self.screen.blit(self.page, (0,0))
        title = self.tfont.render("--- Settings ---", True, WHITE)
        v_txt = self.font.render("Volume", True, WHITE)
        v = self.font.render(str(self.vol), True, WHITE)
        s_txt = self.font.render("Sounds", True, WHITE)

        self.screen.blit(v, (140,300))
        self.screen.blit(v_txt, (100, 260))
        self.screen.blit(s_txt, (100, 360))
        self.screen.blit(title, (160,80))

        self.volbtn1.update(self.screen)
        self.volbtn2.update(self.screen)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.volbtn1.checkForInput(pygame.mouse.get_pos()):
                    self.vol = self.vol + 1
                    if self.vol > 10:
                        self.vol = 10
                    return "+1"
                if self.volbtn2.checkForInput(pygame.mouse.get_pos()):
                    self.vol = self.vol - 1
                    if self.vol < 0:
                        self.vol = 0
                    return "-1"
        return None

g = Gameplay()
s = SettingsMenu(g.screen)
g.intro()
g.new()
g.playmusic()
while g.running:
    g.mainloop()
pygame.quit()
sys.exit()
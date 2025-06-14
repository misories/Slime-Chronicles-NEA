import sys

import pygame

from config import *
from battlesprite import *
from sprites import *

from random import sample

class Battle:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen # Using the game screen
        self.battle = True # State Checker
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group() # Sprite Group

        self.import_assets()

        # Slime Data
        monster_list = ["blue", "red"] # List of sprites
        self.player_monster = [Monster(name, self.back_surfs[name]) for name in monster_list] # Creating the player
        self.monster = self.player_monster[0]
        self.sprites.add(self.monster) # adding to group
        opponent_name = "green"
        self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.sprites) # Creating NPC1 opponent
        self.sprites.add(self.opponent)

        # Transforming sizes
        self.background["bg"] = pygame.transform.scale(self.background["bg"], (960, 640))
        self.background["floor"] = pygame.transform.scale(self.background["floor"], (300, 100))

        # Battle UI
        self.ui = BattleUI(self.monster, self.battle, monster_list)

    def import_assets(self):
        self.back_surfs = folder_importer("Pics","battle","back") # importing back surfaces
        self.front_surfs = folder_importer("Pics", "battle", "front")  # importing front surfaces
        self.background = folder_importer("Pics","battle","extra") # importing extra images

    def set_floor(self):
        for sprite in self.sprites:
            floor_rect = self.background["floor"].get_rect(center = sprite.rect.midbottom + pygame.Vector2(0, -30))
            self.screen.blit(self.background["floor"], floor_rect)

    def update(self):
        self.sprites.update()

    def handle_events(self, events):
        self.ui.handle_events(events)

    def draw(self):
        if self.battle:
            self.screen.blit(self.background["bg"], (0,0)) # displaying background
            self.set_floor()
            self.sprites.draw(self.screen)
            self.ui.draw()
            pygame.display.update()
            self.clock.tick(FPS)


class BattleUI:
    def __init__(self, player, state, player_monsters):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        self.left = w / 2 - 100
        self.top = h / 2 + 50
        self.rows = 2
        self.columns = 2

        self.player = player
        self.state = state

        self.user_options = ["Fight","Items","Switch","Forfeit"]
        self.user_selection = {"column": 0, "row": 0}
        self.attack_selection = {"column": 0, "row": 0}
        self.switch_index = 0
        self.menu_state = "main"
        self.visible_monsters = 4
        self.player_monsters = player_monsters
        self.avaliable_monsters = [player for player in self.player_monsters if player != self.player]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.menu_state == "main" and self.state:
                    if event.key == pygame.K_DOWN:
                        self.user_selection["row"] = (self.user_selection["row"] + 1) % self.rows
                    if event.key == pygame.K_UP:
                        self.user_selection["row"] = (self.user_selection["row"] - 1) % self.rows
                    if event.key == pygame.K_RIGHT:
                        self.user_selection["column"] = (self.user_selection["column"] + 1) % self.columns
                    if event.key == pygame.K_LEFT:
                        self.user_selection["column"] = (self.user_selection["column"] - 1) % self.columns
                    if event.key == pygame.K_RETURN:
                        idx = self.user_selection["column"] + self.user_selection["row"] * 2
                        self.menu_state = self.user_options[idx]
                elif self.menu_state == "Fight" and self.state:
                    if event.key == pygame.K_DOWN:
                        self.attack_selection["row"] = (self.attack_selection["row"] + 1) % self.rows
                    if event.key == pygame.K_UP:
                        self.attack_selection["row"] = (self.attack_selection["row"] - 1) % self.rows
                    if event.key == pygame.K_RIGHT:
                        self.attack_selection["column"] = (self.attack_selection["column"] + 1) % self.columns
                    if event.key == pygame.K_LEFT:
                        self.attack_selection["column"] = (self.attack_selection["column"] - 1) % self.columns
                    if event.key == pygame.K_RETURN:
                        idx = self.attack_selection["column"] + self.attack_selection["row"] * 2
                        print(self.player.moves[idx])
                elif self.menu_state == "Switch" and self.state:
                    if event.key == pygame.K_DOWN:
                        self.switch_index = (self.switch_index + 1) % len(self.avaliable_monsters)
                    if event.key == pygame.K_UP:
                        self.switch_index = (self.switch_index - 1) % len(self.avaliable_monsters)

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def selectGUI(self, index, moves):
        rect = pygame.Rect(self.left + 40, self.top + 60, 400, 200)
        pygame.draw.rect(self.screen, WHITE, rect, 0, 4)
        pygame.draw.rect(self.screen, GRAY, rect, 4, 4)

        for column in range(self.columns):
            for row in range(self.rows):
                i = column + 2 * row
                if i >= len(moves):
                    continue

                x = rect.left + rect.width / 4 + (rect.width / 2) * column
                y = rect.top + rect.height / 4 + (rect.height / 2) * row

                colour = RED if column == index["column"] and row == index["row"] else BLACK
                option_surf = self.font.render(moves[i], True, colour)
                option_rect =  option_surf.get_rect()
                option_rect.center = (x, y)

                self.screen.blit(option_surf, option_rect)

    def switch(self):
        # BG
        rect = pygame.Rect(self.left + 40, self.top - 100, 400, 400)
        pygame.draw.rect(self.screen, WHITE, rect, 0, 4)
        pygame.draw.rect(self.screen, GRAY, rect, 4, 4)

        # Switch Menu
        for i in range(len(self.avaliable_monsters)):
            x = rect.centerx
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i

            name = self.avaliable_monsters[i].capitalize()
            colour = RED if i == self.switch_index else BLACK
            text_surf = self.font.render(name, True, colour)
            text_rect = text_surf.get_rect(center = (x,y))
            self.screen.blit(text_surf, text_rect)

    def draw(self):
        match self.menu_state:
            case "main": self.selectGUI(self.user_selection, self.user_options)
            case "Switch": self.switch()
            case "Forfeit": self.state = False
import pygame
from config import *

class Slime:
    def get_data(self, name, moves):
        # Inputting Data

        self.type = SLIME_DATA[name]["type"]
        self.speed = SLIME_DATA[name]["speed"]
        self.hp = self.max_hp = SLIME_DATA[name]["hp"]
        self.moves = moves
        for move, move_data in MOVESET.items():
            if move_data["type"] == "normal":
                self.moves.append(move)
        self.name = name
        print(self.name,self.type, self.speed, self.hp, self.moves)
        return self.moves

class Monster(pygame.sprite.Sprite, Slime):
    def __init__(self, name, surf):
        super().__init__()
        self.image = surf # front/back sprite image
        self.rect = self.image.get_rect(bottomleft = (100, h)) # setting in the bottom left of the screen
        self.name = name
        self.moves = ["Scald"]
        self.get_data(name, self.moves)

class Opponent(pygame.sprite.Sprite, Slime):
    def __init__(self, name, surf, groups):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(midbottom = (w - 250, 300))
        self.moves = ["Root"]
        self.get_data(name, self.moves)
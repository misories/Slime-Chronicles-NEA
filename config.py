import pygame

from os import walk
from os.path import join

w = 960
h = 640

P_layer = 3
W_layer = 2
G_layer = 1

pixels = 32
RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
GRAY = (105,105,105)


FPS = 60
speed = 2

wallmap = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X...................................................................................................X",
    "X...................................................................................................X",
    "X.........P........N................................................................................X",
    "X...................................................................................................X",
    "X........XXXX...............................................................................X..X....X",
    "X...................................................................................................X",
    "X...................................................................................................X",
    "X...................................................................................................X",
    "X...................................................................................................X",
    "X...................................................................................................X",
    "X...................................................................................................X",
    "X.....XXXX.....XXX..................................................................................X",
    "X......XXX......XXXXXXXXX...........................................................................X",
    "X.......XX.......XXXXXXXX...........................................................................X",
    "X.......XX.............XX...........................................................................X",
    "X.......XX.............XX...........................................................................X",
    "X.......XXXXXXXXXXXXXXXXX...........................................................................X",
    "X...................................................................................................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

world_w = (101 + 1) * pixels
world_h = (19 + 1) * pixels

COPPER = (184, 115, 51)

health = 20

SLIME_DATA= {
    "blue": {"type": "water", "hp": health, "speed": 3},
    "green": {"type": "nature", "hp": health, "speed": 2},
    "red": {"type": "fire", "hp": health, "speed": 4}
}

MOVESET = {
    "Rush": {"dmg": 4, "type": "normal", "uses": 15},
    "Root": {"heal": 2, "type": "nature", "uses": 5},
    "Scald": {"dmg": 3, "type": "water", "uses": 20},
    "Stretch": {"speed": +0.5, "type": "normal", "uses": 5},
    "Fireball": {"dmg": 3,"type": "fire", "uses": 15}

}

TYPE_DATA = {
    "normal": {"normal": 1, "water": 1, "nature": 1, "fire": 1},
    "nature": {"normal": 1, "water": 2, "nature": 1, "fire": 0.5},
    "water": {"normal": 1, "water": 1, "nature": 0.5, "fire": 2},
    "fire": {"normal": 1, "water": 0.5, "nature": 2, "fire": 1}
}

def folder_importer(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
            for image in surfs:
                surfs[image] = pygame.transform.scale(surfs[image], (100,100))
    return surfs
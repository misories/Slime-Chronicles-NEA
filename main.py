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

g = Gameplay()
g.intro()
g.new()
while g.running:
    g.mainloop()
    g.game_over()
pygame.quit()
sys.exit()
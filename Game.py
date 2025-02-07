import pygame

pygame.innit()

w = 900
h = 550
game = True

window = pygame.display.set_mode((w,h))

while game:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            game = False

pygame.quit()
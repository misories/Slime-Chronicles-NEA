import pygame.sprite
from config import *

class BreadTasteBetterThanKey(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def upd_offset(self, target_pos):
        self.offset.x = -(target_pos[0] - w / 2)
        self.offset.y = -(target_pos[1] - h / 2)

    def draw(self, surface):
        super().draw(surface)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            surface.blit(sprite.image, offset_pos)
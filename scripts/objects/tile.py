
import pygame

from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, grupos, pos, imagem=pygame.Surface((16, 16))):
        super().__init__(grupos)
        self.image = imagem
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(0, 0)

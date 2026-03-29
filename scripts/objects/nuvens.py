
from ..constants import LARGURA, ALTURA

from pygame.sprite import Sprite
from pygame.math import Vector2


class Nuvem(Sprite):
    def __init__(self, grupo, img, pos, velocidade, margem) -> None:
        super().__init__(grupo)
        self.pos = Vector2(pos)
        self.image = img
        self.rect = self.image.get_rect(topleft=self.pos)

        self.vel = velocidade
        self.margem = margem

    def update(self, dt, deslocamento=(0, 0)) -> None:
        self.pos.x += self.vel * 100 * dt

        pos_x = (self.pos.x - deslocamento[0] * self.margem)
        pos_y = (self.pos.y - deslocamento[1] * self.margem)

        self.rect.x = pos_x % (LARGURA + self.rect.width) - self.rect.width
        self.rect.y = pos_y % (ALTURA + self.rect.height) - self.rect.height
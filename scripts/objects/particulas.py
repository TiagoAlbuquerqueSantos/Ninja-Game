
import pygame

from random import random, randint
from pygame.sprite import Sprite
from pygame.math import Vector2
from math import sin

from scripts.utils import Animacao


class Particula(Sprite):
    def __init__(self, grupos, anim: Animacao, pos: tuple, velocidade: tuple, frame: int) -> None:
        super().__init__(grupos)
        self.pos = Vector2(pos)
        self.velocidade = velocidade

        self.anim = anim.copia()
        self.anim.frame = frame

        self.image = self.anim.imagem()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, deslocamento=(0, 0)) -> None:
        self.anim.atualizar()

        if self.anim.concluido:
            self.kill()

        self.pos.x += self.velocidade[0]
        self.pos.y += self.velocidade[1]

        self.rect.topleft = (self.pos.x - deslocamento[0] - self.rect.width // 2,
                             self.pos.y - deslocamento[1] - self.rect.height // 2)
        self.image = self.anim.imagem()

#TODO: Implementar essa classe futuramente
class ParticulaFolha(Particula):
    def __init__(self, grupos, anim: Animacao, pos: tuple, velocidade: tuple, frame: int) -> None:
        super().__init__(grupos, anim, pos, velocidade, frame)

    def update(self, deslocamento=(0, 0)) -> None:
        super().update(deslocamento)
        self.pos.x += sin(self.anim.frame * 0.035) * 0.3


class GeradorFolhas:
    def __init__(self, game) -> None:
        self.game = game
        self.geradores = []

    def carregar_geradores(self, mapa_jogo) -> None:
        """Carrega os retângulos das árvores a partir do mapa"""
        self.geradores = []
        for arvore in mapa_jogo.extrair([('decor_larga', 2)], manter=True):
            self.geradores.append(pygame.Rect(
                4 + arvore['pos'][0], 4 + arvore['pos'][1], 23, 13))

    def atualizar(self) -> None:
        """Gera novas partículas de folhas aleatoriamente"""
        for rect in self.geradores:
            if random() * 49999 < rect.width * rect.height:
                Particula(
                    grupos=self.game.particulas,
                    anim=self.game.assets['folhas'],
                    pos=(rect.x + random() * rect.width, rect.y + random() * rect.height),
                    velocidade=(-0.1, 0.3),
                    frame=randint(0, 20))

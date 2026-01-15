import pygame

from scripts.constants import *


class HUD:
    def __init__(self, game):
        self.game = game

        self.barra_vida = BarraVida((LARGURA / 2 - 50, 5), (100, 10), 100)

    def atualizar(self):
        pass

    def renderizar(self, display):
        self.barra_vida.renderizar(display)


class BarraVida:
    def __init__(self, pos, tamanho, hp_max):
        self.pos = pos

        self.surf = pygame.Surface(tamanho)

        self.hp_max = hp_max
        self.hp_atual = hp_max

    def levar_dano(self, quantidade):
        self.hp_atual = max(0, self.hp_atual - quantidade)

    def curar(self, quantidade):
        self.hp_atual = min(self.hp_max, self.hp_atual + quantidade)

    def renderizar(self, surf):
        proporcao = self.hp_atual / self.hp_max
        cor_hp = VERDE if proporcao > 0.4 else VERMELHO

        rect_fundo = pygame.Rect(0, 0, self.surf.get_width(), self.surf.get_height())
        rect_vida = pygame.Rect(0, 0, self.surf.get_width() * proporcao, self.surf.get_height())

        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, cor_hp, rect_vida)
        pygame.draw.rect(self.surf, PRETO, rect_fundo, 1)
        surf.blit(self.surf, self.pos)

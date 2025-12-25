
import pygame

from scripts.constants import *


class Circulo:
    def __init__(self):
        self.estado = -RAIO_TRANSICAO

    def atualizar(self):
        if self.estado < 0:
            self.estado += 1

    def ativar(self):
        self.estado += 1

    def finalizada(self):
        return self.estado > RAIO_TRANSICAO

    def resetar(self):
        self.estado = -RAIO_TRANSICAO

    def renderizar(self, display):
        if self.estado != 0:
            surf_transicao = pygame.Surface(display.get_size())
            pygame.draw.circle(surf_transicao, BRANCO, CENTRO_TELA, (RAIO_TRANSICAO - abs(self.estado)) * 8)
            surf_transicao.set_colorkey(BRANCO)
            display.blit(surf_transicao, (0, 0))

    @property
    def ativo(self):
        return self.estado != 0

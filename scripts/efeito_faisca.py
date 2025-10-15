import math

import pygame

class Faisca:
    def __init__(self, pos, angulo, velocidade):
        self.pos = list(pos)
        self.angulo = angulo
        self.velocidade = velocidade

    def atualizar(self):
        self.pos[0] += math.cos(self.angulo) * self.velocidade
        self.pos[1] += math.sin(self.angulo) * self.velocidade

        self.velocidade = max(0, self.velocidade - 0.1)
        return not self.velocidade

    def renderizar(self, surf, deslocamento=(0, 0)):
        pontos_renderizacao = [
            (self.pos[0] + math.cos(self.angulo) * self.velocidade * 3 - deslocamento[0],
             self.pos[1] + math.sin(self.angulo) * self.velocidade * 3 - deslocamento[1]),

            (self.pos[0] + math.cos(self.angulo + math.pi * 0.5) * self.velocidade * 0.5 - deslocamento[0],
             self.pos[1] + math.sin(self.angulo + math.pi * 0.5) * self.velocidade * 0.5 - deslocamento[1]),

            (self.pos[0] + math.cos(self.angulo + math.pi) * self.velocidade * 3 - deslocamento[0],
             self.pos[1] + math.sin(self.angulo + math.pi) * self.velocidade * 3 - deslocamento[1]),

            (self.pos[0] + math.cos(self.angulo - math.pi * 0.5) * self.velocidade * 0.5 - deslocamento[0],
             self.pos[1] + math.sin(self.angulo - math.pi * 0.5) * self.velocidade * 0.5 - deslocamento[1]),
        ]

        pygame.draw.polygon(surf, (255, 255, 255), pontos_renderizacao)

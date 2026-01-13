
import pygame

from random import randint
from random import random


class Particula:
    def __init__(self, main, tipo_p, pos, velocidade=(0, 0), frame=0):
        self.main = main
        self.tipo = tipo_p
        self.pos = list(pos)
        self.velocidade = list(velocidade)
        self.animacao = self.main.assets['particulas/' + tipo_p].copia()
        self.animacao.frame = frame

    def atualizar(self):
        interromper = False
        if self.animacao.concluido:
            interromper = True

        self.pos[0] += self.velocidade[0]
        self.pos[1] += self.velocidade[1]

        self.animacao.atualizar()

        return interromper

    def renderizar(self, surf, deslocamento=(0, 0)):
        imagem = self.animacao.imagem()
        surf.blit(imagem, (self.pos[0] - deslocamento[0] - imagem.get_width() // 2,
                           self.pos[1] - deslocamento[1] - imagem.get_height() // 2))


class GeradorFolhas:
    def __init__(self, game):
        self.game = game
        self.geradores = []

    def carregar_geradores(self, mapa_jogo):
        """Carrega os retângulos das árvores a partir do mapa"""
        self.geradores = []
        for arvore in mapa_jogo.extrair([('decor_larga', 2)], manter=True):
            self.geradores.append(pygame.Rect(
                4 + arvore['pos'][0], 4 + arvore['pos'][1], 23, 13))

    def atualizar(self):
        """Gera novas partículas de folhas aleatoriamente"""
        for rect in self.geradores:
            if random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random() * rect.width,
                       rect.y + random() * rect.height)
                self.game.particulas.append(
                    Particula(self.game, 'folhas', pos, velocidade=[-0.1, 0.3], frame=randint(0, 20)))

    def resetar(self):
        """Reseta os geradores"""
        self.geradores = []

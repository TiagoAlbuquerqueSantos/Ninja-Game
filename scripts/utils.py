import os
import pygame

BASE_LOCAL_IMG = './data/images/'

def carregar_imagem(caminho):
    imagem = pygame.image.load(BASE_LOCAL_IMG + caminho).convert()
    imagem.set_colorkey((0, 0, 0))
    return imagem

def carregar_imagens(caminho):
    imagems = []
    for nome_img in sorted(os.listdir(BASE_LOCAL_IMG + caminho)):
        imagems.append(carregar_imagem(caminho + '/' + nome_img))
    return imagems

class Animacao:
    def __init__(self, imagens, dur_img=5, loop=True):
        self.imagens = imagens
        self.loop = loop
        self.duracao_img = dur_img
        self.concluido = False
        self.frame = 0

    def copia(self):
        return Animacao(self.imagens, self.duracao_img, self.loop)

    def atualizar(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.duracao_img * len(self.imagens))
        else:
            self.frame = min(self.frame + 1, self.duracao_img * len(self.imagens) - 1)
            if self.frame >= self.duracao_img * len(self.imagens) - 1:
                self.concluido = True

    def imagem(self):
        return self.imagens[int(self.frame / self.duracao_img)]
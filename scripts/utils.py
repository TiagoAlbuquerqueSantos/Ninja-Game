import os
import pygame

from .paths import IMG_ASSETS

def carregar_imagem(caminho):
    imagem = pygame.image.load(IMG_ASSETS / caminho).convert()
    imagem.set_colorkey((0, 0, 0))
    return imagem

def carregar_imagens(caminho):
    imagems = []
    for nome_img in sorted(os.listdir(IMG_ASSETS / caminho)):
        imagems.append(carregar_imagem(caminho + '/' + nome_img))
    return imagems

def aplicar_contornos(surf, mascara_surf):
    mascara_display = pygame.mask.from_surface(mascara_surf)
    silueta_display = mascara_display.to_surface(
        setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
    for deslocamento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        surf.blit(silueta_display, deslocamento)


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
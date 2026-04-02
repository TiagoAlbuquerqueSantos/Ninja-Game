
import pygame
from os import listdir

from ..paths import IMG_ASSETS

def carregar_imagem(caminho, escala=None) -> pygame.Surface:
    img = pygame.image.load(IMG_ASSETS / caminho).convert()
    img.set_colorkey((0, 0, 0))
    if escala is not None:
        img = pygame.transform.scale(img, escala)
    return img

def carregar_imagens(caminho) -> list:
    imagems = []
    for nome_img in sorted(listdir(IMG_ASSETS / caminho)):
        imagems.append(carregar_imagem(caminho + '/' + nome_img))
    return imagems

def aplicar_contornos(surf, mascara_surf) -> None:
    mascara_display = pygame.mask.from_surface(mascara_surf)
    silueta_display = mascara_display.to_surface(
        setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
    for deslocamento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        surf.blit(silueta_display, deslocamento)
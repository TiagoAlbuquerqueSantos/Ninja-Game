import os
import sys
import math
import random

import pygame

from scripts.utils import carregar_imagem, carregar_imagens, Animacao
from scripts.entidades import Jogador, Inimigo
from scripts.efeito_faisca import Faisca
from scripts.particulas import Particula
from scripts.tilemap import Tilemap
from scripts.nuvens import Nuvens
from scripts.configuracoes import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(LEGENDA)
        flags = pygame.RESIZABLE | pygame.SCALED
        self.tela = pygame.display.set_mode(RESOLUCAO_TELA, flags=flags)
        self.display = pygame.Surface(RES_DISPLAY, pygame.SRCALPHA)
        self.display_2 = pygame.Surface(RES_DISPLAY)
        self.relogio = pygame.time.Clock()

        self.camera = None
        self.scroll = None
        self.faiscas = None
        self.inimigos = None
        self.derrotado = None
        self.projeteis = None
        self.transicao = None
        self.particulas = None
        self.gerador_folhas = None

        self.movimento = [False, False]

        self.assets = {
            'decor': carregar_imagens('tiles/decor'),
            'grama': carregar_imagens('tiles/grass'),
            'decor_larga': carregar_imagens('tiles/large_decor'),
            'pedra': carregar_imagens('tiles/stone'),
            'nuvens': carregar_imagens('clouds'),
            'inimigo/idle': Animacao(carregar_imagens('entities/enemy/idle'), dur_img=6),
            'inimigo/run': Animacao(carregar_imagens('entities/enemy/run'), dur_img=4),
            'jogador/idle': Animacao(carregar_imagens('entities/player/idle'), dur_img=6),
            'jogador/run': Animacao(carregar_imagens('entities/player/run'), dur_img=4),
            'jogador/pulo': Animacao(carregar_imagens('entities/player/jump')),
            'jogador/deslize': Animacao(carregar_imagens('entities/player/slide')),
            'jogador/deslize_parede': Animacao(carregar_imagens('entities/player/wall_slide')),
            'particulas/folhas': Animacao(carregar_imagens('particles/leaf'), dur_img=20, loop=False),
            'particulas/particula': Animacao(carregar_imagens('particles/particle'), dur_img=6, loop=False),
            'pistola': carregar_imagem('gun.png'),
            'projetil': carregar_imagem('projectile.png'),
            'plano_fundo': carregar_imagem('background.png'),
        }

        self.sfx = {
            'pulo': pygame.mixer.Sound('data/sfx/jump.wav'),
            'repulsao': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'tiro': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambiente': pygame.mixer.Sound('data/sfx/ambience.wav')
        }

        self.sfx['ambiente'].set_volume(0.2)
        self.sfx['tiro'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['repulsao'].set_volume(0.3)
        self.sfx['pulo'].set_volume(0.7)

        self.nuvens = Nuvens(self.assets['nuvens'], quant=NUM_NUVENS)

        self.jogador = Jogador(self, POSICAO, HIT_BOX)

        self.mapa_jogo = Tilemap(self, tamanho_tile=TILE_SIZE)

        self.nivel = LEVEL
        self.carregar_nivel(self.nivel)

        self.balanco_imagem = 0

    def carregar_nivel(self, id_mapa):
        self.mapa_jogo.carregar('data/maps/' + str(id_mapa) + '.json')

        self.gerador_folhas = []
        for arvore in self.mapa_jogo.extrair([('decor_larga', 2)], manter=True):
            self.gerador_folhas.append(pygame.Rect(
                4 + arvore['pos'][0], 4 + arvore['pos'][1], 23, 13))

        self.inimigos = []
        for gerador in self.mapa_jogo.extrair([('geradores', 0), ('geradores', 1)]):
            if gerador['variante'] == 0:
                self.jogador.pos = gerador['pos']
                self.jogador.tempo_ar = 0
            else:
                self.inimigos.append(Inimigo(self, gerador['pos'], (8, 15)))

        self.projeteis = []
        self.particulas = []
        self.faiscas = []

        self.scroll = [0, 0]
        self.derrotado = 0
        self.transicao = -30

    def desenhar_texto(self, texto, cor, pos):
        obj_texto = self.font_style.render(str(texto), False, cor)
        rect_texto = obj_texto.get_rect(topleft=(pos[0], pos[1]))
        self.display.blit(obj_texto, rect_texto)

    def atualizar_folhas(self):
        for rect in self.gerador_folhas:
            if random.random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random.random() * rect.width,
                       rect.y + random.random() * rect.height)
                self.particulas.append(
                    Particula(self, 'folhas', pos, velocidade=[-0.1, 0.3], frame=random.randint(0, 20)))

    def renderizar_inimigos(self, surf, deslocamento):
        for inimigo in self.inimigos.copy():
            derrotar = inimigo.atualizar(self.mapa_jogo, (0, 0))
            inimigo.renderizar(surf, deslocamento)
            if derrotar:
                self.inimigos.remove(inimigo)

        self.particulas_faiscas_projeteis()

    def particulas_faiscas_projeteis(self):
        for projetil in self.projeteis.copy():
            projetil[0][0] += projetil[1]
            projetil[2] += 1
            img = self.assets['projetil']
            self.display.blit(img, (projetil[0][0] - img.get_width() / 2 - self.camera[0],
                                    projetil[0][1] - img.get_height() / 2 - self.camera[1]))
            if self.mapa_jogo.checar_solido(projetil[0]):
                self.projeteis.remove(projetil)
                for i in range(4):
                    self.faiscas.append(Faisca(projetil[0], random.random() - 0.5 + (math.pi if projetil[1] > 0 else 0),
                                               2 + random.random()))

            elif projetil[2] > 360:
                self.projeteis.remove(projetil)
            elif abs(self.jogador.repulsando) < 50:
                if self.jogador.retangulo().collidepoint(projetil[0]):
                    self.projeteis.remove(projetil)
                    self.derrotado += 1
                    self.sfx['hit'].play()
                    self.balanco_imagem = max(16, self.balanco_imagem)
                    for i in range(30):
                        angulo = random.random() * math.pi * 2
                        velocidade = random.random() * 5
                        self.faiscas.append(
                            Faisca(self.jogador.retangulo().center, angulo, 2 + random.random()))
                        self.particulas.append(Particula(self, 'particula', self.jogador.retangulo().center,
                                                         velocidade=[math.cos(angulo + math.pi) * velocidade * 0.5,
                                                                     math.sin(angulo + math.pi) * velocidade * 0.5],
                                                         frame=random.randint(0, 7)))

        for faisca in self.faiscas.copy():
            interromper = faisca.atualizar()
            faisca.renderizar(self.display, deslocamento=self.camera)
            if interromper:
                self.faiscas.remove(faisca)

        self.contornos()

        for particula in self.particulas.copy():
            interromper = particula.atualizar()
            particula.renderizar(self.display, deslocamento=self.camera)
            if particula.tipo == 'folhas':
                particula.pos[0] += math.sin(
                    particula.animacao.frame * 0.035) * 0.3
            if interromper:
                self.particulas.remove(particula)

    def verificar_derrota(self):
        if not len(self.inimigos):
            self.transicao += 1
            if self.transicao > 30:
                self.nivel = min(
                    self.nivel + 1, len(os.listdir('./data/maps')) - 1)
                self.carregar_nivel(self.nivel)
        if self.transicao < 0:
            self.transicao += 1

        if self.derrotado:
            self.derrotado += 1
            if self.derrotado >= 10:
                self.transicao = min(30, self.transicao + 1)
            if self.derrotado > 40:
                self.carregar_nivel(self.nivel)

    def musica_fundo(self):
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.sfx['ambiente'].play(-1)

    def contornos(self):
        mascara_display = pygame.mask.from_surface(self.display)
        silueta_display = mascara_display.to_surface(
            setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
        for deslocamento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.display_2.blit(silueta_display, deslocamento)

    def circulo_transicao(self):
        if self.transicao:
            surf_transicao = pygame.Surface(self.display.get_size())
            pygame.draw.circle(surf_transicao, (255, 255, 255),
                               (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transicao)) * 8)
            surf_transicao.set_colorkey((255, 255, 255))
            self.display.blit(surf_transicao, (0, 0))

    def movimento_camera(self):
        self.scroll[0] += (self.jogador.retangulo().centerx -
                           self.display.get_width() / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.jogador.retangulo().centery -
                           self.display.get_height() / 2 - self.scroll[1]) / 30
        self.camera = (int(self.scroll[0]), int(self.scroll[1]))

    def atualizar(self):
        self.verificar_derrota()
        self.movimento_camera()
        self.atualizar_folhas()
        self.nuvens.atualizar()
        if not self.derrotado:
            self.jogador.atualizar(
                self.mapa_jogo, (self.movimento[1] - self.movimento[0], 0))

    def renderizar(self):
        self.display.fill((0, 0, 0, 0))
        self.display_2.blit(self.assets['plano_fundo'], (0, 0))
        self.balanco_imagem = max(0, self.balanco_imagem - 1)
        self.nuvens.renderizar(self.display_2, deslocamento=self.camera)
        self.mapa_jogo.renderizar(self.display, deslocamento=self.camera)
        if not self.derrotado:
            self.jogador.renderizar(self.display, deslocamento=self.camera)
        self.renderizar_inimigos(self.display, deslocamento=self.camera)

        self.circulo_transicao()

        self.display_2.blit(self.display, (0, 0))

        balanco = (random.random() * self.balanco_imagem - self.balanco_imagem / 2,
                   random.random() * self.balanco_imagem - self.balanco_imagem / 2)

        self.tela.blit(pygame.transform.scale(
            self.display_2, self.tela.get_size()), balanco)

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                if evento.key == pygame.K_a:
                    self.movimento[0] = True
                if evento.key == pygame.K_d:
                    self.movimento[1] = True
                if evento.key == pygame.K_SPACE:
                    if self.jogador.pular():
                        self.sfx['pulo'].play()
                if evento.key == pygame.K_j:
                    self.jogador.repulsao()
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_a:
                    self.movimento[0] = False
                if evento.key == pygame.K_d:
                    self.movimento[1] = False

    def rodar(self):
        self.musica_fundo()
        while True:
            self.checar_eventos()
            self.atualizar()
            self.renderizar()
            pygame.display.update()
            self.relogio.tick(FPS)


if __name__ == '__main__':
    Game().rodar()


import pygame

from pygame.sprite import Group

from random import random, randint
from math import sin
from os import listdir
from sys import exit

from scripts.utils import carregar_imagem, carregar_imagens, aplicar_contornos, Animacao
from scripts.objects import Particula, Tilemap, Nuvens, Jogador, Inimigo
from scripts.soundmanager import SoundManager
from scripts.ui import Circulo, HUD
from scripts.debug import Debug
from scripts.constants import *
from scripts import paths


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(LEGENDA)
        flags = pygame.SCALED + pygame.RESIZABLE
        self.tela = pygame.display.set_mode(RES_TELA, flags=flags)
        self.display = pygame.Surface((DISPLAY_L, DISPLAY_A), pygame.SRCALPHA)
        self.display_2 = self.display.copy()
        self.relogio = pygame.time.Clock()

        self.hud = HUD(self)
        self.debug = Debug(self)
        self.transicao = Circulo()

        self.sprites = Group()
        self.projetil_sprite = Group()

        self.camera = None
        self.scroll = None
        self.faiscas = None
        self.inimigos = None
        self.derrotado = None
        self.particulas = None
        self.gerador_folhas = []

        self.rodando = True

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

        self.sounds = SoundManager(paths.SOUND_ASSETS)
        self.sounds.play_music('ambience')
        self.sounds.play_music('music')

        self.nuvens = Nuvens(self.assets['nuvens'], NUM_NUVENS)

        self.jogador = Jogador(self, POSICAO, HIT_BOX)

        self.mapa_jogo = Tilemap(self, TILE_SIZE)

        self.nivel = LEVEL
        self.carregar_nivel(self.nivel)

        self.balanco_imagem = 0

    def carregar_nivel(self, id_mapa):
        self.mapa_jogo.carregar(paths.MAPS_PATH / f'{id_mapa}.json')

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

        self.projetil_sprite.empty()
        self.particulas = []
        self.faiscas = []

        self.scroll = [0, 0]
        self.derrotado = 0
        self.transicao.resetar()

    def atualizar_folhas(self):
        for rect in self.gerador_folhas:
            if random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random() * rect.width,
                       rect.y + random() * rect.height)
                self.particulas.append(
                    Particula(self, 'folhas', pos, velocidade=[-0.1, 0.3], frame=randint(0, 20)))

    def renderizar_inimigos(self):
        for inimigo in self.inimigos.copy():
            derrotar = inimigo.atualizar(self.mapa_jogo, (0, 0))
            inimigo.renderizar(self.display, deslocamento=self.camera)
            if derrotar:
                self.inimigos.remove(inimigo)

    def desenhar_faiscas(self):
        for faisca in self.faiscas.copy():
            interromper = faisca.atualizar()
            faisca.renderizar(self.display, deslocamento=self.camera)
            if interromper:
                self.faiscas.remove(faisca)

    def desenhar_particulas(self):
        for particula in self.particulas.copy():
            interromper = particula.atualizar()
            particula.renderizar(self.display, deslocamento=self.camera)
            if particula.tipo == 'folhas':
                particula.pos[0] += sin(
                    particula.animacao.frame * 0.035) * 0.3
            if interromper:
                self.particulas.remove(particula)

    def carregar_proximo_nivel(self):
        if not len(self.inimigos):
            self.transicao.ativar()
            if self.transicao.finalizada():
                self.nivel = min(self.nivel + 1, len(listdir(paths.MAPS_PATH)) - 1)
                self.carregar_nivel(self.nivel)

    def verificar_derrota(self):
        if self.derrotado:
            self.derrotado += 1
            if self.derrotado >= 10:
                self.transicao.ativar()
            if self.derrotado > 60:
                self.carregar_nivel(self.nivel)

    def movimento_camera(self):
        self.scroll[0] += (self.jogador.retangulo().centerx - DISPLAY_L / 2 - self.scroll[0]) / ACE_CAMERA
        self.scroll[1] += (self.jogador.retangulo().centery - DISPLAY_A / 2 - self.scroll[1]) / ACE_CAMERA
        self.camera = (int(self.scroll[0]), int(self.scroll[1]))

    def atualizar(self, dt):
        self.balanco_imagem = max(0, self.balanco_imagem - 1)
        self.carregar_proximo_nivel()
        self.verificar_derrota()
        self.movimento_camera()
        self.atualizar_folhas()
        self.sprites.update(dt)
        self.projetil_sprite.update(dt)
        self.nuvens.atualizar(dt)
        self.jogador.atualizar(self.mapa_jogo, (self.movimento[1] - self.movimento[0], 0))
        self.hud.atualizar()

    def renderizar(self):
        self.display.fill((0, 0, 0, 0))
        self.display_2.blit(pygame.transform.scale(self.assets['plano_fundo'], RES_TELA), (0, 0))
        self.nuvens.renderizar(self.display_2, deslocamento=self.camera)
        self.mapa_jogo.renderizar(self.display, deslocamento=self.camera)
        self.jogador.renderizar(self.display, deslocamento=self.camera)
        self.renderizar_inimigos()
        self.sprites.draw(self.display)
        self.desenhar_faiscas()
        aplicar_contornos(self.display_2, self.display)
        self.desenhar_particulas()
        self.hud.renderizar(self.display)
        self.debug.renderizar(self.display)

        self.transicao.atualizar()
        self.transicao.renderizar(self.display)

        self.display_2.blit(self.display, (0, 0))

        balanco = (random() * self.balanco_imagem - self.balanco_imagem / 2,
                   random() * self.balanco_imagem - self.balanco_imagem / 2)

        self.tela.blit(pygame.transform.scale(self.display_2, RES_TELA), balanco)

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False
                elif evento.key == pygame.K_a:
                    self.movimento[0] = True
                elif evento.key == pygame.K_d:
                    self.movimento[1] = True
                elif evento.key == pygame.K_SPACE:
                    if self.jogador.pular():
                        self.sounds.play_sfx('jump')
                elif evento.key == pygame.K_j:
                    self.jogador.repulsao()
                self.debug.exibir_debug(evento)
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_a:
                    self.movimento[0] = False
                elif evento.key == pygame.K_d:
                    self.movimento[1] = False

    def rodar(self):
        while self.rodando:
            dt = self.relogio.tick(FPS) / 1000.0
            self.checar_eventos()
            self.atualizar(dt)
            self.renderizar()
            pygame.display.update()
        pygame.quit()
        exit()


if __name__ == '__main__':
    Game().rodar()

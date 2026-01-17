
import pygame
from pygame.sprite import Group

from random import random
from math import sin
from os import listdir, environ
from sys import exit

from scripts.utils import carregar_imagem, carregar_imagens, aplicar_contornos, Animacao
from scripts.objects import GeradorFolhas, Tilemap, Nuvens, Jogador, Inimigo
from scripts.soundmanager import SoundManager
from scripts.ui import Circulo, HUD
from scripts.debug import Debug
from scripts.constants import *
from scripts import paths

FLAGS_TELA = pygame.SCALED | pygame.RESIZABLE


class Game:
    def __init__(self):
        pygame.init()
        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption(LEGENDA)
        self.tela = pygame.display.set_mode(RES_TELA, FLAGS_TELA)
        self.mascara_surf = pygame.Surface(RES_TELA, pygame.SRCALPHA)
        self.relogio = pygame.time.Clock()

        self.sprites = Group()
        self.projetil_sprite = Group()

        self.hud = HUD(self)
        self.debug = Debug(self)
        self.transicao = Circulo()

        self.camera = None
        self.scroll = None
        self.faiscas = None
        self.inimigos = None
        self.derrotado = None
        self.particulas = None

        self.rodando = True
        self.tela_cheia = False

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
            'plano_fundo': carregar_imagem('background.png', RES_TELA),
        }

        self.sounds = SoundManager(paths.SOUND_ASSETS)
        self.sounds.play_music('ambience')
        self.sounds.play_music('music')

        self.nuvens = Nuvens(self.assets['nuvens'], NUM_NUVENS)

        self.jogador = Jogador(self, POSICAO, HIT_BOX)

        self.mapa_jogo = Tilemap(self, TILE_SIZE)

        self.gerador_folhas = GeradorFolhas(self)

        self.nivel = LEVEL
        self.carregar_nivel(self.nivel)

        self.balanco_imagem = 0

    def carregar_nivel(self, id_mapa):
        self.mapa_jogo.carregar(paths.MAPS_PATH / f'{id_mapa}.json')

        self.gerador_folhas.carregar_geradores(self.mapa_jogo)

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

    def renderizar_inimigos(self):
        for inimigo in self.inimigos.copy():
            derrotado = inimigo.atualizar(self.mapa_jogo, (0, 0))
            inimigo.renderizar(self.mascara_surf, deslocamento=self.camera)
            if derrotado:
                self.inimigos.remove(inimigo)

    def desenhar_faiscas(self):
        for faisca in self.faiscas.copy():
            interromper = faisca.atualizar()
            faisca.renderizar(self.mascara_surf, deslocamento=self.camera)
            if interromper:
                self.faiscas.remove(faisca)

    def desenhar_particulas(self):
        for particula in self.particulas.copy():
            interromper = particula.atualizar()
            particula.renderizar(self.mascara_surf, deslocamento=self.camera)
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
        self.scroll[0] += (self.jogador.retangulo().centerx - LARGURA / 2 - self.scroll[0]) / ACE_CAMERA
        self.scroll[1] += (self.jogador.retangulo().centery - ALTURA / 2 - self.scroll[1]) / ACE_CAMERA
        self.camera = (int(self.scroll[0]), int(self.scroll[1]))

        balanco = (random() * self.balanco_imagem - self.balanco_imagem / 2,
                   random() * self.balanco_imagem - self.balanco_imagem / 2)

        self.camera = (self.camera[0] + int(balanco[0]), self.camera[1] + int(balanco[1]))

    def atualizar(self, dt):
        self.balanco_imagem = max(0, self.balanco_imagem - 1)
        self.carregar_proximo_nivel()
        self.verificar_derrota()
        self.movimento_camera()
        self.gerador_folhas.atualizar()
    #    self.sprites.update(dt)
        self.projetil_sprite.update(dt)
        self.nuvens.atualizar(dt)
        self.jogador.atualizar(self.mapa_jogo)
        self.hud.atualizar()
        self.transicao.atualizar()

    def renderizar(self):
        self.mascara_surf.fill((0, 0, 0, 0))
        self.tela.blit(self.assets['plano_fundo'], (0, 0))
        self.nuvens.renderizar(self.tela, deslocamento=self.camera)
        self.mapa_jogo.renderizar(self.mascara_surf, deslocamento=self.camera)
        self.jogador.renderizar(self.mascara_surf, deslocamento=self.camera)
        self.renderizar_inimigos()
        self.projetil_sprite.draw(self.mascara_surf)
        #self.sprites.draw(self.mascara_surf)
        self.desenhar_faiscas()
        aplicar_contornos(self.tela, self.mascara_surf)
        self.desenhar_particulas()
        self.hud.renderizar(self.mascara_surf)
        self.debug.renderizar(self.mascara_surf)

        self.transicao.renderizar(self.mascara_surf)

        self.tela.blit(self.mascara_surf, (0, 0))

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False
                elif evento.key == pygame.K_SPACE:
                    if self.jogador.pular():
                        self.sounds.play_sfx('jump')
                elif evento.key == pygame.K_j:
                    self.jogador.repulsao()
                elif evento.key == pygame.K_F11:
                    self.tela_cheia = not self.tela_cheia
                    if self.tela_cheia:
                        pygame.display.set_mode(RES_TELA, FLAGS_TELA | pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode(RES_TELA, FLAGS_TELA)
                self.debug.exibir_dados_tela(evento)

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

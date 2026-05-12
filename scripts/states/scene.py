
import pygame
from pygame.sprite import Group
from random import random, choice
from os import listdir

from .state import State

from ..objects import GeradorFolhas, Tilemap, Nuvem, Jogador, Inimigo
from scripts.utils import carregar_imagem, carregar_imagens, aplicar_contornos, Animacao
from scripts.soundmanager import SoundManager
from scripts.ui import Circulo, HUD
from scripts.debug import Debug
from scripts.constants import *
from scripts import paths


class Scene(State):
    def __init__(self):
        super().__init__()
        self.dt = 0.0
        self.proximo = None

        self.relogio = pygame.time.Clock()

        # Sprites e grupos
        self.sprites = Group()
        self.nuvens = Group()
        self.particulas = Group()
        self.projetil_sprite = Group()

        # Componentes principais
        self.hud = HUD(self)
        self.debug = Debug(self)
        self.transicao = Circulo()

        # Estado e câmera
        self.camera = None
        self.scroll = None
        self.faiscas = None
        self.inimigos = None
        self.derrotado = None
        self.tela_cheia = False
        self.balanco_imagem = 0

        # Assets
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
            'folhas': Animacao(carregar_imagens('particles/leaf'), dur_img=20, loop=False),
            'particula': Animacao(carregar_imagens('particles/particle'), dur_img=6, loop=False),
            'pistola': carregar_imagem('gun.png'),
            'projetil': carregar_imagem('projectile.png'),
            'plano_fundo': carregar_imagem('background.png', RES_TELA),
        }

        # Sons
        self.sounds = SoundManager(paths.SOUND_ASSETS)
        self.sounds.play_music('ambience')
        self.sounds.play_music('music')

        # Nuvens
        self.desenhar_nuvem(self.nuvens, self.assets['nuvens'], NUM_NUVENS)

        # Jogador
        self.jogador = Jogador(self, POSICAO, HIT_BOX)

        # Mapa
        self.mapa_jogo = Tilemap(self, TILE_SIZE)

        # Gerador de folhas
        self.gerador_folhas = GeradorFolhas(self)

        # Nível
        self.nivel = LEVEL
        self.carregar_nivel(self.nivel)

        # Máscara para renderização
        self.mascara_surf = pygame.Surface(RES_TELA, pygame.SRCALPHA)

    def reset_game(self):
        self.projetil_sprite.empty()
        self.faiscas = []
        self.scroll = [0, 0]
        self.derrotado = 0
        self.transicao.resetar()

    def carregar_inimigos_folhas(self):
        self.inimigos = []
        for gerador in self.mapa_jogo.extrair([('geradores', 0), ('geradores', 1)]):
            if gerador['variante'] == 0:
                self.jogador.pos = gerador['pos']
                self.jogador.tempo_ar = 0
            else:
                self.inimigos.append(Inimigo(self, gerador['pos'], (8, 15)))

    def carregar_nivel(self, id_mapa):
        """Carrega um nível específico."""
        self.mapa_jogo.carregar(paths.MAPS_PATH / f'{id_mapa}.json')
        self.gerador_folhas.carregar_geradores(self.mapa_jogo)

        self.carregar_inimigos_folhas()
        self.reset_game()

    @staticmethod
    def desenhar_nuvem(sprites, imgs, quant):
        """Cria nuvens de fundo."""
        [Nuvem(
            grupo=sprites,
            img=choice(imgs),
            pos=(int(random() * 99999), int(random() * 99999)),
            velocidade=0.2 + random() * 0.2,
            margem=0.5 + random() * 0.5
        ) for _ in range(quant)]

    def renderizar_inimigos(self):
        """Renderiza e atualiza inimigos."""
        for inimigo in self.inimigos.copy():
            derrotado = inimigo.atualizar(self.dt, self.mapa_jogo, (0, 0))
            inimigo.renderizar(self.mascara_surf, deslocamento=self.camera)
            if derrotado:
                self.inimigos.remove(inimigo)

    def desenhar_faiscas(self):
        """Desenha efeitos de faiscas."""
        for faisca in self.faiscas.copy():
            interromper = faisca.atualizar()
            faisca.renderizar(self.mascara_surf, deslocamento=self.camera)
            if interromper:
                self.faiscas.remove(faisca)

    def carregar_proximo_nivel(self):
        """Carrega o próximo nível ao derrotar todos os inimigos."""
        if not len(self.inimigos):
            self.transicao.ativar()
            if self.transicao.finalizada():
                self.nivel = min(self.nivel + 1, len(listdir(paths.MAPS_PATH)) - 1)
                self.carregar_nivel(self.nivel)

    def verificar_derrota(self):
        """Verifica se o jogador foi derrotado."""
        if self.derrotado:
            self.derrotado += 1
            if self.derrotado >= 10:
                self.transicao.ativar()
            if self.derrotado > 40:
                self.carregar_nivel(self.nivel)

    def movimento_camera(self):
        """Calcula movimento da câmera seguindo o jogador."""
        self.scroll[0] += (self.jogador.retangulo.centerx - LARGURA / 2 - self.scroll[0]) / ACE_CAMERA
        self.scroll[1] += (self.jogador.retangulo.centery - ALTURA / 2 - self.scroll[1]) / ACE_CAMERA
        self.camera = (int(self.scroll[0]), int(self.scroll[1]))

        balanco = (random() * self.balanco_imagem - self.balanco_imagem / 2,
                   random() * self.balanco_imagem - self.balanco_imagem / 2)

        self.camera = (self.camera[0] + int(balanco[0]), self.camera[1] + int(balanco[1]))

    def checar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.proximo = 'menu'
                self.feito = True
            elif evento.key == pygame.K_SPACE:
                if self.jogador.pular():
                    self.sounds.play_sfx('jump')
            elif evento.key == pygame.K_j:
                self.jogador.repulsao()
            self.debug.exibir_dados_tela(evento)

    def atualizar(self, dt, tempo):
        """Atualiza o estado do jogo."""
        self.dt = dt
        self.balanco_imagem = max(0, self.balanco_imagem - 1)
        self.carregar_proximo_nivel()
        self.verificar_derrota()
        self.movimento_camera()
        self.gerador_folhas.atualizar()
        self.projetil_sprite.update(dt)
        self.nuvens.update(dt, self.camera)
        self.jogador.atualizar(dt, self.mapa_jogo)
        self.particulas.update(self.camera)
        self.hud.atualizar()
        self.transicao.atualizar()

    def renderizar(self, surf):
        """Renderiza o estado do jogo."""
        self.mascara_surf.fill((0, 0, 0, 0))
        surf.blit(self.assets['plano_fundo'], (0, 0))
        self.nuvens.draw(surf)
        self.mapa_jogo.renderizar(self.mascara_surf, deslocamento=self.camera)
        self.jogador.renderizar(self.mascara_surf, deslocamento=self.camera)
        self.renderizar_inimigos()
        self.projetil_sprite.draw(self.mascara_surf)
        self.desenhar_faiscas()
        aplicar_contornos(surf, self.mascara_surf)
        self.particulas.draw(self.mascara_surf)
        self.hud.renderizar(self.mascara_surf)
        self.debug.renderizar(self.mascara_surf)
        self.transicao.renderizar(self.mascara_surf)
        surf.blit(self.mascara_surf, (0, 0))


# def carregar_tilemap(self):
#     """Carrega tilemap TMX (mantido para compatibilidade)."""
#     dados_mapa = load_pygame(str(paths.MAPS_PATH / f'teste.tmx'))
#     tilesize = dados_mapa.tilewidth
#
#     terreno = dados_mapa.get_layer_by_name('terreno')
#     for x, y, gid, in terreno:  # type: ignore
#         tile = dados_mapa.get_tile_image_by_gid(gid)
#         if tile:
#             Tile([self.sprites, self.sprites_colisao],
#                  (x * tilesize, y * tilesize), tile)
#
#     decor = dados_mapa.get_layer_by_name('decoracoes')
#     for x, y, gid, in decor:  # type: ignore
#         tile = dados_mapa.get_tile_image_by_gid(gid)
#         if tile:
#             Tile([self.sprites],
#                  (x * tilesize, y * tilesize), tile)
#
#     decor_grande = dados_mapa.get_layer_by_name('decor_grande')
#     for obj in decor_grande:  # type: ignore
#         Tile([self.sprites], (obj.x, obj.y), obj.image)
#
#     pontos_entidades = dados_mapa.get_layer_by_name('pontos_entidades')
#     for obj in pontos_entidades:  # type: ignore
#         if obj.name == 'jogador':
#             self.pos_jogador = [obj.x, obj.y]


import pygame

from math import sin, cos, pi
from random import random, randint
from pygame.math import Vector2 as Vetor
from pygame.sprite import Sprite, Group

from scripts.constants import *
from .projetil import Projetil
from .particulas import Particula
from .efeito_faisca import Faisca

#TODO: Refatorar para usar a classe Sprites do pygame
class Entitiy(Sprite):
    def __init__(
            self,
            main,
            tipo: str,
            pos: tuple[int, int],
            tamanho: tuple[int, int],
            colisoes: Group
    ) -> None:
        super().__init__(main.grupos)
        self.main = main
        self.tipo = tipo
        self.sprites_colisao = colisoes

        self.direcao = Vetor(0, 0)
        self.flipe = False

        self.image = pygame.Surface(*tamanho).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos) # type: ignore
        self.hitbox = self.rect.copy().inflate(*tamanho) # type: ignore

    def update(self, *args, **kwargs) -> None:
        pass


class Entitiy(Sprite):
    def __init__(
            self,
            main,
            tipo: str,
            pos: tuple[int, int],
            tamanho: tuple[int, int],
            colisoes: Group
    ) -> None:
        super().__init__(main.grupos)
        self.main = main
        self.tipo = tipo
        self.sprites_colisao = colisoes

        self.direcao = Vetor(0, 0)
        self.flipe = False

        self.image = pygame.Surface(*tamanho).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos) # type: ignore
        self.hitbox = self.rect.copy().inflate(*tamanho) # type: ignore

    def update(self, *args, **kwargs) -> None:
        pass


class PhysicsEntity:
    def __init__(self, main, tipo_e, pos, tamanho):
        self.main = main
        self.tipo = tipo_e
        self.pos = list(pos)
        self.tamanho = tamanho
        self.velocidade = Vetor(0, 0)
        self.colisoes = {'up': False, 'down': False, 'right': False, 'left': False}

        self.animacao = None

        self.acao = ''
        self.flipe = False
        self.acao_atual('idle')

        self.movimento_atual = [0, 0]
        self.movimento_frame = None

    @property
    def retangulo(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.tamanho[0], self.tamanho[1])

    def acao_atual(self, acao):
        if acao != self.acao:
            self.acao = acao
            self.animacao = self.main.assets[self.tipo + '/' + self.acao].copia()

    def _resetar_colisoes(self):
        self.colisoes = {'up': False, 'down': False, 'right': False, 'left': False}

    def _calcular_movimento_frame(self, movimento):
        return movimento[0] + self.velocidade.x, movimento[1] + self.velocidade.y

    def _processar_colisoes_horizontal(self, tilemap, movimento_frame):
        self.pos[0] += movimento_frame[0]
        rect_entidade = self.retangulo
        for rect in tilemap.colisao_rects_aoredor(self.pos):
            if rect_entidade.colliderect(rect):
                if movimento_frame[0] > 0:
                    rect_entidade.right = rect.left
                    self.colisoes['right'] = True
                if movimento_frame[0] < 0:
                    rect_entidade.left = rect.right
                    self.colisoes['left'] = True
                self.pos[0] = rect_entidade.x

    def _processar_colisoes_vertical(self, tilemap, movimento_frame):
        self.pos[1] += movimento_frame[1]
        rect_entidade = self.retangulo
        for rect in tilemap.colisao_rects_aoredor(self.pos):
            if rect_entidade.colliderect(rect):
                if movimento_frame[1] > 0:
                    rect_entidade.bottom = rect.top
                    self.colisoes['down'] = True
                if movimento_frame[1] < 0:
                    rect_entidade.top = rect.bottom
                    self.colisoes['up'] = True
                self.pos[1] = rect_entidade.y

    def _atualizar_velocidade_vertical(self):
        self.velocidade.y = min(VEL_MAX_QUEDA, self.velocidade.y + 0.1)

        if self.colisoes['down'] or self.colisoes['up']:
            self.velocidade.y = 0

    def flipe_horizontal_imagem(self, movimento):
        if movimento[0] > 0:
            self.flipe = False
        if movimento[0] < 0:
            self.flipe = True

    def atualizar(self, dt, tilemap, movimento=(0, 0)):
        self._resetar_colisoes()
        self.movimento_frame = self._calcular_movimento_frame(movimento)

        self._processar_colisoes_horizontal(tilemap, self.movimento_frame)
        self._processar_colisoes_vertical(tilemap, self.movimento_frame)

        self.flipe_horizontal_imagem(movimento)

        self.movimento_atual = movimento

        self._atualizar_velocidade_vertical()

        self.animacao.atualizar()

    def renderizar(self, surf, deslocamento=(0, 0)):
        surf.blit(pygame.transform.flip(self.animacao.imagem(), self.flipe, False),
                 (self.pos[0] - deslocamento[0] + DESLOCAMENTO_ANIM,
                  self.pos[1] - deslocamento[1] + DESLOCAMENTO_ANIM))


class Inimigo(PhysicsEntity):
    def __init__(self, main, pos, tamanho):
        super().__init__(main, 'inimigo', pos, tamanho)
        self.correndo = 0

    def atualizar_animacao(self, movimento):
        if movimento[0] != 0:
            self.acao_atual('run')
        else:
            self.acao_atual('idle')

    def calcular_distancia_jogador(self):
        return self.main.jogador.pos[0] - self.pos[0], self.main.jogador.pos[1] - self.pos[1]

    def atirar_projetil(self, direcao):
        self.main.sounds.play_sfx('shoot')
        Projetil(
            self.main,
            [self.main.projetil_sprite, self.main.sprites],
            [self.retangulo.centerx + (-7 if direcao == -1 else 7), self.retangulo.centery],
            direcao)

    def gerar_particulas_ataque(self):
        for i in range(NUMS_PARTICULAS_ATAQUE):
            angulo = random() * pi * 2
            velocidade = random() * 5
            self.main.faiscas.append(Faisca(self.retangulo.center, angulo, 2 + random()))
            Particula(
                grupos=self.main.particulas,
                anim=self.main.assets['particula'],
                pos=self.retangulo.center,
                velocidade=(cos(angulo + pi) * velocidade * 0.5,
                           sin(angulo + pi) * velocidade * 0.5),
                frame=randint(0, 7))
        self.main.faiscas.append(Faisca(self.retangulo.center, 0, 5 + random()))
        self.main.faiscas.append(Faisca(self.retangulo.center, pi, 5 + random()))

    def verificar_colisao_jogador_dash(self):
        if abs(self.main.jogador.repulsando) >= 50:
            if self.retangulo.colliderect(self.main.jogador.retangulo):
                self.main.balanco_imagem = max(16, self.main.balanco_imagem)
                self.main.sounds.play_sfx('hit')
                self.gerar_particulas_ataque()
                return True
        return False

    def verificar_disparo_inimigo(self):
        if not self.correndo:
            distancia = self.calcular_distancia_jogador()

            if abs(distancia[1]) < 16:
                if self.flipe and distancia[0] < 0:
                    self.atirar_projetil(-1)
                elif not self.flipe and distancia[0] > 0:
                    self.atirar_projetil(1)

    def ajustar_movimento_terreno(self, movimento):
        if self.colisoes['right'] or self.colisoes['left']:
            self.flipe = not self.flipe
        else:
            movimento = (movimento[0] - 0.5 if self.flipe else 0.5, movimento[1])
        return movimento

    def atualizar_corrida(self, tilemap, movimento):
        if self.correndo:
            if tilemap.checar_solido((self.retangulo.centerx + (-7 if self.flipe else 7), self.pos[1] + 23)):
                movimento = self.ajustar_movimento_terreno(movimento)
            else:
                self.flipe = not self.flipe
            self.correndo = max(0, self.correndo - 1)
            self.verificar_disparo_inimigo()
        elif random() < 0.01:
            self.correndo = randint(30, 120)
        return movimento

    def atualizar(self, dt, tilemap, movimento=(0, 0)):
        movimento = self.atualizar_corrida(tilemap, movimento)
        super().atualizar(dt, tilemap, movimento=movimento)

        self.atualizar_animacao(movimento)
        return self.verificar_colisao_jogador_dash()

    def renderizar(self, surf, deslocamento=(0, 0)):
        super().renderizar(surf, deslocamento=deslocamento)
        if self.flipe:
            surf.blit(pygame.transform.flip(self.main.assets['pistola'], True, False),
                      (self.retangulo.centerx - 4 - self.main.assets['pistola'].get_width() - deslocamento[0],
                       self.retangulo.centery - deslocamento[1]))
        else:
            surf.blit(self.main.assets['pistola'], (self.retangulo.centerx + 4 - deslocamento[0],
                                                    self.retangulo.centery - deslocamento[1]))


class Jogador(PhysicsEntity):
    def __init__(self, main, pos, tamanho):
        super().__init__(main, 'jogador', pos, tamanho)
        self.tempo_ar = 0
        self.pulos = 1
        self.deslize_parede = False
        self.repulsando = 0
        self.direcao = 0

    def controlar_jogador(self):
        teclas = pygame.key.get_pressed()
        self.direcao = int(teclas[pygame.K_d]) - int(teclas[pygame.K_a])

    def _atualizar_tempo_ar(self):
        self.tempo_ar += 1
        if self.tempo_ar > 120:
            if not self.main.derrotado:
                self.main.balanco_imagem = max(16, self.main.balanco_imagem)
            self.main.derrotado += 1

    def _resetar_ao_pousar(self):
        if self.colisoes['down']:
            self.tempo_ar = 0
            self.pulos = 1

    def _verificar_deslize_parede(self):
        self.deslize_parede = False
        if (self.colisoes['right'] or self.colisoes['left']) and self.tempo_ar > 4:
            self.deslize_parede = True
            self.velocidade.y = min(self.velocidade.y, 0.5)
            if self.colisoes['right']:
                self.flipe = False
            else:
                self.flipe = True
            self.acao_atual('deslize_parede')

    def _atualizar_animacao(self):
        if not self.deslize_parede:
            if self.tempo_ar > 4:
                self.acao_atual('pulo')
            elif self.direcao != 0:
                self.acao_atual('run')
            else:
                self.acao_atual('idle')

    def _gerar_particulas_dash(self):
        if abs(self.repulsando) in {60, 50}:
            for i in range(20):
                angulo = random() * pi * 2
                velocidade = random() * 0.5 + 0.5
                vel_particula = (cos(angulo) * velocidade, sin(angulo) * velocidade)
                Particula(
                    grupos=self.main.particulas,
                    anim=self.main.assets['particula'],
                    pos=self.retangulo.center,
                    velocidade=vel_particula,
                    frame=randint(0, 7))

    def _gerar_particulas_pulo(self):
        for i in range(3):
            angulo = random() * pi + pi
            velocidade = random() * 2
            self.main.faiscas.append(Faisca(self.retangulo.midbottom, angulo, 2 + random()))
            Particula(
                grupos=self.main.particulas,
                anim=self.main.assets['particula'],
                pos=self.retangulo.midbottom,
                velocidade=(cos(angulo) * velocidade * 0.5,
                           sin(angulo) * velocidade * 0.5),
                frame=randint(0, 7))

    def _atualizar_repulsao(self):
        if self.repulsando > 0:
            self.repulsando = max(0, self.repulsando - 1)
        if self.repulsando < 0:
            self.repulsando = min(0, self.repulsando + 1)

        self._gerar_particulas_dash()

        if abs(self.repulsando) > 50:
            self.velocidade.x = abs(self.repulsando) / self.repulsando * 8
            if abs(self.repulsando) == 51:
                self.velocidade.x *= 0.1
            Particula(
                grupos=self.main.particulas,
                anim=self.main.assets['particula'],
                pos=self.retangulo.center,
                velocidade=(abs(self.repulsando) / self.repulsando * random() * 3, 0),
                frame=randint(0, 7))

    def _atualizar_velocidade_horizontal(self):
        """Aplica desaceleração à velocidade horizontal"""
        if self.velocidade.x > 0:
            self.velocidade.x = max(self.velocidade.x - 0.1, 0)
        else:
            self.velocidade.x = min(self.velocidade.x + 0.1, 0)

    def pular(self):
        if self.deslize_parede:
            if self.flipe and self.movimento_atual[0] < 0:
                self.velocidade.x = 3.5
                self.velocidade.y = -2.5
                self.tempo_ar = 5
                self.pulos = max(0, self.pulos - 1)
                return True

            elif not self.flipe and self.movimento_atual[0] > 0:
                self.velocidade.x = -3.5
                self.velocidade.y = -2.5
                self.tempo_ar = 5
                self.pulos = max(0, self.pulos - 1)
                return True

        elif self.pulos:
            self.velocidade.y = -FORCA_PULO
            self.pulos -= 1
            self.tempo_ar = 5
            self._gerar_particulas_pulo()
            return True
        return None

    def repulsao(self):
        if not self.repulsando:
            self.main.sounds.play_sfx('dash')
            if self.flipe:
                self.repulsando = -60
            else:
                self.repulsando = 60

    def atualizar(self, dt, tilemap, movimento=(0, 0)):
        self.controlar_jogador()
        if not self.main.derrotado:
            super().atualizar(dt, tilemap, movimento=(self.direcao, 0))

            self._atualizar_tempo_ar()
            self._resetar_ao_pousar()
            self._verificar_deslize_parede()
            self._atualizar_animacao()
            self._atualizar_repulsao()
            self._atualizar_velocidade_horizontal()

    def renderizar(self, surf, deslocamento=(0, 0)):
        if not self.main.derrotado:
            if abs(self.repulsando) <= 50:
                super().renderizar(surf, deslocamento=deslocamento)
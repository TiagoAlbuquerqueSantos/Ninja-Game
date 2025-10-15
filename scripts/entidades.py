import math
import random

import pygame

from scripts.particulas import Particula
from scripts.efeito_faisca import Faisca

class PhysicsEntity:
    def __init__(self, main, tipo_e, pos, tamanho):
        self.main = main
        self.tipo = tipo_e
        self.pos = list(pos)
        self.tamanho = tamanho
        self.velocidade = [0, 0]
        self.colisoes = {'up': False, 'down': False, 'right': False, 'left': False}

        self.animacao = None

        self.acao = ''
        self.deslocamento_anim = (-3, -3)
        self.flipe = False
        self.acao_atual('idle')

        self.movimento_atual = [0, 0]

    def retangulo(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.tamanho[0], self.tamanho[1])

    def acao_atual(self, acao):
        if acao != self.acao:
            self.acao = acao
            self.animacao = self.main.assets[self.tipo + '/' + self.acao].copia()

    def atualizar(self, tilemap, movimento=(0, 0)):
        self.colisoes = {'up': False, 'down': False, 'right': False, 'left': False}

        movimento_frame = (movimento[0] + self.velocidade[0], movimento[1] + self.velocidade[1])

        self.pos[0] += movimento_frame[0]
        rect_entidade = self.retangulo()
        for rect in tilemap.colisao_rects_aoredor(self.pos):
            if rect_entidade.colliderect(rect):
                if movimento_frame[0] > 0:
                    rect_entidade.right = rect.left
                    self.colisoes['right'] = True
                if movimento_frame[0] < 0:
                    rect_entidade.left = rect.right
                    self.colisoes['left'] = True
                self.pos[0] = rect_entidade.x

        self.pos[1] += movimento_frame[1]
        rect_entidade = self.retangulo()
        for rect in tilemap.colisao_rects_aoredor(self.pos):
            if rect_entidade.colliderect(rect):
                if movimento_frame[1] > 0:
                    rect_entidade.bottom = rect.top
                    self.colisoes['down'] = True
                if movimento_frame[1] < 0:
                    rect_entidade.top = rect.bottom
                    self.colisoes['up'] = True
                self.pos[1] = rect_entidade.y

        if movimento[0] > 0:
            self.flipe = False
        if movimento[0] < 0:
            self.flipe = True

        self.movimento_atual = movimento

        self.velocidade[1] = min(5, self.velocidade[1] + 0.1)

        if self.colisoes['down'] or self.colisoes['up']:
            self.velocidade[1] = 0

        self.animacao.atualizar()

    def renderizar(self, surf, deslocamento=(0, 0)):
        surf.blit(pygame.transform.flip(self.animacao.imagem(), self.flipe, False),
                 (self.pos[0] - deslocamento[0] + self.deslocamento_anim[0],
                  self.pos[1] - deslocamento[1] + self.deslocamento_anim[1]))


class Inimigo(PhysicsEntity):
    def __init__(self, main, pos, tamanho):
        super().__init__(main, 'inimigo', pos, tamanho)
        
        self.correndo = 0
        
    def atualizar(self, tilemap, movimento=(0, 0)):
        if self.correndo:
            if tilemap.checar_solido((self.retangulo().centerx + (-7 if self.flipe else 7), self.pos[1] + 23)):
                if self.colisoes['right'] or self.colisoes['left']:
                    self.flipe = not self.flipe
                else:
                    movimento = (movimento[0] - 0.5 if self.flipe else 0.5, movimento[1])
            else:
                self.flipe = not self.flipe
            self.correndo = max(0, self.correndo - 1)
            if not self.correndo:
                distancia =  (self.main.jogador.pos[0] - self.pos[0], self.main.jogador.pos[1] - self.pos[1])
                if abs(distancia[1]) < 16:
                    if self.flipe and distancia[0] < 0:
                        self.main.sfx['tiro'].play()
                        self.main.projeteis.append([[self.retangulo().centerx - 7, self.retangulo().centery], -1.5, 0])
                        for i in range(4):
                            self.main.faiscas.append(
                                Faisca(self.main.projeteis[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))

                    if not self.flipe and distancia[0] > 0:
                        self.main.sfx['tiro'].play()
                        self.main.projeteis.append([[self.retangulo().centerx + 7, self.retangulo().centery], 1.5, 0])
                        for i in range(4):
                            self.main.faiscas.append(
                                Faisca(self.main.projeteis[-1][0], random.random() - 0.5, 2 + random.random()))

        elif random.random() < 0.01:
            self.correndo = random.randint(30, 120)

        super().atualizar(tilemap, movimento=movimento)

        if movimento[0] != 0:
            self.acao_atual('run')
        else:
            self.acao_atual('idle')

        if abs(self.main.jogador.repulsando) >= 50:
            if self.retangulo().colliderect(self.main.jogador.retangulo()):
                self.main.balanco_imagem = max(16, self.main.balanco_imagem)
                self.main.sfx['hit'].play()
                for i in range(30):
                    angulo = random.random() * math.pi * 2
                    velocidade = random.random() * 5
                    self.main.faiscas.append(Faisca(self.retangulo().center, angulo, 2 + random.random()))
                    self.main.particulas.append(Particula(self.main,'particula', self.retangulo().center,
                                                     velocidade=[math.cos(angulo + math.pi) * velocidade * 0.5,
                                                                 math.sin(angulo + math.pi) * velocidade * 0.5],
                                                     frame=random.randint(0, 7)))
                self.main.faiscas.append(Faisca(self.retangulo().center,0, 5 + random.random()))
                self.main.faiscas.append(Faisca(self.retangulo().center, math.pi, 5 + random.random()))
                return True

    def renderizar(self, surf, deslocamento=(0, 0)):
        super().renderizar(surf, deslocamento=deslocamento)

        if self.flipe:
            surf.blit(pygame.transform.flip(self.main.assets['pistola'], True, False),
                      (self.retangulo().centerx - 4 - self.main.assets['pistola'].get_width() - deslocamento[0],
                       self.retangulo().centery - deslocamento[1]))
        else:
            surf.blit(self.main.assets['pistola'], (self.retangulo().centerx + 4 - deslocamento[0],
                                                    self.retangulo().centery - deslocamento[1]))


class Jogador(PhysicsEntity):
    def __init__(self, main, pos, tamanho):
        super().__init__(main, 'jogador', pos, tamanho)
        self.tempo_ar = 0
        self.pulos = 1
        self.deslize_parede = False
        self.repulsando = 0

    def atualizar(self, tilemap, movimento=(0, 0)):
        super().atualizar(tilemap, movimento=movimento)

        self.tempo_ar += 1

        if self.tempo_ar > 120:
            if not self.main.derrotado:
                self.main.balanco_imagem = max(16, self.main.balanco_imagem)
            self.main.derrotado += 1

        if self.colisoes['down']:
            self.tempo_ar = 0
            self.pulos = 1

        self.deslize_parede = False
        if (self.colisoes['right'] or self.colisoes['left']) and self.tempo_ar > 4:
            self.deslize_parede = True
            self.velocidade[1] = min(self.velocidade[1], 0.5)
            if self.colisoes['right']:
                self.flipe = False
            else:
                self.flipe = True
            self.acao_atual('deslize_parede')

        if not self.deslize_parede:
            if self.tempo_ar > 4:
                self.acao_atual('pulo')
            elif movimento[0] != 0:
                self.acao_atual('run')
            else:
                self.acao_atual('idle')

        if abs(self.repulsando) in {60, 50}:
            for i in range(20):
                angulo = random.random() * math.pi * 2
                velocidade = random.random() * 0.5 + 0.5
                vel_particula = [math.cos(angulo) * velocidade, math.sin(angulo) * velocidade]
                self.main.particulas.append(Particula(self.main, 'particula', self.retangulo().center,
                                                      velocidade=vel_particula, frame=random.randint(0, 7)))
        if self.repulsando > 0:
            self.repulsando = max(0, self.repulsando - 1)
        if self.repulsando < 0:
            self.repulsando = min(0, self.repulsando + 1)
        if abs(self.repulsando) > 50:
            self.velocidade[0] = abs(self.repulsando) / self.repulsando * 8
            if abs(self.repulsando) == 51:
                self.velocidade[0] *= 0.1
            vel_particula = [abs(self.repulsando) / self.repulsando * random.random() * 3, 0]
            self.main.particulas.append(Particula(self.main, 'particula', self.retangulo().center,
                                                  velocidade=vel_particula, frame=random.randint(0, 7)))

        if self.velocidade[0] > 0:
            self.velocidade[0] = max(self.velocidade[0] - 0.1, 0)
        else:
            self.velocidade[0] = min(self.velocidade[0] + 0.1, 0)

    def renderizar(self, surf, deslocamento=(0, 0)):
        if abs(self.repulsando) <= 50:
            super().renderizar(surf, deslocamento=deslocamento)

    def pular(self):
        if self.deslize_parede:
            if self.flipe and self.movimento_atual[0] < 0:
                self.velocidade[0] = 3.5
                self.velocidade[1] = -2.5
                self.tempo_ar = 5
                self.pulos = max(0, self.pulos - 1)
                return True

            elif not self.flipe and self.movimento_atual[0] > 0:
                self.velocidade[0] = -3.5
                self.velocidade[1] = -2.5
                self.tempo_ar = 5
                self.pulos = max(0, self.pulos - 1)
                return True

        elif self.pulos:
            self.velocidade[1] = -3
            self.pulos -= 1
            self.tempo_ar = 5
            return True

    def repulsao(self):
        if not self.repulsando:
            self.main.sfx['repulsao'].play()
            if self.flipe:
                self.repulsando = -60
            else:
                self.repulsando = 60


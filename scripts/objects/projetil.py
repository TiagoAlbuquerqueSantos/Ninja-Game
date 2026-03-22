
from random import random, randint
from math import sin, cos, pi

from pygame.math import Vector2
from pygame.sprite import Sprite

from ..utils import Timer
from ..constants import NUMS_FAISCA_PAREDE, NUMS_FAISCA_DERROTADO
from .particulas import Particula
from .efeito_faisca import Faisca
from ..constants import VEL_PROJETIL


class Projetil(Sprite):
    def __init__(self, game, grupos, pos, direcao) -> None:
        super().__init__(grupos)
        self.game = game
        self.image = self.game.assets['projetil']
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.direcao = direcao

        self.tempo_vida = Timer(5000, auto_start=True)

        self.gerar_faisca_tiro()
        
    def gerar_faisca_tiro(self) -> None:
        for i in range(4):
            if self.direcao < 0:
                self.game.faiscas.append(Faisca(self.pos, random() - 0.5 + pi, 2 + random()))
            else:
                self.game.faiscas.append(Faisca(self.pos, random() - 0.5, 2 + random()))

    def destruir_projetil(self) -> None:
        if self.game.mapa_jogo.checar_solido(self.pos):
            self.kill()

            for i in range(NUMS_FAISCA_PAREDE):  # TODO particulas quando o projetil bater na parede
                self.game.faiscas.append(
                    Faisca(self.pos, random() - 0.5 + (pi if self.direcao > 0 else 0), 2 + random()))

        elif not self.tempo_vida.ativo:
            self.kill()

        elif abs(self.game.jogador.repulsando) < 50 and self.game.jogador.retangulo().collidepoint(self.pos):
            self.kill()
            self.game.derrotado += 1
            self.game.sounds.play_sfx('hit')
            self.game.balanco_imagem = max(16, self.game.balanco_imagem)

            for i in range(NUMS_FAISCA_DERROTADO):  # TODO particulas quando o jogador for derrotado
                angulo = random() * pi * 2
                velocidade = random() * 5
                self.game.faiscas.append(
                    Faisca(self.game.jogador.retangulo().center, angulo, 2 + random()))
                self.game.particulas.append(Particula(self.game, 'particula',
                                                      self.game.jogador.retangulo().center,
                                                 velocidade=[cos(angulo + pi) * velocidade * 0.5,
                                                             sin(angulo + pi) * velocidade * 0.5],
                                                 frame=randint(0, 7)))

    def update(self, dt) -> None:
        self.tempo_vida.atualizar()

        self.pos.x += self.direcao * VEL_PROJETIL * dt
        self.rect.x = self.pos.x - self.image.get_width() / 2 - self.game.camera[0]
        self.rect.y = self.pos.y - self.image.get_height() / 2 - self.game.camera[1]
        self.destruir_projetil()



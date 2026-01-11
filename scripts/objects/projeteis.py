
from pygame.sprite import Sprite
from random import random, randint
from math import pi, cos, sin

from .efeito_faisca import Faisca
from .particulas import Particula
from ..constants import NUMS_FAISCA_PAREDE, NUMS_FAISCA_DERROTADO


class Projetil(Sprite):
    def __init__(self, game, pos, velocidade, duracao=360):
        # É necessário chamar o construtor da classe pai (Sprite)
        super().__init__()
        self.game = game

        # Atributos obrigatórios para Sprites
        self.image = self.game.assets['projetil']
        self.rect = self.image.get_rect(center=pos)

        # Usamos float para a posição para manter a precisão do movimento
        self.pos = list(pos)
        self.velocidade = velocidade
        self.timer = 0
        self.duracao = duracao

        # TODO corrigir faíscas que não estão invertidas
        for _ in range(4):
            self.game.faiscas.append(Faisca(self.pos, random() - 0.5 + pi, 2 + random()))

    def update(self):
        """O Pygame chama o mét-odo 'update' automaticamente através do Grupo."""
        self.timer += 1
        self.pos[0] += self.velocidade
        self.rect.centerx = self.pos[0]

        # 1. Colisão com o mapa
        if self.game.mapa_jogo.checar_solido(self.pos):
            self.kill()  # Remove o sprite de todos os grupos
            self.gerar_faiscas_parede()

        # 2. Tempo de vida esgotado
        elif self.timer > self.duracao:
            self.kill()

        # 3. Colisão com o jogador
        elif abs(self.game.jogador.repulsando) < 50:
            if self.game.jogador.retangulo().colliderect(self.rect):
                self.game.derrotado += 1
                self.game.sounds.play_sfx('hit')
                self.game.balanco_imagem = max(16, self.game.balanco_imagem)
                self.gerar_faiscas_morte()
                self.kill()

    def gerar_faiscas_parede(self):
        for i in range(NUMS_FAISCA_PAREDE):
            angulo = random() - 0.5 + (pi if self.velocidade > 0 else 0)
            self.game.faiscas.append(Faisca(self.pos, angulo, 2 + random()))

    def gerar_faiscas_morte(self):
        for i in range(NUMS_FAISCA_DERROTADO):
            angulo = random() * pi * 2
            vel_particula = random() * 5
            self.game.faiscas.append(Faisca(self.game.jogador.retangulo().center, angulo, 2 + random()))
            self.game.particulas.append(Particula(
                self.game, 'particula', self.game.jogador.retangulo().center,
                velocidade=[cos(angulo + pi) * vel_particula * 0.5, sin(angulo + pi) * vel_particula * 0.5],
                frame=randint(0, 7)
            ))

    def draw(self, superficie, camera):
        # Subtraímos a câmera da posição do rect para desenhar no lugar certo
        pos_render = (self.rect.x - camera[0], self.rect.y - camera[1])
        superficie.blit(self.image, pos_render)
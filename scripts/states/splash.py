
import pygame

from .state import State
from ..ui import TextoTitulo
from ..constants import CENTRO_TELA


class Splash(State):
    def __init__(self):
        super().__init__()
        self.proximo = 'menu'
        self.tempo_decorrido = 0
        self.duracao_splash = 3.0  # 3 segundos
        self.alpha = 255

    def checar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                self.tempo_decorrido = self.duracao_splash  # Pula para transição

    def atualizar(self, dt, tempo):
        self.tempo_decorrido += dt

        # Calcula o alpha baseado no tempo
        if self.tempo_decorrido < 0.5:
            # Fade in
            self.alpha = int(255 * (self.tempo_decorrido / 0.5))
        elif self.tempo_decorrido < 2.5:
            # Mantém total
            self.alpha = 255
        elif self.tempo_decorrido < 3.0:
            # Fade out
            tempo_fade = self.tempo_decorrido - 2.5
            self.alpha = int(255 * (1 - (tempo_fade / 0.5)))
        else:
            # Transição concluída
            self.feito = True
            self.alpha = 0

    def renderizar(self, surf):
        TextoTitulo('Criado por Tiago Albuquerque', surf, CENTRO_TELA)

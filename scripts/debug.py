import pygame

from .constants import *
from .ui import Text


class Debug:
    def __init__(self, game):
        self.game = game
        self.exibir_dados = True

    def exibir_dados_tela(self, tecla):
        if tecla.key == pygame.K_F3:
            self.exibir_dados = not self.exibir_dados

    def renderizar(self, display):
        pos = (round(self.game.jogador.pos[0], 1),
               round(self.game.jogador.pos[1], 1))
        vel = (round(self.game.jogador.velocidade[0], 2),
               round(self.game.jogador.velocidade[1], 2))
        mov = self.game.jogador.movimento_frame


        dados_texto = f"""
        FPS: {self.game.relogio.get_fps():.2f}
        Pos: {pos}
        Vel: {vel} - Mov Frame: {mov}
        Nums de chances: {self.game.derrotado} - Tempo no Ar: {self.game.jogador.tempo_ar}
        """

        if self.exibir_dados:
            self.renderizar_customizado(display, dados_texto)

    def renderizar_customizado(self, display, dados_texto, posicao=(-30, ALTURA - 45)):
        if isinstance(dados_texto, str):
            dados_texto = [dados_texto]

        x, y = posicao
        for i, texto in enumerate(dados_texto):
            Text(texto, display, (x, y + i * 15), cor=Cores.VERMELHO)
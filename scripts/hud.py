import pygame
from pathlib import Path
from pgbitmapfont import BitmapFont

from scripts.constants import *


class HUD:
    def __init__(self, game):
        self.game = game
        self.fonte = BitmapFont(
            path=Path("data/fonts/small_font.json"),
            size=TAM_FONTE,
            fgcolor=pygame.Color(COR_FONTE),
            spacing=(1, 1)
        )
    
    def renderizar(self, display):
        pos = (round(self.game.jogador.pos[0], 1),
               round(self.game.jogador.pos[1], 1))
        vel = (round(self.game.jogador.velocidade[0], 2),
               round(self.game.jogador.velocidade[1], 2))

        dados_texto = f"""
        FPS: {self.game.relogio.get_fps():.2f} - Dt: {self.game.dt:.4f}
        Pos: {pos}
        Vel: {vel}
        Nums de chances: {self.game.derrotado}
        Transicao de fase: {self.game.transicao}
        """

        self.renderizar_customizado(display, dados_texto)

    def renderizar_customizado(self, display, dados_texto, posicao=(-30, -5)):
        """
        Renderiza textos customizados em uma posição específica.
        
        Args:
            display: Superfície pygame onde renderizar
            dados_texto: String ou lista de strings a renderizar
            posicao: Tupla (x, y) para posição inicial
        """
        if isinstance(dados_texto, str):
            dados_texto = [dados_texto]
        
        x, y = posicao
        for i, texto in enumerate(dados_texto):
            surf_texto = self.fonte.render(texto)[0]
            display.blit(surf_texto, (x, y + i * 15))


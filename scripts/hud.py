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
        fps = self.game.relogio.get_fps()
        pos_x = round(self.game.jogador.pos[0], 1)
        pos_y = round(self.game.jogador.pos[1], 1)
        vel_x = round(self.game.jogador.velocidade[0], 2)
        vel_y = round(self.game.jogador.velocidade[1], 2)
        
        # Criar strings de texto
        texto_fps = f'FPS: {fps:.2f}'
        texto_pos = f'Pos: ({pos_x}, {pos_y})'
        texto_vel = f'Vel: ({vel_x}, {vel_y})'
        texto_drr = f'Nums de chances: ({self.game.derrotado})'

        # Renderizar cada linha
        surf_fps = self.fonte.render(texto_fps)[0]
        surf_pos = self.fonte.render(texto_pos)[0]
        surf_vel = self.fonte.render(texto_vel)[0]
        surf_drr = self.fonte.render(texto_drr)[0]

        # Posicionar na tela (canto superior esquerdo com espaçamento)
        display.blit(surf_fps, (5, 5))
        display.blit(surf_pos, (5, 15))
        display.blit(surf_vel, (5, 25))
        display.blit(surf_drr, (5, 35))

    def renderizar_customizado(self, display, dados_texto, posicao=(5, 5)):
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


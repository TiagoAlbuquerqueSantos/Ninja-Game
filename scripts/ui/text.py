from pygame import Color
from pgbitmapfont import BitmapFont

from scripts.paths import FONTS_ASSETS
from scripts.constants import TAM_FONTE, Cores


class Text:
    def __init__(self, conteudo, surf, pos, cor=Cores.AZUL, estilo_fonte='small_font'):
        self.conteudo = conteudo
        self.fonte = BitmapFont(
            path=FONTS_ASSETS / f'{estilo_fonte}.json',
            site=TAM_FONTE,
            fgcolor=Color(cor),
            spacing=(1, 1)
        )

        self._render(surf, pos)

    def _render(self, surf, pos):
        surf_texto = self.fonte.render(self.conteudo)[0]
        surf.blit(surf_texto, pos)
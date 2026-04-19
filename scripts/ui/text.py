from pygame import Color, Surface
from pgbitmapfont import BitmapFont

from scripts.paths import FONTS_ASSETS
from scripts.constants import TAM_FONTE


class Text:
    def __init__(
            self,
            conteudo: str,
            surf: Surface,
            pos: tuple[int, int],
            cor: tuple[int, int, int],
            estilo_fonte: str = 'small_font'
    ) -> None:
        self.conteudo = conteudo
        self.fonte = BitmapFont(
            path=FONTS_ASSETS / f'{estilo_fonte}.json',
            size=TAM_FONTE,
            fgcolor=Color(cor),
            spacing=(1, 1)
        )

        self._render(surf, pos)

    def _render(self, surf: Surface, pos: tuple[int, int]) -> None:
        surf_texto = self.fonte.render(self.conteudo)[0]
        surf.blit(surf_texto, pos)
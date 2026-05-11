from pygame import Color, Surface
from pgbitmapfont import BitmapFont

from ..paths import FONTS_ASSETS
from ..constants import TAM_FONTE, Cores

#TODO: Refatorar essa classe para melhorar o desempenho, criando uma instânsia do Text no construtor e usando o render apenas na função de renderizar.
class Text:
    def __init__(
            self,
            conteudo: str,
            surf: Surface,
            pos: tuple[int, int],
            cor: tuple[int, int, int],
            tamanho: int = TAM_FONTE,
            estilo_fonte: str = 'small_font'
    ) -> None:
        self.conteudo = conteudo
        self.fonte = BitmapFont(
            path=FONTS_ASSETS / f'{estilo_fonte}.json',
            size=tamanho,
            fgcolor=Color(cor),
            spacing=(1, 1)
        )

        self._render(surf, pos)

    def _render(self, surf: Surface, pos: tuple[int, int]) -> None:
        surf.blit(self.fonte.render(self.conteudo)[0], pos)


class TextoTitulo(Text):
    def __init__(
            self,
            conteudo: str,
            surf: Surface,
            pos: tuple[int, int]
    ) -> None:
        super().__init__(
            conteudo,
            surf,
            pos=pos,
            cor=Cores.BRANCO,
            tamanho=TAM_FONTE * 2,
            estilo_fonte='good_neighbours_font'
        )

    def _render(self, surf: Surface, pos: tuple[int, int]) -> None:
        surf_texto = self.fonte.render(self.conteudo)[0]
        rect_texto = surf_texto.get_rect(center=pos)
        surf.blit(surf_texto, rect_texto)

import pygame


class HUD:
    """
    HUD simples que desenha uma barra de vida.
    Pode ser ligado a um objeto `player` que possua atributos `health` e `max_health`
    (ou `hp` e `max_hp`). Também permite controlar saúde manualmente.

    Esta versão mantém todas as posições/dimensões em unidades lógicas (a mesma
    resolução usada pelo jogo — `RES_DISPLAY`) e garante que a fonte seja criada
    com tamanho proporcional à altura da barra para que fique visualmente
    consistente com os sprites do jogo. Também aceita um `font_path` opcional
    para usar uma fonte pixel art do projeto.
    """
    def __init__(self, player=None, pos=(10, 10), size=(200, 20),
                 bg_color=(40, 40, 40), fg_color=(200, 30, 30),
                 border_color=(255, 255, 255), font_size=None, padding=2, font_path=None):
        self.player = player
        self.x, self.y = int(pos[0]), int(pos[1])
        self.width, self.height = int(size[0]), int(size[1])
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.border_color = border_color
        self.padding = int(padding)

        # valores padrão; serão atualizados por update_from_player se ligado
        self.max_health = 100
        self.current_health = 100

        # fonte lazy-init no primeiro draw (garante que pygame.font foi inicializado)
        self._font = None
        # se nenhum font_size for provido, calcula um tamanho proporcional à altura
        if font_size is None:
            # queremos que o texto caiba confortavelmente dentro da barra
            # normalmente cerca de 60-80% da altura da barra funciona bem
            self._font_size = max(8, int(round(self.height * 0.75)))
        else:
            self._font_size = int(font_size)
        self._font_path = font_path

    def link_player(self, player):
        """Associar um objeto player para ler health/max_health automaticamente."""
        self.player = player
        self.update_from_player()

    def update_from_player(self):
        """Lê atributos do player (se existir). Aceita nomes comuns."""
        if not self.player:
            return
        # tenta vários nomes comuns para HP
        cur = getattr(self.player, "health", None)
        if cur is None:
            cur = getattr(self.player, "hp", None)
        maxh = getattr(self.player, "max_health", None)
        if maxh is None:
            maxh = getattr(self.player, "max_hp", None)

        if cur is not None:
            self.current_health = cur
        if maxh is not None:
            self.max_health = maxh

    def set_health(self, value):
        self.current_health = max(0, value)

    def set_max_health(self, value):
        self.max_health = max(1, value)
        # garante que current <= max
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def _ensure_font(self):
        if self._font is None:
            if not pygame.font.get_init():
                pygame.font.init()
            # usa font_path se fornecido, caso contrário fonte padrão
            try:
                self._font = pygame.font.Font(self._font_path, self._font_size)
            except Exception:
                # fallback para fonte padrão caso o path falhe
                self._font = pygame.font.Font(None, self._font_size)

    def rescale(self, pos=None, size=None, padding=None, font_size=None):
        """Recalcula posições/dimensões — útil se o sistema de resolução lógica mudar.

        Todos os valores esperados são em coordenadas lógicas (mesma unidade usada
        para desenhar sprites). Chamadores podem fornecer apenas os valores que
        querem alterar.
        """
        if pos is not None:
            self.x, self.y = int(pos[0]), int(pos[1])
        if size is not None:
            self.width, self.height = int(size[0]), int(size[1])
        if padding is not None:
            self.padding = int(padding)
        if font_size is not None:
            self._font_size = int(font_size)
        # invalida a fonte para que seja recriada com novo tamanho
        self._font = None

    def draw(self, surface):
        """
        Desenha a barra no surface (ex.: a tela do pygame).
        Deve ser chamado dentro do loop principal após atualizar jogador.
        """
        # atualiza a partir do player se estiver linkado
        if self.player:
            self.update_from_player()

        # evita divisão por zero
        max_hp = max(1, self.max_health)
        cur_hp = max(0, min(self.current_health, max_hp))
        ratio = float(cur_hp) / float(max_hp)

        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        inner_x = self.x + self.padding
        inner_y = self.y + self.padding
        inner_w = max(0, self.width - 2 * self.padding)
        inner_h = max(1, self.height - 2 * self.padding)

        # fundo
        pygame.draw.rect(surface, self.bg_color, bg_rect)

        # preenchimento proporcional
        fill_w = int(round(inner_w * ratio))
        fill_rect = pygame.Rect(inner_x, inner_y, fill_w, inner_h)
        pygame.draw.rect(surface, self.fg_color, fill_rect)

        # contorno (1 ou 2px) — mantém aparência nítida em resolução lógica
        pygame.draw.rect(surface, self.border_color, bg_rect, 2)

        # texto de HP (ex.: 75/100)
        self._ensure_font()
        text = f"{int(cur_hp)}/{int(max_hp)}"
        text_surf = self._font.render(text, True, self.border_color)
        # centraliza dentro do bg_rect
        text_rect = text_surf.get_rect(center=bg_rect.center)
        surface.blit(text_surf, text_rect)


# Uso (exemplo mínimo, integrar no loop do jogo):
# hud = HUD(player=player, pos=(10,10), size=(220,24), font_path='data/fonts/pocketpixel.ttf')
# no loop:
#    hud.draw(screen)
#    pygame.display.flip()

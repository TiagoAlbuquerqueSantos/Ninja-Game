import pygame


class LevelDisplay:
    """
    Exibe um pop-up mostrando o nível atual com bordas, sombra e tempo de exibição.
    
    O pop-up aparece no centro da tela e desaparece automaticamente após o tempo
    especificado (padrão: 180 frames = 3 segundos em 60 FPS).
    Inclui animação de entrada de cima para baixo.
    """
    def __init__(self, nivel=1, tempo_exibicao=180, font_path=None, 
                 tamanho_fonte=None, cor_texto=(255, 255, 255),
                 cor_fundo=(40, 40, 40), cor_borda=(255, 255, 255),
                 tempo_animacao=30):
        self.nivel = nivel
        self.tempo_exibicao = tempo_exibicao
        self.tempo_restante = tempo_exibicao
        self.tempo_animacao = tempo_animacao  # Frames para animar entrada
        self.tempo_animacao_restante = tempo_animacao
        self.font_path = font_path
        self.tamanho_fonte = tamanho_fonte
        self.cor_texto = cor_texto
        self.cor_fundo = cor_fundo
        self.cor_borda = cor_borda
        
        self._font = None
        self.ativo = True
        
    def _ensure_font(self):
        """Inicializa a fonte se não estiver criada."""
        if self._font is None:
            if not pygame.font.get_init():
                pygame.font.init()
            
            tamanho = self.tamanho_fonte or 32
            try:
                self._font = pygame.font.Font(self.font_path, tamanho)
            except Exception:
                self._font = pygame.font.Font(None, tamanho)
    
    def atualizar(self):
        """Atualiza o contador de tempo."""
        if self.ativo:
            self.tempo_restante -= 1
            if self.tempo_animacao_restante > 0:
                self.tempo_animacao_restante -= 1
            if self.tempo_restante <= 0:
                self.ativo = False
    
    def desenhar(self, surface):
        """
        Desenha o pop-up no centro da tela com animação de entrada.

        Args:
            surface: Surface do pygame onde desenhar
        """
        if not self.ativo:
            return
        
        self._ensure_font()
        
        # Renderiza o texto
        texto = f"LEVEL {self.nivel}"
        texto_surf = self._font.render(texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect()
        
        # Define dimensões da caixa com padding
        padding = 20
        box_width = texto_rect.width + padding * 2
        box_height = texto_rect.height + padding * 2
        
        # Posiciona no centro da tela
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2

        # Calcula a posição com animação de entrada
        # A animação começa com tempo_animacao_restante = tempo_animacao
        # e vai até 0. Quanto maior o tempo restante, mais para cima fica
        if self.tempo_animacao_restante > 0:
            progresso = 1 - (self.tempo_animacao_restante / self.tempo_animacao)
            # Deslocamento vertical: começa fora da tela (no topo) até o centro
            screen_height = surface.get_height()
            deslocamento_y = -screen_height / 2 + (screen_height / 2) * progresso
        else:
            deslocamento_y = 0

        box_x = center_x - box_width // 2
        box_y = center_y - box_height // 2 + deslocamento_y

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        # Desenha a sombra (deslocada 4px para baixo-direita)
        shadow_offset = 4
        shadow_surf = pygame.Surface((box_width, box_height))
        shadow_surf.set_colorkey((0, 0, 0))
        shadow_surf.fill((0, 0, 0))

        # Desenha a sombra com alpha (se possível)
        shadow_rect = box_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        
        # Cria uma superfície temporária para a sombra semi-transparente
        shadow_temp = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_temp, (0, 0, 0, 80), shadow_temp.get_rect())
        surface.blit(shadow_temp, shadow_rect)
        
        # Desenha o fundo da caixa
        pygame.draw.rect(surface, self.cor_fundo, box_rect)
        
        # Desenha a borda (3px de espessura)
        pygame.draw.rect(surface, self.cor_borda, box_rect, 3)
        
        # Desenha o texto no centro da caixa
        texto_x = center_x - texto_rect.width // 2
        texto_y = center_y - texto_rect.height // 2 + deslocamento_y
        surface.blit(texto_surf, (texto_x, texto_y))
        
        # Efeito de fade out nos últimos 30 frames
        fade_duration = 30
        if self.tempo_restante < fade_duration:
            alpha = int(255 * (self.tempo_restante / fade_duration))
            fade_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            fade_surf.fill((0, 0, 0, 255 - alpha))
            surface.blit(fade_surf, box_rect)


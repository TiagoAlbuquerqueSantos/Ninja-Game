
import pygame
from .state import State
from ..ui import TextoTitulo, Text
from scripts.constants import Cores, LARGURA, ALTURA


class Menu(State):
    def __init__(self):
        super().__init__()
        self.proximo = 'scene'
        self.selecao_index = 0
        self.opcoes = ['Start Game', 'Quit']

    def checar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.sair = True
            elif evento.key == pygame.K_UP:
                self.selecao_index = (self.selecao_index - 1) % len(self.opcoes)
            elif evento.key == pygame.K_DOWN:
                self.selecao_index = (self.selecao_index + 1) % len(self.opcoes)
            elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                if self.selecao_index == 0:
                    self.feito = True
                else:
                    self.sair = True

    def atualizar(self, dt, tempo):
        pass

    def renderizar(self, surf):
        surf.fill((20, 20, 40))

        #TODO: Interpolar a posição do título para melhorar a animação de entrada do menu.
        TextoTitulo("Ninja Game", surf, (LARGURA // 2, ALTURA // 4))

        #TODO: Ajustar a posição do texto para centralizar melhor, considerando o tamanho do texto.
        for i, opcao in enumerate(self.opcoes):
            cor = Cores.AMARELO if i == self.selecao_index else Cores.BRANCO

            Text(opcao, surf, (LARGURA // 2, ALTURA // 2 + i * 40), cor)


import sys
import pygame
import asyncio
import logging

from scripts.constants import *
from scripts.engine import Engine
from scripts.states import Splash, Scene, Menu
from scripts.log import setup_logger

logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(LEGENDA)
        self.tela = pygame.display.set_mode(RES_TELA)
       # self.display = pygame.Surface((DISPLAY_L, DISPLAY_A))
        self.relogio = pygame.time.Clock()
        self.dt = 0.1

        self.rodando = True

        state_dict = {
            'splash': Splash(),
            'menu': Menu(),
            'scene': Scene(),
        }

        self.engine = Engine(self)
        self.engine.setup_states(state_dict, 'scene')

    def atualizar(self):
        self.engine.atualizar(self.dt, 0)

    def renderizar(self):
        self.engine.renderizar(self.tela)
       # self.tela.blit(pygame.transform.scale(self.display, RES_TELA), (0, 0))

    def checar_eventos(self):
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.rodando = False

        self.engine.eventos_engine(eventos)

    async def rodar(self):
        try:
            while self.rodando:
                self.checar_eventos()
                self.atualizar()
                self.renderizar()
                pygame.display.update()

                self.dt = self.relogio.tick(FPS) / 1000.0
                await asyncio.sleep(0)

        except Exception as e:
            logger.error(e)
        finally:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    setup_logger()
    asyncio.run(Game().rodar())

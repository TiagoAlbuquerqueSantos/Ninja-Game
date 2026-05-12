
import sys
import pygame
import asyncio
import logging

from os import environ

from scripts.constants import *
from scripts.engine import Engine
from scripts.states import Splash, Scene, Menu
from scripts.log import setup_logger

FLAGS_TELA = pygame.SCALED | pygame.RESIZABLE

logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        pygame.init()
        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption(LEGENDA)
        self.tela = pygame.display.set_mode(RES_TELA, FLAGS_TELA, vsync=True)
        self.relogio = pygame.time.Clock()
        self.dt = 0.1

        self.rodando = True
        self.tela_cheia = False

        state_dict = {
            'splash': Splash(),
            'menu': Menu(),
            'scene': Scene(),
        }

        self.engine = Engine(self)
        self.engine.setup_states(state_dict, 'splash')

    def atualizar(self):
        self.engine.atualizar(self.dt, 0)

    def renderizar(self):
        self.engine.renderizar(self.tela)

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False
                elif evento.key == pygame.K_F11:
                    self.tela_cheia = not self.tela_cheia
                    if self.tela_cheia:
                        pygame.display.set_mode(RES_TELA, FLAGS_TELA | pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode(RES_TELA, FLAGS_TELA)
            self.engine.eventos_engine(evento)

        # Verifica se deve sair da aplicação
        if self.engine.estado.sair:
            self.rodando = False

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

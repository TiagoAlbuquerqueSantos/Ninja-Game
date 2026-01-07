
import sys
import pygame
import asyncio
import logging

from scripts.constants import *

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)

logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(LEGENDA)
        self.tela = pygame.display.set_mode(RES_TELA)
        self.display = pygame.Surface((DISPLAY_L, DISPLAY_A))
        self.relogio = pygame.time.Clock()
        self.dt = 0.1

        self.rodando = True

    def atualizar(self):
        pass

    def renderizar(self):
        self.tela.blit(pygame.transform.scale(self.display, RES_TELA), (0, 0))

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
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
            self.finalizar()

    @staticmethod
    def finalizar():
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = Game()
    asyncio.run(app.rodar())

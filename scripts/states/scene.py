
import pygame

from pytmx.util_pygame import load_pygame
from pygame.sprite import Group

from .state import State
from ..objects import Tile
from scripts import paths


class Scene(State):
    def __init__(self):
        super().__init__()
        self.proximo = None
        self.pos_jogador = [0, 0]

        self.sprites = Group()
        self.sprites_colisao = Group()

        self.carregar_tilemap()

    def carregar_tilemap(self):
        dados_mapa = load_pygame(str(paths.MAPS_PATH / f'teste.tmx'))
        tilesize = dados_mapa.tilewidth

        terreno = dados_mapa.get_layer_by_name('terreno')
        for x, y, gid, in terreno:  # type: ignore
            tile = dados_mapa.get_tile_image_by_gid(gid)
            if tile:
                Tile([self.sprites, self.sprites_colisao],
                     (x * tilesize, y * tilesize), tile)

        decor = dados_mapa.get_layer_by_name('decoracoes')
        for x, y, gid, in decor:  # type: ignore
            tile = dados_mapa.get_tile_image_by_gid(gid)
            if tile:
                Tile([self.sprites],
                     (x * tilesize, y * tilesize), tile)

        decor_grande = dados_mapa.get_layer_by_name('decor_grande')
        for obj in decor_grande:  # type: ignore
            Tile([self.sprites], (obj.x, obj.y), obj.image)

        pontos_entidades = dados_mapa.get_layer_by_name(
            'pontos_entidades')
        for obj in pontos_entidades:  # type: ignore
            if obj.name == 'jogador':
                self.pos_jogador = [obj.x, obj.y]
            else:
                pass

    def checar_evento(self, eventos):
        pass

    def atualizar(self, dt, tempo):
        self.sprites.update()

    def renderizar(self, surf):
        surf.fill((0, 0, 50))
        self.sprites.draw(surf)

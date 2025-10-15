import json

import pygame

AUTOTILE_MAPA = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1),
                    (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
COLISAO_TILES = {'grama', 'pedra'}
TIPOS_AUTOTILE = {'grama', 'pedra'}


class Tilemap:
    def __init__(self, main, tamanho_tile=16):
        self.main = main
        self.tamanho_tile = tamanho_tile
        self.tilemap = {}
        self.offgrid_tiles = []

    def extrair(self, id_pares, manter=False):
        partidas = []
        for tile in self.offgrid_tiles.copy():
            if (tile['tipo'], tile['variante']) in id_pares:
                partidas.append(tile.copy())
                if not manter:
                    self.offgrid_tiles.remove(tile)
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['tipo'], tile['variante']) in id_pares:
                partidas.append(tile.copy())
                partidas[-1]['pos'] = partidas[-1]['pos'].copy()
                partidas[-1]['pos'][0] *= self.tamanho_tile
                partidas[-1]['pos'][1] *= self.tamanho_tile
                if not manter:
                    del self.tilemap[loc]
        return partidas

    def tiles_aoredor(self, pos):
        tiles = []
        loc_tile = (int(pos[0] // self.tamanho_tile),
                    int(pos[1] // self.tamanho_tile))
        for desvio in NEIGHBOR_OFFSETS:
            checar_loc = str(loc_tile[0] + desvio[0]) + \
                ';' + str(loc_tile[1] + desvio[1])
            if checar_loc in self.tilemap:
                tiles.append(self.tilemap[checar_loc])
        return tiles

    def salvar(self, caminho):
        arquivo = open(caminho, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tamanho_tile,
                  'offgrid': self.offgrid_tiles}, arquivo)
        arquivo.close()

    def carregar(self, caminho):
        arquivo = open(caminho, 'r')
        dados_mapa = json.load(arquivo)
        arquivo.close()

        self.tilemap = dados_mapa['tilemap']
        self.tamanho_tile = dados_mapa['tile_size']
        self.offgrid_tiles = dados_mapa['offgrid']

    def checar_solido(self, pos):
        loc_tile = str(int(pos[0] // self.tamanho_tile)) + \
            ';' + str(int(pos[1] // self.tamanho_tile))
        if loc_tile in self.tilemap:
            if self.tilemap[loc_tile]['tipo'] in COLISAO_TILES:
                return self.tilemap[loc_tile]

    def colisao_rects_aoredor(self, pos):
        retangulos = []
        for tile in self.tiles_aoredor(pos):
            if tile['tipo'] in COLISAO_TILES:
                retangulos.append(pygame.Rect(
                    tile['pos'][0] * self.tamanho_tile, tile['pos'][1] * self.tamanho_tile, self.tamanho_tile, self.tamanho_tile))
        return retangulos

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            vizinhos = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                checar_loc = str(tile['pos'][0] + shift[0]) + \
                    ';' + str(tile['pos'][1] + shift[1])
                if checar_loc in self.tilemap:
                    if self.tilemap[checar_loc]['tipo'] == tile['tipo']:
                        vizinhos.add(shift)
            vizinhos = tuple(sorted(vizinhos))
            if (tile['tipo'] in TIPOS_AUTOTILE) and (vizinhos in AUTOTILE_MAPA):
                tile['variante'] = AUTOTILE_MAPA[vizinhos]

    def renderizar(self, surf, deslocamento=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.main.assets[tile['tipo']][tile['variante']], (tile['pos'][0] - deslocamento[0],
                                                                         tile['pos'][1] - deslocamento[1]))

        for x in range(deslocamento[0] // self.tamanho_tile,
                       (deslocamento[0] + surf.get_width()) // self.tamanho_tile + 1):
            for y in range(deslocamento[1] // self.tamanho_tile,
                           (deslocamento[1] + surf.get_height()) // self.tamanho_tile + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.main.assets[tile['tipo']][tile['variante']],
                              (tile['pos'][0] * self.tamanho_tile - deslocamento[0],
                               tile['pos'][1] * self.tamanho_tile - deslocamento[1]))

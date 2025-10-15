import sys

import pygame

from tkinter import Tk, filedialog

from scripts.utils import carregar_imagens
from scripts.tilemap import Tilemap

ESCALA_RENDER = 2.0


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Editor de Levels')
        self.tela = pygame.display.set_mode((1280, 720))
        self.display = pygame.Surface((640, 360))
        self.relogio = pygame.time.Clock()

        self.mpos = None; self.camera = None; self.pos_tile = None

        self.assets = {
            'decor': carregar_imagens('tiles/decor'),
            'grama': carregar_imagens('tiles/grass'),
            'decor_larga': carregar_imagens('tiles/large_decor'),
            'pedra': carregar_imagens('tiles/stone'),
            'geradores': carregar_imagens('tiles/spawners')
        }

        self.movimento = [False, False, False, False]

        self.mapa_jogo = Tilemap(self, tamanho_tile=16)
        self.tamanho_tile = self.mapa_jogo.tamanho_tile

        try:
            self.mapa_jogo.carregar('mapa.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.selecao = [None, None]

        self.lista_tiles = list(self.assets)
        self.grupo_tile = 0
        self.variante_tile = 0

        self.clique = False
        self.clique_direito = False
        self.shift = False
        self.grid_ativo = True

    def pesquisar_mapas(self):
        janela = Tk()
        janela.withdraw()
        nome_arquivo = filedialog.askopenfilename(
            initialdir='', title='Selecionar Mapa',
            filetypes=(('mapas json', '*.json'), ('todos os arquivos', '*.*')))
        if nome_arquivo != '':
            self.mapa_jogo.carregar(nome_arquivo)

    # ------------------------------- Interfaçe Visual --------------------------------------------
    def renderizar_tile_atual(self):
        img_tile = self.assets[self.lista_tiles[self.grupo_tile]][self.variante_tile].copy()
        img_tile.set_alpha(128)
        self.display.blit(img_tile, (5, 5))
        if not self.grid_ativo:
            self.display.blit(img_tile, self.mpos)
        else:
            pos = (self.pos_tile[0] * self.tamanho_tile - self.scroll[0],
                   self.pos_tile[1] * self.tamanho_tile - self.scroll[1])
            self.display.blit(img_tile, pos)
            pygame.draw.rect(self.display, (255, 255, 255), (pos[0], pos[1], self.tamanho_tile, self.tamanho_tile), 1)

    def desenhar_sidebar(self):
        surf_sidebar = pygame.Surface((70, self.display.get_height()), pygame.SRCALPHA)
        surf_sidebar.fill((0, 40, 60, 180))

        pygame.draw.line(surf_sidebar, (0, 255, 120), (0, 0), (0, surf_sidebar.get_height()))
        pygame.draw.line(surf_sidebar, (0, 255, 120), (0, 70), (surf_sidebar.get_width(), 70))
        self.display.blit(surf_sidebar, (self.display.get_width() - 70, 0))

    def grids_editor(self):
        deslocamento_grid = (self.scroll[0] % self.tamanho_tile, self.scroll[1] % self.tamanho_tile)
        surf_grid = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)

        pygame.draw.line(surf_grid, (0, 255, 255),
                         (-self.scroll[0], 0), (-self.scroll[0], self.display.get_height()), 3)
        pygame.draw.line(surf_grid, (0, 255, 255),
                         (0, -self.scroll[1]), (self.display.get_width(), -self.scroll[1]), 3)

        # Linhas Horizontais
        for x in range(self.display.get_width() // self.tamanho_tile + 1):
            pygame.draw.line(surf_grid, (100, 100, 100, 180), (x * self.tamanho_tile - deslocamento_grid[0], 0),
                             (x * self.tamanho_tile - deslocamento_grid[0], self.display.get_height()))
        # Linhas Verticais
        for y in range(self.display.get_height() // self.tamanho_tile + 1):
            pygame.draw.line(surf_grid, (100, 100, 100), (0, y * self.tamanho_tile - deslocamento_grid[1]),
                             (self.display.get_width(), y * self.tamanho_tile - deslocamento_grid[1]))

        surf_grid.set_alpha(100)
        self.display.blit(surf_grid, (0, 0))

    # ---------------------------------------------------------------------------------------------

    def alterar_tile_atual(self, evento):
        if self.shift:
            if evento.button == 4:
                self.variante_tile = (self.variante_tile - 1) % len(self.assets[self.lista_tiles[self.grupo_tile]])
            if evento.button == 5:
                self.variante_tile = (self.variante_tile + 1) % len(self.assets[self.lista_tiles[self.grupo_tile]])
        else:
            if evento.button == 4:
                self.grupo_tile = (self.grupo_tile - 1) % len(self.lista_tiles)
                self.variante_tile = 0
            if evento.button == 5:
                self.grupo_tile = (self.grupo_tile + 1) % len(self.lista_tiles)
                self.variante_tile = 0

    def adicionar_tiles(self):
        pos_offgrid = (self.mpos[0] + self.scroll[0], self.mpos[1] + self.scroll[1])
        tipo_tile_atual = self.lista_tiles[self.grupo_tile]
        if self.clique and self.grid_ativo:
            self.mapa_jogo.tilemap[str(self.pos_tile[0]) + ';' + str(self.pos_tile[1])] =\
                {'tipo': tipo_tile_atual, 'variante': self.variante_tile, 'pos': self.pos_tile}

        if self.clique and not self.grid_ativo:
            self.clique = False
            self.mapa_jogo.offgrid_tiles.append(
                {'tipo': tipo_tile_atual, 'variante': self.variante_tile, 'pos': pos_offgrid})

    def remover_tiles(self):
        if self.clique_direito:
            loc_tile = str(self.pos_tile[0]) + ';' + str(self.pos_tile[1])
            if loc_tile in self.mapa_jogo.tilemap:
                del self.mapa_jogo.tilemap[loc_tile]
            for tile in self.mapa_jogo.offgrid_tiles.copy():
                img_tile = self.assets[tile['tipo']][tile['variante']]
                r_tile = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                     img_tile.get_width(), img_tile.get_height())
                if r_tile.collidepoint(self.mpos):
                    self.mapa_jogo.offgrid_tiles.remove(tile)

    def movimento_camera(self):
        self.scroll[0] += (self.movimento[1] - self.movimento[0]) * 5
        self.scroll[1] += (self.movimento[3] - self.movimento[2]) * 5
        self.camera = (int(self.scroll[0]), int(self.scroll[1]))

    def mouse_tile_pos(self):
        self.mpos = pygame.mouse.get_pos()
        self.mpos = (self.mpos[0] / ESCALA_RENDER, self.mpos[1] / ESCALA_RENDER)
        self.pos_tile = (int((self.mpos[0] + self.scroll[0]) // self.tamanho_tile),
                         int((self.mpos[1] + self.scroll[1]) // self.tamanho_tile))

    def atualizar(self):
        self.movimento_camera()
        self.mouse_tile_pos()
        self.adicionar_tiles()
        self.remover_tiles()

    def renderizar(self):
        self.display.fill((0, 0, 0))
        self.mapa_jogo.renderizar(self.display, deslocamento=self.camera)
        self.grids_editor()
       # self.desenhar_sidebar()
        self.renderizar_tile_atual()

        self.tela.blit(pygame.transform.scale(
        self.display, self.tela.get_size()), (0, 0))
        pygame.display.update()
        self.relogio.tick(60)

    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.clique = True
                elif evento.button == 3:
                    self.clique_direito = True
                self.alterar_tile_atual(evento=evento)
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    self.clique = False
                elif evento.button == 3:
                    self.clique_direito = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    self.movimento[0] = True
                elif evento.key == pygame.K_d:
                    self.movimento[1] = True
                elif evento.key == pygame.K_w:
                    self.movimento[2] = True
                elif evento.key == pygame.K_s:
                    self.movimento[3] = True
                elif evento.key == pygame.K_LSHIFT:
                    self.shift = True
                elif evento.key == pygame.K_g:
                    self.grid_ativo = not self.grid_ativo
                elif evento.key == pygame.K_t:
                    self.mapa_jogo.autotile()
                elif evento.key == pygame.K_o:
                    self.mapa_jogo.salvar('mapa.json')
                elif evento.key == pygame.K_p:
                    self.pesquisar_mapas()
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_a:
                    self.movimento[0] = False
                elif evento.key == pygame.K_d:
                    self.movimento[1] = False
                elif evento.key == pygame.K_w:
                    self.movimento[2] = False
                elif evento.key == pygame.K_s:
                    self.movimento[3] = False
                elif evento.key == pygame.K_LSHIFT:
                    self.shift = False

    def rodar(self):
        while True:
            self.checar_eventos()
            self.atualizar()
            self.renderizar()

if __name__ == '__main__':
    Editor().rodar()

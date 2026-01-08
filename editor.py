import sys

import pygame

from tkinter import Tk, filedialog

from scripts.editor_config import *
from scripts.utils import carregar_imagens
from scripts.objects import Tilemap


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(LEGENDA)
        self.tela = pygame.display.set_mode(EDITOR_RES)
        self.display = pygame.Surface((DISPLAY_L, DISPLAY_A))
        self.relogio = pygame.time.Clock()

        self.rodando = True

        self.m_pos = None
        self.camera = None
        self.pos_tile = None

        self.assets = {
            'decor': carregar_imagens('tiles/decor'),
            'grama': carregar_imagens('tiles/grass'),
            'decor_larga': carregar_imagens('tiles/large_decor'),
            'pedra': carregar_imagens('tiles/stone'),
            'geradores': carregar_imagens('tiles/spawners')
        }

        self.movimento = [False, False, False, False]

        self.mapa_jogo = Tilemap(self, TILE_SIZE)

        try:
            self.mapa_jogo.carregar(NOME_SAVE)
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.lista_tiles = list(self.assets)
        self.grupo_tile = 0
        self.variante_tile = 0

        self.clique = False
        self.clique_direito = False
        self.shift = False
        self.grid_ativo = True

    def pesquisar_mapas(self):
        try:
            janela = Tk()
            janela.withdraw()
            nome_arquivo = filedialog.askopenfilename(
                initialdir='', title='Selecionar Mapa',
                filetypes=(('mapas json', '*.json'), ('todos os arquivos', '*.*')))
            if nome_arquivo != '':
                self.mapa_jogo.carregar(nome_arquivo)
        except Exception as e:
            print(f'Erro ao carregar mapa: {e}')

    # ------------------------------- Interfaçe Visual --------------------------------------------
    def renderizar_tile_atual(self, mpos, pos_tile):
        img_tile = self.assets[self.lista_tiles[self.grupo_tile]][self.variante_tile].copy()
        img_tile.set_alpha(128)
        self.display.blit(img_tile, POS_TILE_ATUAL)
        if not self.grid_ativo:
            self.display.blit(img_tile, mpos)
        else:
            pos = (pos_tile[0] * TILE_SIZE - self.scroll[0],
                   pos_tile[1] * TILE_SIZE - self.scroll[1])
            self.display.blit(img_tile, pos)
            pygame.draw.rect(self.display, BRANCO, (pos[0], pos[1], TILE_SIZE, TILE_SIZE), 1)

    def desenhar_sidebar(self):
        surf_sidebar = pygame.Surface((70, self.display.get_height()), pygame.SRCALPHA)
        surf_sidebar.fill((0, 40, 60, 180))

        pygame.draw.line(surf_sidebar, (0, 255, 120), (0, 0), (0, surf_sidebar.get_height()))
        pygame.draw.line(surf_sidebar, (0, 255, 120), (0, 70), (surf_sidebar.get_width(), 70))
        self.display.blit(surf_sidebar, (self.display.get_width() - 70, 0))

    def grids_editor(self):
        deslocamento_grid = (self.scroll[0] % TILE_SIZE, self.scroll[1] % TILE_SIZE)
        surf_grid = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)

        pygame.draw.line(surf_grid, (0, 255, 255),
                         (-self.scroll[0], 0), (-self.scroll[0], DISPLAY_A), 3)
        pygame.draw.line(surf_grid, (0, 255, 255),
                         (0, -self.scroll[1]), (DISPLAY_L, -self.scroll[1]), 3)

        # Linhas Horizontais
        for x in range(DISPLAY_L // TILE_SIZE + 1):
            pygame.draw.line(surf_grid, CINZA, (x * TILE_SIZE - deslocamento_grid[0], 0),
                             (x * TILE_SIZE - deslocamento_grid[0], DISPLAY_A))
        # Linhas Verticais
        for y in range(DISPLAY_A // TILE_SIZE + 1):
            pygame.draw.line(surf_grid, CINZA, (0, y * TILE_SIZE - deslocamento_grid[1]),
                             (DISPLAY_L, y * TILE_SIZE - deslocamento_grid[1]))

        surf_grid.set_alpha(TRANSPARENCIA_GRID)
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

    def adicionar_tiles(self, mpos, pos_tile):
        pos_offgrid = (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])
        tipo_tile_atual = self.lista_tiles[self.grupo_tile]
        if self.clique and self.grid_ativo:
            self.mapa_jogo.tilemap[str(pos_tile[0]) + ';' + str(pos_tile[1])] =\
                {'tipo': tipo_tile_atual, 'variante': self.variante_tile, 'pos': pos_tile}

        if self.clique and not self.grid_ativo:
            self.clique = False
            self.mapa_jogo.offgrid_tiles.append(
                {'tipo': tipo_tile_atual, 'variante': self.variante_tile, 'pos': pos_offgrid})

    def remover_tiles(self, mpos, pos_tile):
        if self.clique_direito:
            loc_tile = str(pos_tile[0]) + ';' + str(pos_tile[1])
            if loc_tile in self.mapa_jogo.tilemap:
                del self.mapa_jogo.tilemap[loc_tile]
            for tile in self.mapa_jogo.offgrid_tiles.copy():
                img_tile = self.assets[tile['tipo']][tile['variante']]
                r_tile = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                     img_tile.get_width(), img_tile.get_height())
                if r_tile.collidepoint(mpos):
                    self.mapa_jogo.offgrid_tiles.remove(tile)

    def movimento_camera(self):
        self.scroll[0] += (self.movimento[1] - self.movimento[0]) * VEL_CAMERA
        self.scroll[1] += (self.movimento[3] - self.movimento[2]) * VEL_CAMERA
        self.camera = (int(self.scroll[0]), int(self.scroll[1]))

    def mouse_tile_pos(self):
        mpos = pygame.mouse.get_pos()
        mpos = (mpos[0] / ESCALA_RENDER, mpos[1] / ESCALA_RENDER)
        pos_tile = (int((mpos[0] + self.scroll[0]) // TILE_SIZE),
                    int((mpos[1] + self.scroll[1]) // TILE_SIZE))
        return mpos, pos_tile

    def atualizar(self):
        self.movimento_camera()
        self.m_pos, self.pos_tile = self.mouse_tile_pos()
        self.adicionar_tiles(self.m_pos, self.pos_tile)
        self.remover_tiles(self.m_pos, self.pos_tile)

    def renderizar(self):
        self.display.fill(PRETO)
        self.mapa_jogo.renderizar(self.display, deslocamento=self.camera)
        self.grids_editor()
        #self.desenhar_sidebar()
        self.renderizar_tile_atual(self.m_pos, self.pos_tile)

        self.tela.blit(pygame.transform.scale(
        self.display, self.tela.get_size()), (0, 0))


    def checar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
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
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False
                elif evento.key == pygame.K_a:
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
                    self.mapa_jogo.salvar(NOME_SAVE)
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
        while self.rodando:
            self.checar_eventos()
            self.atualizar()
            self.renderizar()
            pygame.display.update()
            self.relogio.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Editor().rodar()


RES_TELA = LARGURA, ALTURA = 640, 480
DISPLAY_L, DISPLAY_A = 320, 240
LEGENDA = 'Ninja Game'
FPS = 60

LEVEL = 0
TILE_SIZE = 16

NUM_NUVENS = 16

TAM_FONTE = 8
COR_FONTE = (255, 0, 0)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (100, 100, 100)
AMARELO = (255, 255, 0)
CIANO = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Parâmetros do jogador
POSICAO = (50, 50)
HIT_BOX = (8, 15)
VEL_MAX_QUEDA = 5
FORCA_PULO = 3

# Volume de áudio
MUSICA_FUNDO = 1
AMBIENTE = 0.2
TIRO = 0.4
HIT = 0.8
REPULSIVE = 0.3
PULO = 0.7


# Parâmetros do tilemap
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


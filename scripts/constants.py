
RES_TELA = LARGURA, ALTURA = 960, 540
DISPLAY_L, DISPLAY_A = LARGURA // 2, ALTURA // 2
CENTRO_TELA = DISPLAY_L // 2, DISPLAY_A // 2
LEGENDA = 'Ninja Game'
FPS = 60

LEVEL = 0
TILE_SIZE = 16

NUM_NUVENS = 16

TAM_FONTE = 8

RAIO_TRANSICAO = 50

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

VOLUME_AUDIO = {
    'ambience': 0.2,
    'shoot': 0.4,
    'jump': 0.7,
    'dash': 0.3,
    'hit': 0.8,
    'music': 1,
}

# Camera
ACE_CAMERA = 30

# Propriedades de Partícula e Faisca
NUMS_FAISCA_PAREDE = 4
NUMS_FAISCA_DERROTADO = 30
NUMS_PARTICULAS_ATAQUE = 30


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

DESLOCAMENTO_ANIM = -3

VEL_PROJETIL = 140
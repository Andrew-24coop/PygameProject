import random

WIDTH, HEIGHT = 1000, 600
BOSS_WIDTH, BOSS_HEIGHT = 250, 200
SIZE = (WIDTH, HEIGHT)
TILE_SIZE = 1
CHUNK_SIZE = 50

FPS = 60
MAIN_SEED = random.randint(0, 255)
BOSS_SEED = random.randint(0, 255)

MAIN_COLORS = {
    "ocean": (0, 0, 255),
    "sand": (194, 178, 128),
    "grass": (34, 139, 34),
    "forest": (0, 100, 0),
    "mountain": (139, 137, 137)
}

BOSS_COLORS = {
    "ocean": (143, 54, 23),
    "sand": (99, 77, 57),
    "grass": (89, 80, 78),
    "forest": (49, 47, 47),
    "mountain": (0, 0, 0)
}

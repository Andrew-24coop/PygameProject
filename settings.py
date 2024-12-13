import random

WIDTH, HEIGHT = 1000, 600
SIZE = (WIDTH, HEIGHT)
TILE_SIZE = 1

FPS = 30
SEED = random.randint(0, 255)

COLORS = {
    "ocean": (0, 0, 255),
    "sand": (194, 178, 128),
    "grass": (34, 139, 34),
    "forest": (0, 100, 0),
    "mountain": (139, 137, 137)
}

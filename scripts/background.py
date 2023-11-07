import pygame
import scripts.settings as settings
from os.path import join

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(settings.WIDTH // width + 1):
        for j in range(settings.HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image
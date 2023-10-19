import pygame
import settings
from os.path import join



def get_block(width, height, name):
    name = name+".png" if name != None else "Block.png"
    path = join("assets", "Terrain", name )
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, width, height)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)



class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Block(Object):
    def __init__(self, x, y, width, height, name=None):
        super().__init__(x, y, width, height)
        self.block = get_block(width, height, name)
        self.image.blit(self.block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        
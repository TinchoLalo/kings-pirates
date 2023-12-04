import pygame
import scripts.settings as settings
from os.path import join



def get_block(width, height,pos, name):
    #name = name+".png" if name != None else "Block.png"
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    rect = pygame.Rect(pos[0], pos[1], width, height)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)



class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, pos=[0,0], name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        self.pos = pos

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Block(Object):
    def __init__(self, x, y, width, height, pos=[0,0], name=None):
        super().__init__(x, y, width, height)
        self.block = get_block(width, height, pos, name)
        self.image.blit(self.block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = name
        
class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.image = pygame.image.load("assets/Decorations/"+name+".png")
        self.image = pygame.transform.scale(self.image, (width*2, height*2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name

    def update_name(self, name):
        self.name = name
        self.image = pygame.image.load("assets/Decorations/"+name+".png")
        self.image = pygame.transform.scale(self.image, (self.width*2, self.height*2))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
    

    
import pygame
import settings
from os.path import join



def get_block(size, color):
    surface = pygame.Surface((size, size))
    surface.fill(color)
    return surface

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None, color="#275950"):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.original_color = color  # Almacena el color original del objeto
        self.current_color = color  # Almacena el color actual del objeto
        self.image = get_block(width, self.current_color)
        self.width = width
        self.height = height
        self.name = name
        self.color = color

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

    def change_color(self, new_color):
        self.color = new_color
        self.image = get_block(self.width, self.color)

class Block(Object):
    
    def __init__(self, x, y, size, name=None, color="#49768b"):
        super().__init__(x, y, size, size, name, color)
        self.mask = pygame.mask.from_surface(self.image)
        self.original_color = color
        self.near_distance = 70  # Define la distancia de de iluminacion 

    def loop(self, player, window, offset_x, offset_y):
        # Calcula la distancia entre el centro del objeto y el centro del jugador
        obj_center_x, obj_center_y = self.rect.center
        player_center_x, player_center_y = player.rect.center
        distance = ((obj_center_x - player_center_x) ** 2 + (obj_center_y - player_center_y) ** 2) ** 0.5

        if distance <= self.near_distance:
            self.change_color("#41bfb3")  # Cambia el color si el jugador está cerca

        else:
            self.change_color(self.original_color)  # Restaura el color original si el jugador no está cerca

        self.draw(window, offset_x, offset_y)

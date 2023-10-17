import pygame

pygame.init()
pygame.joystick.init()

pygame.display.set_caption("Correr o Morir")

screen_info = pygame.display.Info()
HEIGHT = screen_info.current_h
WIDTH = screen_info.current_w
FPS = 90
PLAYER_VEL = 5


window = pygame.display.set_mode((WIDTH, HEIGHT))
joysticks = []

import pygame
from scripts.text import Text

pygame.init()
pygame.joystick.init()

pygame.display.set_caption("Kings & Pirates")

screen_info = pygame.display.Info()
HEIGHT = screen_info.current_h
WIDTH = screen_info.current_w
FPS = 90
PLAYER_VEL = 5


window = pygame.display.set_mode((WIDTH, HEIGHT))
joysticks = []
life = 5

# DATOS DEL USUARIO
def get_data():
    file = open("user.txt", "r")
    lines = file.read().splitlines()
    file.close()
    return lines

# ACTUALIZAR DATOS
def set_data(level, score, life):
    file = open("user.txt", "w")
    file.write(str(level)+"\n")
    file.write(str(score))
    file.close()
    lines = get_data()
    current_level = lines[0]
    score = lines[1]
    score_Text.set_text(score)
    create_life(life)
  

# LEER DATOS
lines = get_data()
current_level = lines[0]
score = lines[1]

# BARRA DE INFORMACION
barrel = pygame.image.load("assets/Decorations/barrel.png")
barrel = pygame.transform.scale(barrel, (30,30))
barrel_rect = barrel.get_rect()
barrel_rect.topleft = (WIDTH- 200, 40)


heart_image = pygame.image.load("assets/Decorations/Heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))


# Score
score_Text = Text(score, WIDTH- 150, 55 , "white", 30)

# Corazones
hearts = []

def create_life(life_count):
    hearts = []
    for i in range(0,life_count):
        heart_rect = heart_image.get_rect()
        heart_rect.topleft = (40 + i * 40, 40)
        hearts.append(heart_rect)
        window.blit(heart_image, heart_rect)

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


# User Data
def get_data():
    file = open("user.txt", "r")
    lines = file.read().splitlines()
    return lines
    file.close()

def set_data(level, score):
    file = open("user.txt", "w")
    file.write(str(level)+"\n")
    file.write(str(score))
    file.close()
    lines = get_data()
    current_level = lines[0]
    score = lines[1]
    score_Text.set_text("Barrels: "+ score)

lines = get_data()
current_level = lines[0]
score = lines[1]

barrel = pygame.image.load("assets/Decorations/barrel.png")
barrel = pygame.transform.scale(barrel, (30,30))
barrel_rect = barrel.get_rect()
barrel_rect.topleft = (70, 30)

score_Text = Text(score, 124, 43 , "white", 30)

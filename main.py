import os
import random
import math
import pygame

# SCRIPTS
import settings
from player import Player
from background import get_background
from objects import Block
from enemies import Fire



# INIT PYGAME
pygame.init()

pygame.display.set_caption("MOAIS")

# DRAW IN SCREEN
def draw(window, background, bg_image, player, objects, offset_x, offset_y):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    # TEXT
    font = pygame.font.Font('freesansbold.ttf', 20)
    text2 = font.render(player.message, True, (0, 0, 0))
    textRect2 = text2.get_rect()
    textRect2.center = (settings.WIDTH // 2, 80)
    settings.window.blit(text2, textRect2)

    player.draw(window, offset_x, offset_y)

    pygame.display.update()




def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 20
    
    blocks = []
    fires = []
    points = []

    # CREATE MAP

    # Leer el archivo de texto
    with open("levels.txt", "r") as file:
        level_map = file.readlines()

    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index 
            y =  row_index 
            if cell == 'P':
                player = Player(x* block_size, y* block_size, 50, 50)
            if cell == 'X':
                block = Block(x* block_size, y* block_size, block_size)
                blocks.append(block)

            if cell == '.':
                point = Block(x* block_size, y* block_size, 5, "#f9f9f9", "point")
                points.append(point)
            
            if cell == 'f':
                fire = Fire(x*block_size+30, y*block_size+32, 16, 32)
                fires.append(Fire(x*block_size+30, y*block_size+32, 16, 32))
 
    
    objects = [*blocks, *fires, *points]
    for i in fires:
        i.on()

    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 200
    init = True
    
    run = True
    while run:
        clock.tick(settings.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
            
            # Joystick
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                settings.joysticks.append(joy)

        player.handle_move(objects)
        
        for i in fires:
            i.loop()

        for i in blocks:
            i.loop(player,window, offset_x, offset_y)
      
        
        if init == True:
            offset_x = player.rect.centerx - (settings.WIDTH // 2)
            offset_y = player.rect.centery - (settings.HEIGHT // 2)
            init = False
            
        if ((player.rect.right - offset_x >= settings.WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
            
        if ((player.rect.bottom - offset_y >= settings.HEIGHT - scroll_area_height) and player.y_vel > 0) or (
        (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel
        
        # Llama a la función draw con la vista de la cámara actualizada
        draw(window, background, bg_image, player, objects, offset_x, offset_y)
       
    quit()


if __name__ == "__main__":
    main(settings.window)

import os
import random
import math
import pygame

# SCRIPTS
import scripts.settings as settings
from scripts.menu import Menu
from scripts.text import Text
from scripts.create_map import create_map, blocks, enemies, lands, back_tree, tree, decorations
from scripts.enemies import bullets

from scripts.player import Player
from scripts.background import get_background




# INIT PYGAME
pygame.init()

pygame.display.set_caption("KINGS AND PIRATES") 
menu = Menu()

# DRAW IN SCREEN
def draw(window, background, bg_image, player, objects, points,offset_x, offset_y):
    for tile in background:
        window.blit(bg_image, tile)

    for tree in back_tree: 
        tree.draw(window,offset_x, offset_y) 

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)
    for b in bullets:
        b.draw(window, offset_x, offset_y)

    for point in points:
        point.draw(window,offset_x, offset_y) 
    
    settings.score_Text.print()

    

    pygame.display.update()



def main(window, menu):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Yellow.png")
    menu.start()
    block_size = 128
    

    # CREATE MAP

    # Leer el archivo de texto
    with open("levels/level"+ settings.current_level+".txt", "r") as file:
        level_map = file.readlines()

    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index 
            y =  row_index 
    

            if cell == 'P':
                player = Player(x* block_size, y* block_size, 90, 58)
            else:
                # llamamos a la función crear mapa y le pasamos la celda para crear el objeto correspondiente
                create_map(cell, x, y)
    
    
    objects = [*blocks, *bullets, *decorations]
    points = [*enemies, *lands, *tree]
    

    offset_x = 0
    offset_y = 0
    scroll_area_width = 400
    scroll_area_height = 200
    init = False
    
    while menu.run:
        clock.tick(settings.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.run = False
                    break
            
            # Joystick
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                settings.joysticks.append(joy)

        player.handle_move(objects, enemies)
        
        for i in enemies:
            i.loop(player, objects)

        for i in tree:
            i.loop()

        for i in back_tree:
            i.loop()
            
        for i in bullets: 
            i.update(player, objects)

      
        
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
        draw(window, background, bg_image, player, objects, points, offset_x, offset_y)
       
    quit()

if __name__ == "__main__":
    main(settings.window, menu)

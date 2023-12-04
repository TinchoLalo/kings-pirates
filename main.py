import os
import random
import math
import pygame
import time


# SCRIPTS
import scripts.settings as settings
from scripts.menu import Menu
from scripts.text import Text
from scripts.create_map import create_map
import scripts.create_map
import scripts.enemies 

from scripts.player import Player
from scripts.background import get_background




# INICIALIZAR PYGAME
pygame.init()

pygame.display.set_caption("KINGS AND PIRATES") 
menu = Menu()


# DIBUJAR EN PANTALLA
def draw(window, background, bg_image, player, objects, points,offset_x, offset_y, perdiste):
    # Fondo
    for tile in background:
        window.blit(bg_image, tile)
    # Arboles
    for tree in scripts.create_map.back_tree: 
        tree.draw(window,offset_x, offset_y) 

    # Objetos, bloques, tierra
    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    # player
    player.draw(window, offset_x, offset_y)

    # enemigos
    for b in scripts.enemies.bullets:
        b.draw(window, offset_x, offset_y)

    # bordes
    for point in points:
        point.draw(window,offset_x, offset_y) 
    
    # info de score
    window.blit(settings.barrel, settings.barrel_rect)
    settings.score_Text.print()

    # Corazones
    settings.create_life(player.LIFE) # Life

    # Perdiste Mensaje
    if player.LIFE <= 0:
        perdiste = pygame.transform.scale(perdiste, (settings.WIDTH- 600, settings.HEIGHT- 600))
        perdiste_width, perdiste_height = perdiste.get_size()
        window.blit(perdiste, ((settings.WIDTH - perdiste_width) // 2, (settings.HEIGHT - perdiste_height)//2))

    pygame.display.update()


# FUNCION PRINCIPAL
def main(window, menu):
    clock = pygame.time.Clock()
    background, bg_image = get_background(f"level{settings.current_level}.png") # cargar fondo de acuerdo al nivel
    menu.start() # cargamos el menu
    block_size = 128 # tamaño de los bloques
    menu.music.stop() # pausar musica menu
    
    # imagen para informar que perdio
    perdiste = pygame.image.load("assets/perdiste.png")

    # music
    music = pygame.mixer.Sound('sounds/Pirates.mp3') 
    # play music on loop
    music.play(-1)

    # CREAR MAPA

    # Leer archivo del nivel
    with open("levels/level"+ settings.current_level+".txt", "r") as file:
        level_map = file.readlines()
    # ir dibujando todo el nivel
    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index 
            y =  row_index 
    
            # instanciamos el player en la posicion del nivel
            if cell == 'P':
                player = Player(x* block_size, y* block_size, 90, 58)
            else:
                # llamamos a la función crear mapa y le pasamos la celda para crear el objeto correspondiente
                create_map(cell, x, y)
    
    # creamos la lista con todos los objetos
    objects = [*scripts.create_map.blocks, *scripts.enemies.bullets, *scripts.create_map.decorations]
    points = [*scripts.create_map.enemies, *scripts.create_map.lands, *scripts.create_map.tree]
    
    # camara y area fija
    offset_x = 0
    offset_y = 0
    scroll_area_width = 400
    scroll_area_height = 200
    init = False
    
    
    # bucle del juego
    while menu.run:
        clock.tick(settings.FPS)
        

        # PASAR DE NIVEL O PERDER
        if player.NEXT_LEVEL or player.LIFE <= 0:
            # Perder
            if player.LIFE <= 0:
                time.sleep(2)
                settings.current_level = str(int(settings.current_level))
            # Ganar
            else:
                settings.current_level = str(int(settings.current_level) +1)

            # limopiamos todo para reiniciar nivel
            objects = []
            points = []
            scripts.create_map.blocks = [] 
            scripts.create_map.decorations = []
            scripts.create_map.enemies = [] 
            scripts.create_map.lands = [] 
            scripts.create_map.tree = []
            scripts.create_map.back_tree= [] 
            scripts.enemies.bullets = []
            
            player.LIFE = 5
            player.key = False
            music.stop()
            menu.music.stop()
            main(settings.window, menu)
        
        # eventos para salir
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.run = False
                music.stop()
                break
            # presionar escape para salir
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.run = False
                    music.stop()
                    break
            
            # Joystick
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                settings.joysticks.append(joy)

        # actualizar movimiento del player
        player.handle_move(objects, scripts.create_map.enemies, scripts.create_map.lands)
        
        # actualizar enemigos
        for i in scripts.create_map.enemies:
            i.loop(player, objects)
        # actualizar arboles
        for i in scripts.create_map.tree:
            i.loop()
        for i in scripts.create_map.back_tree:
            i.loop()
        
        # actualizar balas
        for i in scripts.enemies.bullets: 
            i.update(player, objects)


        # CAMARA
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
        draw(window, background, bg_image, player, objects, points, offset_x, offset_y, perdiste)
       
    quit()


if __name__ == "__main__":
    main(settings.window, menu)
    

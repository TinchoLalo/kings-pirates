import pygame
import settings
from text import Text, Button
from player import Player
from background import get_background
from enemies import Fire
from objects import Block

# DRAW IN SCREEN
def draw(window, background, bg_image, player, objects, buttons, offset_x, offset_y):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x, offset_y)
        
    for button in buttons:
        button.draw()
    
    Text("MOAIS", settings.WIDTH//2, settings.HEIGHT//3, "white", 80)
    Text("the lost secrets", settings.WIDTH//2, (settings.HEIGHT//3)+50, "white", 30)
    
    
    
    pygame.display.update()

class Menu():
    def __init__(self):
        self.run = False
        
    def start(self):
        clock = pygame.time.Clock()
        background, bg_image = get_background("Blue.png")
       
        block_size = 20
        
        blocks = []
        fires = []
        points = []
        buttons = []
        
        start_button = Button("EMPEZAR (A o Space)", settings.WIDTH//2, (settings.HEIGHT//3) + 130, "white", 20)
        buttons.append(start_button)
        

        # Leer el archivo de texto
        with open("levels/menu.txt", "r") as file:
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
                    point = Block(x* block_size, y* block_size, 5, "point", "#f9f9f9")
                    points.append(point)
                
                if cell == 'f':
                    fire = Fire(x*block_size+30, y*block_size+32, 16, 32)
                    fires.append(Fire(x*block_size+30, y*block_size+32, 16, 32))

        objects = [*blocks, *fires, *points]
        
        while not self.run:
            clock.tick(settings.FPS)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                        break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.textRect.collidepoint(event.pos):
                        self.run = True

                # Joystick
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    settings.joysticks.append(joy)

            # START
            keys = pygame.key.get_pressed()
            for joystick in settings.joysticks:
                if joystick.get_button(0): self.run = True

            if keys[pygame.K_SPACE]: self.run = True

            # Llama a la función draw con la vista de la cámara actualizada
            draw(settings.window, background, bg_image, player, objects, buttons, 0, 0)
            
            pygame.display.update()
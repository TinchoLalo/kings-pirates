import pygame
import settings
from text import Text, Button
from player import Player
#from background import get_background

# DRAW IN SCREEN
def draw(window, buttons, background):
   
    window.blit(background, (0, 0))

    for button in buttons:
        button.draw()

    pygame.display.update()

class Menu():
    def __init__(self):
        self.run = False
        
    def start(self):
        clock = pygame.time.Clock()
        #background, bg_image = get_background("background.png")
        image = pygame.image.load("assets/Background/background.png")
        background = pygame.transform.scale(image, (settings.WIDTH, settings.HEIGHT))
       
        buttons = []
        
        start_button = Button("EMPEZAR", settings.WIDTH//2, (settings.HEIGHT//3) + 150, "white", 30)
        exit_button = Button("SALIR", settings.WIDTH//2, (settings.HEIGHT//3) + 260, "white", 30)
        buttons.append(start_button)
        buttons.append(exit_button)
        
        

        while not self.run:
            clock.tick(settings.FPS)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                        quit()
                        break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.textRect.collidepoint(event.pos):
                        self.run = True
                    if start_button.textRect.collidepoint(event.pos):
                        self.run = True
                    if exit_button.textRect.collidepoint(event.pos):
                        self.run = False
                        quit()

                # Joystick
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    settings.joysticks.append(joy)

            # START
            keys = pygame.key.get_pressed()
            for joystick in settings.joysticks:
                if joystick.get_button(0): 
                    self.run = True
                    
            if keys[pygame.K_SPACE]: 
                self.run = True
             
                 

            # Llama a la función draw con la vista de la cámara actualizada
            draw(settings.window, buttons, background)
            
            pygame.display.update()

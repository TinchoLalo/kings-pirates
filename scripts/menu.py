import pygame
import scripts.settings as settings
from scripts.text import Text, Button
from scripts.player import Player
#from background import get_background

# DRAW IN SCREEN
def draw(window, buttons, background, author):
   
    window.blit(background, (0, 0))

    for button in buttons:
        button.draw()
    author.print()
    
    pygame.display.update()

class Menu():
    def __init__(self):
        self.run = False
        # music
        self.music = pygame.mixer.Sound('sounds/Pirate Tavern.mp3') 
        
    def start(self):
        clock = pygame.time.Clock()
        # bakcground
        image = pygame.image.load("assets/Background/background.png")
        background = pygame.transform.scale(image, (settings.WIDTH, settings.HEIGHT))

        
        # play music on loop
        self.music.play(-1)


        # buttons
        buttons = []
        
        start_button = Button("EMPEZAR", settings.WIDTH//2, (settings.HEIGHT//3) + 150, "white", 30)
        exit_button = Button("SALIR", settings.WIDTH//2, (settings.HEIGHT//3) + 260, "white", 30)
        buttons.append(start_button)
        buttons.append(exit_button)
        
        # Autor
        author = Text("MARTIN LA LOGGIA", settings.WIDTH//2 , settings.HEIGHT-155, "white", 30)
        
        

        while not self.run:
            clock.tick(settings.FPS)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    self.music.stop()
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                        self.music.stop()
                        quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.textRect.collidepoint(event.pos):
                        self.run = True
                        self.music.stop()
                    if exit_button.textRect.collidepoint(event.pos):
                        self.run = False
                        self.music.stop()
                        quit()

                # Joystick
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    settings.joysticks.append(joy)

            # START
            keys = pygame.key.get_pressed()
            for joystick in settings.joysticks:
                if joystick.get_button(0): 
                    self.music.stop()
                    self.run = True
                    
                    
            if keys[pygame.K_SPACE]: 
                self.music.stop()
                self.run = True
                
             
                 

            # Llama a la función draw con la vista de la cámara actualizada
            draw(settings.window, buttons, background, author)
            
            pygame.display.update()

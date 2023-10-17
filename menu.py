import pygame
import settings
from text import Text, Button
from background import get_background


class Menu():
    def __init__(self):
        self.run = False
       

    def start(self):
        clock = pygame.time.Clock()
        background, bg_image = get_background("Blue.png")
        

        while not self.run:
            clock.tick(settings.FPS)

            for tile in background:
                settings.window.blit(bg_image, tile)
                
            Text("MOAIS", settings.WIDTH//2, settings.HEIGHT//3, "white", 80)
            Text("the lost secrets", settings.WIDTH//2, (settings.HEIGHT//3)+50, "white", 30)
            
            start_button = Button("EMPEZAR (A o Space)", settings.WIDTH//2, (settings.HEIGHT//3) + 130, "white", 20)

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

            
            pygame.display.update()
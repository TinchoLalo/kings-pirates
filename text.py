import pygame
import settings
import sys

class Text():
    def __init__(self, text="", x=0, y=0, color="white", size=20, font='freesansbold.ttf'):
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.color = color
        self.text = self.font.render(text, True, self.color)
        self.x = x
        self.y = y
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x, self.y)
        self.on = True
        self.print()
    
    def print(self): 
        if self.on:   
            settings.window.blit(self.text, self.textRect)

    def set_on(self): self.on = True
    def set_off(self): self.on = False

    def change_color(self,new_color):
        self.color = new_color
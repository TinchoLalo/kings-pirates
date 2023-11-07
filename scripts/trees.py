import pygame
from scripts.load_sprite import load_sprite_sheets
from scripts.objects import Object


class Tree(Object):
    def __init__(self, x, y, width, height, name):
        super().__init__(x, y, width, height, name)
        self.sprite = load_sprite_sheets("Trees", name, width, height, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.animation_count = 0
        self.sprite_sheet = "idle"
        self.ANIMATION_DELAY = 5
        
    def loop(self):
        sprite_sheet_name = self.sprite_sheet
        sprites = self.sprite[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1


        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


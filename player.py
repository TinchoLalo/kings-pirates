import pygame
import settings
from load_sprite import load_sprite_sheets



class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3
    SPEED = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.land = False
        self.col = False
        self.sprite_sheet = "idle"
        self.pos = 0
        self.message = ""
        self.update_sprite()

    def jump(self):
        self.land = False
        self.y_vel = -self.GRAVITY * 4
        self.animation_count = 0
        self.jump_count = 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.land = True
        
    
    def handle_vertical_collision(self, objects, dy):
        collided_objects = []
       
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj) and obj.name != "point":
                if self.y_vel > 0:
                    self.rect.bottom = obj.rect.top
                    self.landed()
                if self.y_vel < 2 and not self.land and self.rect.bottom != obj.rect.top:
                    self.rect.top = obj.rect.bottom 
                    self.hit_head()
            
        return collided_objects
    
    
    def collide(self, objects, dx):
        self.move(dx, self.y_vel/2)
        collided_object = None
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj) and obj.name != "point":
                collided_object = obj
                break
          
        return collided_object

    def handle_move(self, objects):
        keys = pygame.key.get_pressed()

        self.x_vel = 0
        collide_left = self.collide(objects, -self.SPEED * 2)
        collide_right = self.collide(objects, self.SPEED * 2)

        # JOYSTICK
        for joystick in settings.joysticks:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)

            if joystick.get_button(5) and self.land:
                self.SPEED = 10
            else:
                self.SPEED = 5
            
            if axis_x < -0.5 and not collide_left:
                self.move_left(self.SPEED)

            if axis_x > 0.5 and not collide_right:
                self.move_right(self.SPEED)

            if joystick.get_button(0) and self.jump_count < 1 and self.land:
                self.jump()
        
        # TECLADO
        if keys[pygame.K_w] and self.land:
            self.SPEED = 10
        else:
            self.SPEED = 5
        if keys[pygame.K_a] and not collide_left:
            self.move_left(self.SPEED)

        if keys[pygame.K_d] and not collide_right:
            self.move_right(self.SPEED)

        if keys[pygame.K_SPACE] and self.jump_count < 1 and self.land:
            self.jump()


        vertical_collide = self.handle_vertical_collision(objects, self.y_vel)
        to_check = [collide_left, collide_right, *vertical_collide]


        for obj in to_check:
            if obj and obj.name == "fire":
                self.make_hit()

        self.loop()

    def loop(self):
        
        self.y_vel += min(1, (self.fall_count / 60) * self.GRAVITY) 
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > 10:
            self.hit = False
            self.hit_count = 0
        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        self.sprite_sheet = "idle"
        if self.hit:
            self.sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                self.sprite_sheet = "jump"
        elif self.y_vel > self.GRAVITY * 2:
            self.sprite_sheet = "fall"
        elif self.x_vel != 0:
            self.sprite_sheet = "run"

        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x,offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

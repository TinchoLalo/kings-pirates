import pygame
import pygame.time
from scripts.load_sprite import load_sprite_sheets
from scripts.objects import Object


bullets = []
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, name, speed, direction):
        super().__init__()
        self.image = pygame.image.load("assets/"+name+".png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed  # Velocidad de la bala
        self.direction = direction  # Dirección de la bala (1 para derecha, -1 para izquierda)
    
    def update(self,player, objects):
        # Mueve la bala en la dirección especificada
        self.rect.x += self.speed * self.direction

        if pygame.sprite.collide_mask(self, player) and not player.attack:
            player.LIFE -= 1
        elif pygame.sprite.collide_mask(self, player):
            bullets.remove(self)

        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                bullets.remove(self)

    def draw(self, win, offset_x,offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

class Enemies(Object):
    LIFE = 100

    def __init__(self, x, y, width, height, name, near_distance, move_distance, move_attack = False, shooter = False, shot_delay = 2000, ANIMATION_DELAY=3):
        super().__init__(x, y, width, height,[0,0], name)
        self.sprite = load_sprite_sheets("MainCharacters", name, width, height, True)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.animation_count = 0
        self.fall_count = 0
        self.land = 0
        self.y_vel = 0
        self.near_distance = near_distance
        self.direction = "right"
        self.sprite_sheet = "idle"
        self.move_count = 0
        self.move_distance = move_distance
        self.move_attack = move_attack
        self.shooter = shooter
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_delay = shot_delay 
        self.ANIMATION_DELAY = ANIMATION_DELAY

    # Mover de lado a lado
    def move(self):
        if self.move_count >= self.move_distance:
            self.direction = "left" if self.direction == "right" else "right"  # Invierte la dirección
            self.move_count = 0
        self.rect.x = self.rect.x - 1 if self.direction == "right" else self.rect.x + 1  # Mueve al enemigo en la dirección actual
        self.move_count += 3 
    
    # Atacar perseguir
    def attack(self,pos):
        if pos > self.rect.x:
            self.rect.x += 2.5
            self.direction = "right" 
        else: 
            self.rect.x -= 2.5
            self.direction = "left" 
    # Disparar
    def shoot(self, dir):
        new_bullet = Bullet(self.x+30, self.y+40, "Bullet",10, dir)
        bullets.append(new_bullet)

    # BUCLE
    def loop(self, player, objects):
        # Muerte
        if self.LIFE <= 0:
            self.sprite_sheet = "dead"

        # Daño recivido
        elif pygame.sprite.collide_mask(self, player) and player.attack:
            self.sprite_sheet = "hit"
        # Atacar si el jugador esta cerca
        elif abs(player.rect.x - self.rect.x) <= self.near_distance and abs(player.rect.y - self.rect.y) <= self.near_distance:
            self.sprite_sheet = "attack"
            if self.move_attack: self.attack(player.rect.x)
            if self.shooter:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time >= self.shot_delay:
                    self.shoot(-1)  # Llama a la función para disparar
                    self.last_shot_time = current_time

        else: self.sprite_sheet = "idle" if self.move_distance <= 0 else "run"

        # Movimiento de lado a lado
        if self.move_distance > 0 and self.LIFE > 0:
            if abs(player.rect.x - self.rect.x) <= self.near_distance and self.LIFE > 0: 
                self.attack(player.rect.x)
                self.direction = "left" if player.rect.x >self.rect.x else "right"
            else:
             self.move()
        else: 
            if abs(player.rect.x - self.rect.x) <= self.near_distance and self.LIFE > 0 and not self.shooter:
                self.direction = "right" if player.rect.x < self.rect.x else "left"

        # COLISION GRAVEDAD
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                if self.y_vel > 0:
                    self.rect.bottom = obj.rect.top-10  if self.move_distance > 0 else obj.rect.top
                    self.land = True
                    self.fall_count = 0
                  
        self.y_vel += min(1, (self.fall_count / 60) * player.GRAVITY) 
        self.rect.y += self.y_vel if self.LIFE > 0 else 0
        self.fall_count += 1

        # SPRITE
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.sprite[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1


        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

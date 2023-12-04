import pygame
import time
import scripts.settings as settings
from scripts.load_sprite import load_sprite_sheets



class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "King", 90, 58, True)
    ANIMATION_DELAY = 4
    SPEED = 5
    LIFE = 5
    NEXT_LEVEL = False

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 1
        self.fall_count = 0
        self.jump_count = 0
        self.attack = False
        self.attack_count = 0
        self.hit = False
        self.hit_count = 0
        self.land = False
        self.col = False
        self.dead = False
        self.sprite_sheet = "idle"
        self.pos = 0
        self.key = False
        self.message = ""
        self.win = False
        self.win_count = 0
        self.update_sprite()

    # SALTAR
    def jump(self):
        self.land = False
        self.y_vel = -self.GRAVITY * 4.4
        self.animation_count = 1
        self.jump_count = 1
        if self.jump_count == 1:
            self.fall_count = 0

    # MOVERSE
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy if self.dead != True else 0
        if self.LIFE <= 0 and self.land and not self.dead:
            self.rect.y += 10
            self.dead = True

    # RECIVIR DAÑO
    def make_hit(self, damage):
        if self.hit == False:
            self.LIFE -= damage
            life = self.LIFE if self.LIFE >= 0 else 0
            settings.set_data(int(settings.current_level), settings.score, life)
        self.hit = True

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    # MOVERSE A LA IZQUIERDA
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 1

    # MOVERSE A LA DERECHA
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 1
    
    # TOCAR TIERRA
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.land = True
        
    # COLISIONES VERTICALES
    def handle_vertical_collision(self, objects,enemies, lands):
        collided_objects = []
       
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj)  and obj.name != "Botle" and obj.name != "Spike" and obj.name != "Key" and obj.name != "Chesto" and obj.name != "Chestc":
                if self.y_vel > 0 and self.rect.right > obj.rect.left+65 and not self.attack :
                    self.rect.bottom = obj.rect.top
                    self.landed()
                elif self.y_vel > 0 and self.rect.right > obj.rect.left+65 and self.attack :
                    self.landed()
                elif self.y_vel < 2 and not self.land:
                    self.rect.top = obj.rect.bottom 
                    self.hit_head()

                # Barriles
                elif pygame.sprite.collide_mask(self, obj) and self.attack and obj.name == "Barrel":
                    settings.set_data(settings.current_level, int(settings.score)+1, self.LIFE)
                    objects.remove(obj)
                # Botella
                elif pygame.sprite.collide_mask(self, obj) and self.attack and obj.name == "Botle":
                    objects.remove(obj)
                # Llave
                elif pygame.sprite.collide_mask(self, obj) and obj.name == "Key":
                    self.key = True
                    objects.remove(obj)
                # Cofre
                elif pygame.sprite.collide_mask(self, obj) and obj.name == "Chestc" and self.key:
                    obj.update_name("Chesto")
                    self.win = True
                    settings.set_data(int(settings.current_level)+1, settings.score, self.LIFE)
                
            # Pinches
            elif pygame.sprite.collide_mask(self, obj) and obj.name == "Spike":
                self.make_hit(1)
        # Enemigos
        for e in enemies:
            if pygame.sprite.collide_mask(self, e) and not self.attack and e.LIFE > 0 and e.name != "Seashell":
                self.make_hit(1)
            elif pygame.sprite.collide_mask(self, e) and self.attack:
                e.LIFE -= 10
        # lava
        for e in lands:
            if pygame.sprite.collide_mask(self, e) and e.name != "Water":
                self.make_hit(1)
            

        return collided_objects
    
    # COLISIONES LATERALES
    def collide(self, objects, dx, enemies, lands):
        self.move(dx, self.y_vel/2)
        collided_object = None
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj) and obj.name != "Botle" and obj.name != "Spike" and obj.name != "Key" and obj.name != "Chesto" and obj.name != "Chestc":
                collided_object = obj
                break
            # Barriles
            elif pygame.sprite.collide_mask(self, obj) and self.attack and obj.name == "Barrel":
                settings.set_data(settings.current_level, int(settings.score)+1, self.LIFE)
                objects.remove(obj)
            # Pinches
            elif pygame.sprite.collide_mask(self, obj) and obj.name == "Spike":
                self.make_hit(1)
            # Llave
            elif pygame.sprite.collide_mask(self, obj) and obj.name == "Key":
                self.key = True
                objects.remove(obj)
            # Cofre
            elif pygame.sprite.collide_mask(self, obj) and obj.name == "Chestc" and self.key:
                obj.update_name("Chesto")
                self.win = True
                settings.set_data(int(settings.current_level)+1, settings.score, self.LIFE)
        # enemigos
        for e in enemies:
            if pygame.sprite.collide_mask(self, e) and not self.attack and e.LIFE > 0 and e.name != "Seashell":
                self.make_hit(1)
            elif pygame.sprite.collide_mask(self, e) and self.attack:
                e.LIFE -= 10
        # lava
        for e in lands:
            if pygame.sprite.collide_mask(self, e) and e.name != "Water":
                self.make_hit(1)

        return collided_object

    def handle_move(self, objects, enemies, lands):
        keys = pygame.key.get_pressed()

        self.x_vel = 0
        collide_left = self.collide(objects, -self.SPEED * 2, enemies, lands)
        collide_right = self.collide(objects, self.SPEED * 2, enemies, lands)
        if self.LIFE > 0:
            # JOYSTICK
            for joystick in settings.joysticks:
                axis_x = joystick.get_axis(0)
                #axis_y = joystick.get_axis(1)

                # Correr o Caminar
                if joystick.get_button(5) and self.land:
                    self.SPEED = 15
                else:
                    self.SPEED = 8
                # Atacar
                if joystick.get_button(2):
                    self.attack = True
                # Moverse
                if axis_x < -0.5 and not collide_left:
                    self.move_left(self.SPEED)

                if axis_x > 0.5 and not collide_right:
                    self.move_right(self.SPEED)
                # Saltar
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

        if not self.dead:
            self.handle_vertical_collision(objects, enemies, lands)
        
        self.loop()

    def loop(self):
        # Gravedad
        self.y_vel += min(1, (self.fall_count / 60) * self.GRAVITY) 
        self.move(self.x_vel, self.y_vel)
        
        # Pasar de nivel
        if self.win:
            self.win_count += 1
        if self.win_count > 30:
            self.win = False
            self.win_count = 0
            
            self.NEXT_LEVEL = True

        # Contadores            
        if self.hit:
            self.hit_count += 1
        if self.hit_count > 20:
            self.hit = False
            self.hit_count = 0
        if self.attack:
            self.attack_count += 1
        if self.attack_count > 7:
            self.attack = False
            self.attack_count = 0
        self.fall_count += 1
        self.update_sprite()

    # ANIMACIONES
    def update_sprite(self):
        self.sprite_sheet = "idle"
        if self.LIFE <= 0:
            self.sprite_sheet = "dead"
        elif self.attack:
            self.sprite_sheet = "attack"
        elif self.hit:
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
        if self.ANIMATION_DELAY != 0 and self.animation_count != 0 and  len(sprites) != 0:
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.sprite = sprites[sprite_index]
        else:
            sprite_index = 0  # Otra acción predeterminada en caso de que ANIMATION_DELAY sea 0
       
        self.animation_count += 1
        self.update()
        
    # ACTUALIZAR COLLIDER
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    # DIBUJAR EN PANTALLA
    def draw(self, win, offset_x,offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

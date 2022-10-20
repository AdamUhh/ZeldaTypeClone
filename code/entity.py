import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        # ? vector of 0 cannot be normalized (if the magnitude was a 0, it will break code)
        if self.direction.magnitude() != 0:
            # ? ensures that the direction is always equal to 1 or -1
            # ? useful when two keys are pressed, which makes the player move faster
            #  ? due to trigonometry stuff. normalize() prevents that
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # ? is the sprite colliding with an obstacle sprite
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # ? moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # ? moving left
                        self.hitbox.left = sprite.hitbox.right
            pass
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                # ? is the sprite colliding with an obstacle sprite
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # ? moving up
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # ? moving down
                        self.hitbox.top = sprite.hitbox.bottom
            pass

    def wave_value(self):
        # ? flicker when hit
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

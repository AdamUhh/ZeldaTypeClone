import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            'graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        # ? y = -26 will shrink 13px on the top and bottom
        self.hitbox = self.rect.inflate(0, -26)
        # ? direction
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

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

    def update(self):
        self.input()
        self.move(self.speed)

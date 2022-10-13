import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            'graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        # ? takes a rectangle and changes its size
        # ? y = -10 will shrink 5px on the top and bottom
        self.hitbox = self.rect.inflate(0, -10)

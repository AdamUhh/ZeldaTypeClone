import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type  # ? could be an enemy, or invisible, etc
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object':
            # ? do a y offset for the object/image to be properly placed on the floor
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        # ? takes a rectangle and changes its size
        # ? y = -10 will shrink 5px on the top and bottom
        self.hitbox = self.rect.inflate(0, y_offset)

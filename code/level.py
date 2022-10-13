import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug


class Level:
    def __init__(self):

        # get the display surface (this is basically self.screen inside main.py)
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        # ? enumerate provides the index
        for row_index, row in enumerate(WORLD_MAP):  # ? y coords
            for col_index, col in enumerate(row):  # ? x coords
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    # ? Create a rock tile ((position), [groups it will be in])
                    # ? a col that is an 'x' will be visible to the player, but also acts as an obstacle
                    # ? that the player can collide with (essentially a wall)
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    # ? player
                    self.player = Player(
                        (x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # ? general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # ? getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # ? displays the sprites on the screen, sprites that have a bigger 'y' value
        # ? will be displayed ontop. This ensures that the player sprite is overlayed properly
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

from random import choice, randint
import pygame
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from debug import debug
from support import *
from weapon import Weapon
from ui import UI
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


class Level:
    def __init__(self):

        #  ?get the display surface (this is basically self.screen inside main.py)
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        # ? sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # ? attack sprites
        self.current_attack = None
        # ? check collisions between below groups
        self.attack_sprites = pygame.sprite.Group()  # ? weapons and logic in this group
        self.attackable_sprites = pygame.sprite.Group()  # ? enemies in this group
        # ? sprite setup
        self.create_map()

        # ? user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        # ? particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects')
        }

        for style, layout in layouts.items():
            # ? enumerate provides the index
            for row_index, row in enumerate(layout):  # ? y coords
                for col_index, col in enumerate(row):  # ? x coords
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            # ? create a collision tile
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            # ? create a grass tile
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y),
                                 [self.visible_sprites, self.attackable_sprites, self.obstacle_sprites],
                                 'grass',
                                 random_grass_image)
                        if style == 'object':
                            # ? create a object tile
                            num = int(col)
                            object_surface = graphics['objects'][num]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_surface)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name,
                                      (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites, self.damage_player, self.trigger_death_particles,
                                      self.add_xp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def player_attack_logic(self):
        # ? cycle through all the attack sprites and
        # ? and check if any of them are colliding with attackable sprites
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            # ? display upgrade menu
            self.upgrade.display()
        else:
            # ? run the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites, self.attack_sprites])

    def add_xp(self, amount):
        self.player.exp += amount

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            # ? spawn particles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # ? general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # ? creating the floor
        self.floor_surface = pygame.image.load(
            '../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # ? getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # ? drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # ? displays the sprites on the screen by their y position, sprites that have a bigger 'y' value
        # ? will be displayed ontop. This ensures that the player sprite is overlayed properly
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and
                         sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

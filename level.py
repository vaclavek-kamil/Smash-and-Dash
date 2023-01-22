import pygame
from settings import *
from tiles import *
from players import *

class Level:
    def __init__(self):
        #getting the display surface from the library
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.floor_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()
        self.pressed_keys = pygame.key.get_pressed()


    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):

                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == 'f':
                    Floor((x,y), [self.obstacles_sprites])

                if col == 'w':
                    Wall((x,y), [self.floor_sprites])

                if col == '1':
                    Player((x,y),1, [self.player_sprites])
                    Floor((x,y), [self.floor_sprites])

                if col == '2':
                    Player((x,y),2, [self.player_sprites])
                    Floor((x,y), [self.floor_sprites])

    def run(self):
        #get the keyboard status, which will be used across all the update functions
        self.pressed_keys = pygame.key.get_pressed()

        #update the game objects
        self.player_sprites.update(self)

        #draw the game objects 
        self.floor_sprites.draw(self.display_surface)
        self.obstacles_sprites.draw(self.display_surface)
        for sprite in self.player_sprites:
            sprite.custom_draw(self)

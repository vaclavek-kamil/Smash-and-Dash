import pygame
from settings import *

class Floor (pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('art/tiles/floor.png')
        self.rect = self.image.get_rect(topleft = pos)

class Wall (pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('art/tiles/wall.png')
        self.rect = self.image.get_rect(topleft = pos)
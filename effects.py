import pygame
import math
from settings import *

            
class Splash (pygame.sprite.Sprite):
#####################################################################################################################################################################################################
#   INITIALIZATION OF THE SPLASH EFFECT CLASS
######################################################################################################################################################################################################
    def __init__(self, pos, groups):
        super().__init__(groups)
        #SPLASH EFFECT SPRITE
        self.image = pygame.image.load('art/effects/splash.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        #the amount of frames this effect stays on the screen for
        self.DURATION = 30
        self.progress = 0

    def update(self):
        self.progress += 1
        if self.progress >= self.DURATION:
            self.kill()

class Healthbars (pygame.sprite.Sprite):
#####################################################################################################################################################################################################
#   INITIALIZATION OF THE SPLASH EFFECT CLASS
######################################################################################################################################################################################################
    def __init__(self, groups):
        super().__init__(groups)
        self.BG1_START = (WIDTH / 20, HEIGTH / 20)
        self.BG1_END = ((WIDTH / 2) - (WIDTH / 20), HEIGTH / 20)
        self.BG2_START = ((WIDTH / 2) + (WIDTH / 20), HEIGTH / 20)
        self.BG2_END = (WIDTH - (WIDTH / 20), HEIGTH / 20)
        self.THICKNESS = HEIGTH / 30
        self.BG_COLOR = (16,16,16)

    def draw(self, level):
        pygame.draw.line(level.display_surface, self.BG_COLOR, self.BG1_START, self.BG1_END, self.THICKNESS)
        pygame.draw.line(level.display_surface, self.BG_COLOR, self.BG2_START, self.BG2_END, self.THICKNESS)
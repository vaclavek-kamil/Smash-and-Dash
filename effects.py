import pygame
import math
from settings import *

            
class Splash (pygame.sprite.Sprite):
#####################################################################################################################################################################################################
#   INITIALIZATION OF THE PLAYER CLASS - THE PLAYER CLASS IS USED FOR BOTH PLAYERS - PLAYERS CAN BE TOLD APART BY THE 'self.NUMBER' CONSTANT SET AT DEFINITION
#####################################################################################################################################################################################################
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
import pygame
import math
from settings import *
from players import *

class Healthbars (pygame.sprite.Sprite):
#####################################################################################################################################################################################################
#   INITIALIZATION OF THE HEALTHBAR CLASS
######################################################################################################################################################################################################
    def __init__(self, groups):
        super().__init__(groups)
        self.THICKNESS = round(HEIGTH / 20)
        self.BAR1_START = (round((WIDTH / 20) - (self.THICKNESS / 2)), round(HEIGTH / 20))
        self.BAR1_END = (round((WIDTH / 2) - (WIDTH / 20) + (self.THICKNESS / 2)), round(HEIGTH / 20))
        self.BAR2_START = (round((WIDTH / 2) + (WIDTH / 20) - (self.THICKNESS / 2)), round(HEIGTH / 20))
        self.BAR2_END = (round(WIDTH - (WIDTH / 20) + (self.THICKNESS / 2)), round(HEIGTH / 20))
        self.BAR_SIZE = int(self.BAR1_END[0]) - int(self.BAR1_START[0])
        self.GREY = (16,16,16)
        self.PURPLE = (127, 0, 255)
        self.ORANGE = (255, 127, 0)
        self.players_hp = [None, None, None]

    def custom_draw(self, level):
        #drawing the grey background bars
        pygame.draw.line(level.display_surface, self.GREY, self.BAR1_START, self.BAR1_END, self.THICKNESS)
        pygame.draw.line(level.display_surface, self.GREY, self.BAR2_START, self.BAR2_END, self.THICKNESS)

        #getting the health amounts from the player sprites
        for sprite in level.player_sprites:
            self.players_hp[sprite.NUMBER] = sprite.hp
            
        MAX_HP = sprite.MAX_HP

        #Drawing the colorful bars (their size is calculated from the player HP) on when the player still has some HP left
        if self.players_hp[1] > 0:
            pygame.draw.line(level.display_surface, self.PURPLE, self.BAR1_START, ((self.BAR1_START[0] + ((self.players_hp[1] / MAX_HP) * self.BAR_SIZE)), self.BAR1_START[1]), self.THICKNESS)
        
        if self.players_hp[2] > 0:
            pygame.draw.line(level.display_surface, self.ORANGE, self.BAR2_START, ((self.BAR2_START[0] + ((self.players_hp[2] / MAX_HP) * self.BAR_SIZE)), self.BAR2_START[1]), self.THICKNESS)


        
            
            
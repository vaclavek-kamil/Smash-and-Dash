import pygame
from settings import *

class Player (pygame.sprite.Sprite):
    def __init__(self, pos, number, groups):
        super().__init__(groups)
        
        #number of the player - either 1 or 2
        self.NUMBER = number

        #sprites / textures for the player.     The list will be used with the NUMBER constant to choose the appropriate player texture
        self.img_idle = [None, pygame.image.load('art/players/player1/idle.png'), pygame.image.load('art/players/player2/idle.png')]
        self.img_charge = [None, pygame.image.load('art/players/player1/charge.png'), pygame.image.load('art/players/player2/charge.png')]
        self.img_hit = [None, pygame.image.load('art/players/player1/hit.png'), pygame.image.load('art/players/player2/hit.png')]
        
        #GETTING THE COLIDER AND THE RECT TO RENDER THE IMAGES ON
        self.rect = self.img_idle[self.NUMBER].get_rect(topleft = (pos[0]-TILE_SIZE, pos[1]-TILE_SIZE))
        self.colider = self.rect.copy()
        self.colider.width -= TILE_SIZE*2
        self.colider.height -= TILE_SIZE*2
        self.colider.topleft = pos

        #AMOUNT OF FRAMES, BEFORE THE ATTACK IS EXECUTED AFTER CHARGING
        self.CHARGE_DURATION = 15

        #THE AMOUNT OF FRAME A DODGE LAST, MAKING THE PLAYER IMUNE TO DAMAGE (IGNORES HITS)
        self.DODGE_DURATION = 25

        #HEALTH POINTS
        self.hp = 100

        #PLAYER DAMAGE
        self.DMG = 20
        
        #THE FACING DIRECTION (left, right, up, down)
        self.facing = 'left'
        

    #CUSTOM DRAW FUNCTION
    def custom_draw(self, level):
        pygame.Surface.blit( level.display_surface, self.img_idle[self.NUMBER], self.rect)
        
        #THIS IS HERE ONLY TO DEBUG THE HITBOX OF THE PLAYER
        #pygame.draw.rect(level.display_surface, (255,255,0), self.rect, 3)
        pygame.draw.rect(level.display_surface, ((self.NUMBER-1)*255,(self.NUMBER-2)*-255,0), self.colider, 3)

import pygame
import math
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

        #PLAYER SPEED (pixels per frame)
        self.SPEED = 4

        #THE FACING DIRECTION (left, right, up, down)
        self.facing = 'left'

#####################################################################################################################################################################################################

    #CUSTOM DRAW FUNCTION
    def custom_draw(self, level):
        #updating the rect position to the position of the colider before rendering
        self.rect.center = self.colider.center

        #so far, only blitting the idle surf, regardless of anything
        pygame.Surface.blit( level.display_surface, self.img_idle[self.NUMBER], self.rect)
        
        #THIS IS HERE ONLY TO DEBUG THE HITBOX OF THE PLAYER
        #pygame.draw.rect(level.display_surface, (255,255,0), self.rect, 3)
        pygame.draw.rect(level.display_surface, ((self.NUMBER-1)*255,(self.NUMBER-2)*-255,0), self.colider, 3)

#####################################################################################################################################################################################################

    #UPDATE FUNCTION, HANDLING INPUT AND PHYSICS
    def update(self, level):

        x_input = 0
        y_input = 0

        #getting the player movement input

        #UP
        if (level.pressed_keys[pygame.K_w] and self.NUMBER == 1) or (level.pressed_keys[pygame.K_UP] and self.NUMBER == 2):
            y_input -= 1;
        
        #DOWN
        if (level.pressed_keys[pygame.K_s] and self.NUMBER == 1) or (level.pressed_keys[pygame.K_DOWN] and self.NUMBER == 2):
            y_input += 1;
       
        #LEFT
        if (level.pressed_keys[pygame.K_a] and self.NUMBER == 1) or (level.pressed_keys[pygame.K_LEFT] and self.NUMBER == 2):
            x_input -= 1;
        
        #RIGHT
        if (level.pressed_keys[pygame.K_d] and self.NUMBER == 1) or (level.pressed_keys[pygame.K_RIGHT] and self.NUMBER == 2):
            x_input += 1;

        #diagonal movement
        if y_input != 0 and x_input != 0:
            diagonal = math.sqrt(self.SPEED*self.SPEED/2)
            
            x_input *= round(diagonal)
            y_input *= round(diagonal)

        #Multiplying the input by the player speed to turn it into a directional vector
        else:
            y_input *= self.SPEED
            x_input *= self.SPEED

            
        #applying the directional vector onto the players position
        self.colider.x += x_input
        self.colider.y += y_input

        #debugging
        pygame.display.set_caption('x: ' + str(x_input) + '     y: ' + str(y_input) + '   ' + str(self.colider.x) + '   ' + str(self.colider.x))


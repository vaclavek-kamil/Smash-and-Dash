##############################################################################################
    #       #       #       #       #       #   ######  #       #####  #     # ####### ######    
import pygame   #       #       #       #       #     # #      #     #  #   #  #       #     #
import math #       #       #       #       #   ######  #      #######   # #   ####### #####
from settings import *  #       #       #       #       #      #     #    #    #       #    #
    #       #       #       #       #       #   #       ###### #     #    #    ####### #     #
##############################################################################################

class Player (pygame.sprite.Sprite):
#####################################################################################################################################################################################################
#   INITIALIZATION OF THE PLAYER CLASS - THE PLAYER CLASS IS USED FOR BOTH PLAYERS - PLAYERS CAN BE TOLD APART BY THE 'self.NUMBER' CONSTANT SET AT DEFINITION
#####################################################################################################################################################################################################
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
        self.rect.width -= TILE_SIZE*2
        self.rect.height -= TILE_SIZE*2
        self.rect.topleft = pos
        self.attack_hitbox = None

        #AMOUNT OF FRAMES, BEFORE THE ATTACK IS EXECUTED AFTER CHARGING
        self.CHARGE_DURATION = 20

        #THE AMOUNT OF FRAME A DODGE LAST, MAKING THE PLAYER IMUNE TO DAMAGE (IGNORES HITS)
        self.DODGE_DURATION = 25

        #THE AMOUNT OF PIXELS AN ATTACK REACHES
        self.ATTACK_RANGE = 40

        #ATTACK PROGRESS -  (0 - CHARGE_DURATION) = THE ATTACK IS CHARGING
        ##################  ((CHAGRE_DURATION + 1 - (2*CHARGE_DURATION)) = THE ATTACK HITBOX IS ACTIVE
        self.attack_progress = 0

        #HEALTH POINTS
        self.hp = 100

        #PLAYER DAMAGE
        self.DMG = 20

        #PLAYER SPEED (pixels per frame)
        self.SPEED = 4

        #THE ANGLE FOR THE FACING DIRECTION in degrees
        self.angle = 0

#####################################################################################################################################################################################################
#   CUSTOM DRAW FUNCTION, USED TO DECIDE WHAT SURF TO BLIT AT WHAT ANGLE
#####################################################################################################################################################################################################
    def custom_draw(self, level):
        #choosing the image to be rendered based on the state of the player (so far, only blitting the idle surf, regardless of anything)
        chosen_image = self.img_idle[self.NUMBER].copy()

        #rotate the image using the player.angle
        chosen_image = pygame.transform.rotate(chosen_image, self.angle)

        #make a new rect to render the rotated image on
        rotated_rect = chosen_image.get_rect(center = self.rect.center)

        #drawing the image at the angle
        pygame.Surface.blit( level.display_surface, chosen_image, rotated_rect)
        
        #IMAGE FRAME DEBUG
        #pygame.draw.rect(level.display_surface, (255,255,0), rotated_rect, 3)
        
        #HITBOX DEBUG
        pygame.draw.rect(level.display_surface, ((self.NUMBER-1)*255,(self.NUMBER-2)*-255,0), self.rect, 3)

        #Attack hitbox debug
        if self.attack_hitbox != None:
            pygame.draw.rect(level.display_surface, (255,255,0), self.attack_hitbox, 3)

#####################################################################################################################################################################################################
#   ATTACK FUNCTION FOR THE PLAYER USED IN THE MAIN UPDATE FUNCTION
#####################################################################################################################################################################################################
    def attack(self, level):
        #START THE ATTACK
        if ((level.pressed_keys[pygame.K_g] and self.NUMBER == 1) or (level.pressed_keys[pygame.K_m] and self.NUMBER == 2)) and self.attack_progress == 0:
            self.attack_progress += 1
            return True

        #ATTACK CHARING
        elif self.attack_progress > 0 and self.attack_progress <= self.CHARGE_DURATION:
            self.attack_progress += 1
            return True

        #ATTACK HIT DETECTION
        elif self.attack_progress > self.CHARGE_DURATION:
            self.attack_progress += 1
            
            print(str(self.angle) + '   ' + str(self.attack_progress))

            if self.angle == 0:
                offset_x = 0
                offset_y = self.ATTACK_RANGE

            elif self.angle == 45:
                offset_x = math.sqrt(self.ATTACK_RANGE*self.ATTACK_RANGE/2)
                offset_y = math.sqrt(self.ATTACK_RANGE*self.ATTACK_RANGE/2)

            elif self.angle == 90:
                offset_x = self.ATTACK_RANGE
                offset_y = 0

            elif self.angle == 135:
                offset_x = math.sqrt(self.ATTACK_RANGE*self.ATTACK_RANGE/2)
                offset_y = -math.sqrt(self.ATTACK_RANGE*self.ATTACK_RANGE/2)

            elif self.angle == 180:
                offset_x = 0
                offset_y = -self.ATTACK_RANGE

            elif self.angle == 225:
                offset_x = -math.sqrt(self.ATTACK_RANGE*self.ATTACK_RANGE/2)
                offset_y = -math.sqrt(self.ATTACK_RANGE*self.ATTACK_RANGE/2)

            elif self.angle == 270:
                offset_x = -self.ATTACK_RANGE
                offset_y = 0

            elif self.angle == 315:
                offset_x = -math.sqrt(self.ATTACK_RANGE*self.ATTACK_RANGE/2)
                offset_y = math.sqrt(self.ATTACK_RANGE*self.ATTACK_RANGE/2)
            
            offset_x = round(offset_x)
            offset_y = round(offset_y)
            
            print(str(offset_x) + '   ' + str(offset_y))

            self.attack_hitbox = pygame.Rect(self.rect.x + offset_x, self.rect.y + offset_y, self.rect.width, self.rect.height)
            
            #end the attack
            if self.attack_progress > 2*self.CHARGE_DURATION:
                self.attack_progress = 0
                self.attack_hitbox = None



        

        

#####################################################################################################################################################################################################
#   MOVEMENT FUNCTION FOR THE PLAYER USED IN THE MAIN UPDATE FUNCTION
#####################################################################################################################################################################################################
    def movement(self, level):
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

        #find the angle of the player for use in the draw function (the angle stays the same on no input to maintaing the facing direction when the player stops)
        if x_input != 0 or y_input != 0:
            last_angle = self.angle
            self.angle = math.degrees(math.atan2(x_input, y_input))

            if self.angle < 0:      
                self.angle += 360

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
        self.rect.x += x_input
        self.rect.y += y_input

#####################################################################################################################################################################################################
#   MAIN UPDATE FUNCTION OF THE PLAYER, USED TO CALL ALL THE MOVEMENT AND PHYSICS FUNCTIONS, AS WELL AS TO HANDLE SOME LOGIC AMONG THEM
#####################################################################################################################################################################################################
    def update(self, level):

        self.movement(level)
        self.attack(level)
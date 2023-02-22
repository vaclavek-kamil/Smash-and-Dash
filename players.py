##############################################################################################
    #       #       #       #       #       #   ######  #       #####  #     # ####### ######    
import pygame   #       #       #       #       #     # #      #     #  #   #  #       #     #
import math #       #       #       #       #   ######  #      #######   # #   ####### #####
from settings import *  #       #       #       #       #      #     #    #    #       #    #
from effects import *       #       #       #   #       ###### #     #    #    ####### #     #
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
        self.img_dodge = [None, pygame.image.load('art/players/player1/dodge.png'), pygame.image.load('art/players/player2/dodge.png')]
        
        #GETTING THE COLIDER AND THE RECT TO RENDER THE IMAGES ON
        self.rect = self.img_idle[self.NUMBER].get_rect(topleft = (pos[0]-TILE_SIZE, pos[1]-TILE_SIZE))
        self.rect.width -= TILE_SIZE*2
        self.rect.height -= TILE_SIZE*2
        self.rect.topleft = pos

        #ATTACK PROGRESS -  (0 - CHARGE_DURATION) = THE ATTACK IS CHARGING
        ##################  ((CHAGRE_DURATION + 1 - (2*CHARGE_DURATION)) = THE ATTACK HITBOX IS ACTIVE
        self.attack_progress = 0
        self.attack_hitbox = None
        self.CHARGE_DURATION = 20
        self.ATTACK_RANGE = 40
        self.DMG = 20
        self.attack_cooldown = 0
        self.ATTACK_COOLDOWN = 40

        #THE AMOUNT OF FRAME A DODGE LAST, MAKING THE PLAYER IMUNE TO DAMAGE (IGNORES HITS)
        self.DODGE_DURATION = 15
        self.dodge_cooldown = 0
        self.DODGE_COOLDOWN = 40
        self.DODGE_SPEED_MULTIPLIER = 2
        self.dodge_progress = 0


        #HEALTH POINTS
        self.MAX_HP = 100
        self.hp = self.MAX_HP

        #PLAYER SPEED (pixels per frame)
        self.SPEED = 3

        #THE ANGLE FOR THE FACING DIRECTION in degrees
        self.angle = 0

#####################################################################################################################################################################################################
#   CUSTOM DRAW FUNCTION, USED TO DECIDE WHAT SURF TO BLIT AT WHAT ANGLE
#####################################################################################################################################################################################################
    def custom_draw(self, level):
        #choosing the image to be rendered based on the state of the player (so far, only blitting the idle surf, regardless of anything)
        if self.dodge_progress > 0:
            chosen_image = self.img_dodge[self.NUMBER].copy()

        elif self.attack_progress == 0:
            chosen_image = self.img_idle[self.NUMBER].copy()

        elif self.attack_progress <= self.CHARGE_DURATION:
            chosen_image = self.img_charge[self.NUMBER].copy()

        else:
            chosen_image = self.img_hit[self.NUMBER].copy()

        #rotate the image using the player.angle
        chosen_image = pygame.transform.rotate(chosen_image, self.angle)

        #make a new rect to render the rotated image on
        rotated_rect = chosen_image.get_rect(center = self.rect.center)

        #drawing the image at the angle
        pygame.Surface.blit( level.display_surface, chosen_image, rotated_rect)
        
        #IMAGE FRAME DEBUG
        #pygame.draw.rect(level.display_surface, (255,255,0), rotated_rect, 3)
        
        #HITBOX DEBUG
        #pygame.draw.rect(level.display_surface, ((self.NUMBER-1)*255,(self.NUMBER-2)*-255,0), self.rect, 3)

        #Attack hitbox debug
        #if self.attack_hitbox != None:
        #   pygame.draw.rect(level.display_surface, (255,255,0), self.attack_hitbox, 3)


#########################################################################################################################################################
#   MOVING THE PLAYER WHILE CHECKING FOR COLLISIONS WITH WALL SPRITES
#########################################################################################################################################################
    def move_and_colide(self, x, y, level):    
        #HORIZONTAL
        if x != 0:
            self.rect.x += x
            for obstacle in level.obstacles_sprites:
                if self.rect.colliderect(obstacle) and obstacle != self:
                    if x > 0:
                        self.rect.right = obstacle.rect.left
                    elif x < 0:
                        self.rect.left = obstacle.rect.right

        #VERTICAL
        if y != 0:
            self.rect.y += y
            for obstacle in level.obstacles_sprites:
                if self.rect.colliderect(obstacle) and obstacle != self:
                    if y > 0:
                        self.rect.bottom = obstacle.rect.top
                    elif y < 0:
                        self.rect.top = obstacle.rect.bottom
        
#####################################################################################################################################################################################################
#   FUNCTION USED TO DETECT WHEN ONE PLAYER HITS THE OTHER
#####################################################################################################################################################################################################
    def hit_detect(self, level):
        if self.attack_hitbox != None:
            for sprite in level.player_sprites:
                if sprite.NUMBER != self.NUMBER:
                    if self.attack_hitbox.colliderect(sprite.rect):
                        
                        #DAMAGING THE ENEMY PLAYER ON HIT (only on the first frame of the attack)
                        if sprite.dodge_progress == 0:
                            sprite.hp -= self.DMG
                            #creating an instance of a splash effect on hit
                            Splash(sprite.rect.center, level.effects_sprites)
                            
                            if sprite.hp <= 0:
                                level.gameloop = False
                                level.pause_state = 'end'
                                
                        

                        #debug for the damage done
                        #print('player ' + str(sprite.NUMBER) + ' hp: ' + str(sprite.hp))
                        
                        return True
                    
        return False

#####################################################################################################################################################################################################
#   ATTACK FUNCTION FOR THE PLAYER USED IN THE MAIN UPDATE FUNCTION
#####################################################################################################################################################################################################
    def attack(self, level):
        #START THE ATTACK
        if ((level.pressed_keys[pygame.K_g] and self.NUMBER == 1 and self.attack_cooldown == 0) or (level.pressed_keys[pygame.K_n] and self.NUMBER == 2 and self.attack_cooldown == 0)) and self.attack_progress == 0:
            self.attack_progress += 1
            return True

        #ATTACK CHARING
        elif self.attack_progress > 0 and self.attack_progress <= self.CHARGE_DURATION:
            self.attack_progress += 1
            return True

        #ATTACK HITBOX
        elif self.attack_progress > self.CHARGE_DURATION:
            self.attack_progress += 1

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

            self.attack_hitbox = pygame.Rect(self.rect.x + offset_x, self.rect.y + offset_y, self.rect.width, self.rect.height)
            
            #calling the hit detection function
            if self.attack_progress == self.CHARGE_DURATION + 2:
                self.hit_detect(level)

            #end the attack
            if self.attack_progress > 2*self.CHARGE_DURATION:
                self.attack_progress = 0
                self.attack_hitbox = None
                self.attack_cooldown = self.ATTACK_COOLDOWN

            return True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        return False

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

        #restricting the player movement when attacking 
        if self.attack_progress > 0 and self.attack_progress <= self.CHARGE_DURATION:
            y_input = round(y_input * 0.5)
            x_input = round(x_input * 0.5)

        elif self.attack_progress > self.CHARGE_DURATION:
            y_input = 0
            x_input = 0
            
        #CHECKING FOR COLISIONS WITH WALLS WILL BE HERE#
        #                                              #
        #                                              #
        #                                              #
        ################################################

        #applying the directional vector onto the players position
        self.move_and_colide(x_input, y_input, level)
        
#####################################################################################################################################################################################################
#   FUNCTION FOR THE DODGE MECHANIC
#####################################################################################################################################################################################################
    def dodge(self, level):
        #DODGE KEY PRESSED BOOL (JUST TO MAKE THE LATTER CONDITION EASIER TO READ)
        if (level.pressed_keys[pygame.K_f] and self.NUMBER == 1) or (level.pressed_keys[pygame.K_m] and self.NUMBER == 2):
            key_pressed = True 
        else:
            key_pressed = False


        if (self.attack_progress == 0 and key_pressed and self.dodge_cooldown == 0) or self.dodge_progress > 0:
            
            if self.angle == 0:
                x_input = 0
                y_input = 1

            elif self.angle == 45:
                x_input = 1
                y_input = 1

            elif self.angle == 90:
                x_input = 1
                y_input = 0

            elif self.angle == 135:
                x_input = 1
                y_input = -1

            elif self.angle == 180:
                x_input = 0
                y_input = -1

            elif self.angle == 225:
                x_input = -1
                y_input = -1
            
            elif self.angle == 270:
                x_input = -1
                y_input = 0

            elif self.angle == 315:
                x_input = -1
                y_input = 1
            


            #Aplying the dodge speed multiplier
            x_input *= self.DODGE_SPEED_MULTIPLIER #* (1/(self.DODGE_DURATION - self.dodge_progress + 1))
            y_input *= self.DODGE_SPEED_MULTIPLIER #* (1/(self.DODGE_DURATION - self.dodge_progress + 1))


            #diagonal movement
            if y_input != 0 and x_input != 0:
                diagonal = math.sqrt(self.SPEED*self.SPEED/2)
            
                x_input *= round(diagonal)
                y_input *= round(diagonal)

            #Multiplying the input by the player speed to turn it into a directional vector
            else:
                y_input *= self.SPEED
                x_input *= self.SPEED

            

            #aplying the dodge movement
            self.move_and_colide(x_input, y_input, level)
        

            #dodge progress logic
            self.dodge_progress += 1

            if self.dodge_progress > self.DODGE_DURATION:
                self.dodge_progress = 0
                self.dodge_cooldown = self.DODGE_COOLDOWN


            return True

        #letting the dodge cooldown pass by on no dodge
        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= 1
        return False
#####################################################################################################################################################################################################
#   MAIN UPDATE FUNCTION OF THE PLAYER, USED TO CALL ALL THE MOVEMENT AND PHYSICS FUNCTIONS, AS WELL AS TO HANDLE SOME LOGIC AMONG THEM
#####################################################################################################################################################################################################
    def update(self, level):

        if self.dodge(level) == False:
            self.movement(level)
            self.attack(level)
       
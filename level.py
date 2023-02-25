import pygame
from settings import *
from tiles import *
from players import *
from effects import *
from ui import *

class Level:
#initialization of the Level class
    def __init__(self):
        #getting the display surface from the library
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.floor_sprites = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.effects_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()

        #sprite setup
        self.pressed_keys = pygame.key.get_pressed()

        #start screen tips
        start_screen_font = pygame.font.Font('freesansbold.ttf', 32)
        self.START_SCREEN_TEXT_1 = start_screen_font.render('Player 1:          WASD - move          G - Attack          F - Dodge', True, (255,255,255))
        self.START_SCREEN_TEXT_2 = start_screen_font.render('Player 2:        Arrows - move          N - Attack          M - Dodge', True, (255,255,255))

        self.start_text_rect1 = self.START_SCREEN_TEXT_1.get_rect()
        self.start_text_rect1.x = ( WIDTH / 2 ) - ( self.start_text_rect1.width / 2 )
        self.start_text_rect1.y = ( HEIGTH / 4 ) - ( self.start_text_rect1.height / 2 )
        
        self.start_text_rect2 = self.start_text_rect1.copy()
        self.start_text_rect2.y += HEIGTH/2

        #endscreen text setup
        PURPLE = (127, 0, 255)
        ORANGE = (255, 127, 0)
        end_text_font = pygame.font.Font('freesansbold.ttf', 32)
        continue_text_font = pygame.font.Font('freesansbold.ttf', 16)

        self.END_TEXT_P1_WINS = end_text_font.render('Purple Wins!', True, PURPLE)
        self.END_TEXT_P2_WINS = end_text_font.render('Orange Wins!', True, ORANGE)
        self.END_TEXT_P1_BG = end_text_font.render('Purple Wins!', True, (20,20,20))
        self.END_TEXT_P2_BG = end_text_font.render('Orange Wins!', True, (20,20,20))

        self.END_TEXT_TIE = end_text_font.render('Tie!', True, (245,245,245))
        self.END_TEXT_TIE_BG = end_text_font.render('Tie!', True, (20,20,20))
        
        self.end_text_rect = self.END_TEXT_P1_BG.get_rect()
        self.end_text_rect.center = (WIDTH / 2, HEIGTH / 2)
        self.end_text_rect_offset = self.end_text_rect.copy()
        self.end_text_rect_offset.x += 1
        self.end_text_rect_offset.y += 1

        self.end_text_tie_rect = self.END_TEXT_TIE.get_rect()
        self.end_text_tie_rect.center = (WIDTH / 2, HEIGTH / 2)
        self.end_text_tie_rect_offset = self.end_text_tie_rect.copy()
        self.end_text_tie_rect_offset.x += 1
        self.end_text_tie_rect_offset.y += 1

        self.CONTINUE_TEXT = continue_text_font.render('Press ESC to play again...', True, (245,245,245))
        self.CONTINUE_TEXT_BG = continue_text_font.render('Press ESC to play again...', True, (20,20,20))

        self.continue_text_rect = self.CONTINUE_TEXT.get_rect()
        self.continue_text_rect.top = self.end_text_rect.bottom
        self.continue_text_rect.y += 10
        self.continue_text_rect.x = ( WIDTH / 2 ) - ( self.continue_text_rect.width / 2 ) 

        self.continue_text_rect_offset = self.continue_text_rect.copy()
        self.continue_text_rect_offset.x += 1
        self.continue_text_rect_offset.y += 1

        #map choice setup
        self.MAP1 = pygame.image.load('art/maps/map1.png')
        self.MAP2 = pygame.image.load('art/maps/map2.png')
        self.MAP3 = pygame.image.load('art/maps/map3.png')
        
        self.map2_rect = self.MAP1.get_rect()
        self.map2_rect.center = (WIDTH / 2, HEIGTH / 2)

        self.map1_rect = self.map2_rect.copy()
        self.map1_rect.x -= ( WIDTH / 4 ) + ( self.map1_rect.width / 4 )
        
        self.map3_rect = self.map2_rect.copy()
        self.map3_rect.x += ( WIDTH / 4 ) + ( self.map1_rect.width / 4 )
        
        self.selected_map = 1
        self.selection_rect = self.map1_rect.copy()
        self.selection_rect.width += 4 
        self.selection_rect.height += 4 

        #gameloop logic variables
        self.gameloop = False
        self.pause_state = 'start' #start = before the game beggins - pause = paused during the game - end = one player or the other has won

        #ui setup
        Healthbars(self.ui_sprites)
        Staminabars(self.ui_sprites)
          
#show endscreen text based on the player who has won
    def endscreen(self, num):

        self.display_surface.blit(self.CONTINUE_TEXT_BG, self.continue_text_rect_offset)
        self.display_surface.blit(self.CONTINUE_TEXT, self.continue_text_rect)

        if num == 1:
            self.display_surface.blit(self.END_TEXT_P1_BG, self.end_text_rect_offset)   
            self.display_surface.blit(self.END_TEXT_P1_WINS, self.end_text_rect) 
            return

        if num == 2:
            self.display_surface.blit(self.END_TEXT_P2_BG, self.end_text_rect_offset)   
            self.display_surface.blit(self.END_TEXT_P2_WINS, self.end_text_rect) 
            return

        self.display_surface.blit(self.END_TEXT_TIE_BG, self.end_text_tie_rect_offset)   
        self.display_surface.blit(self.END_TEXT_TIE, self.end_text_tie_rect) 
        return
    
#place sprites on the map
    def create_map(self, map):
        for row_index, row in enumerate(WORLD_MAP[map]):        #2Dpole = [pole1,pole2,pole3]       x   x   x
                                                                                            #       x   x   x
            for col_index, col in enumerate(row):                                           #       x   x   x

                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == 'f':
                    Floor((x,y), [self.floor_sprites])

                if col == 'w':
                    Wall((x,y), [self.obstacles_sprites, self.wall_sprites])

                if col == '1':
                    Player((x,y),1, [self.player_sprites, self.obstacles_sprites])
                    Floor((x,y), [self.floor_sprites])

                if col == '2':
                    Player((x,y),2, [self.player_sprites, self.obstacles_sprites])
                    Floor((x,y), [self.floor_sprites])
    
#reset all sprites for a new game
    def reset(self):
        self.ui_sprites.empty()
        self.floor_sprites.empty()
        self.player_sprites.empty()
        self.effects_sprites.empty()
        self.obstacles_sprites.empty()
        self.wall_sprites.empty()
        
        Healthbars(self.ui_sprites)
        Staminabars(self.ui_sprites)
        
        self.pause_state = 'start'
   
#main function for the level class called in the main function - chooses whether to continue the game loop or handle UI - also handles input
    def run(self):
        #get the keyboard status, which will be used across all the update functions
        self.pressed_keys = pygame.key.get_pressed()

        if self.gameloop:
            self.play()

        else:
            if self.pause_state == 'start':
                self.pause_start()
            if self.pause_state == 'pause':
                self.pause_pause()
            if self.pause_state == 'end':
                self.pause_end()
   
#the main game loop for gameplay (calling draw and update functions)
    def play(self):
        #update the game objects
        self.player_sprites.update(self)
        self.effects_sprites.update()

        #draw the game objects 
        self.floor_sprites.draw(self.display_surface)
        self.wall_sprites.draw(self.display_surface)

        for sprite in self.ui_sprites:
            sprite.custom_draw(self)

        for sprite in self.player_sprites:
            sprite.custom_draw(self)

        self.effects_sprites.draw(self.display_surface)

        #pausing the game with the P key
        if self.pressed_keys[pygame.K_p]:
            self.pause_state = 'pause'
            self.gameloop = False

#pause state prior to the gameplay - players choose the map layout they want to play on
    def pause_start(self):
        mouse_pos = pygame.mouse.get_pos()
        selection_rect = self.map1_rect.copy()
        selected_map = None

        selection_rect.width += 15
        selection_rect.height += 15
        
        self.display_surface.fill('black')

        if self.map1_rect.collidepoint(mouse_pos):  
            selection_rect.center = self.map1_rect.center     
            selected_map = 1

        elif self.map2_rect.collidepoint(mouse_pos):
            selection_rect.center = self.map2_rect.center   
            selected_map = 2

        elif self.map3_rect.collidepoint(mouse_pos):
            selection_rect.center = self.map3_rect.center       
            selected_map = 3

        if selected_map != None:
            pygame.draw.rect(self.display_surface, (255,255,255), selection_rect, 4)

        self.display_surface.blit(self.MAP1, self.map1_rect)
        self.display_surface.blit(self.MAP2, self.map2_rect)
        self.display_surface.blit(self.MAP3, self.map3_rect)
        self.display_surface.blit(self.START_SCREEN_TEXT_1, self.start_text_rect1)
        self.display_surface.blit(self.START_SCREEN_TEXT_2, self.start_text_rect2)

        if pygame.mouse.get_pressed(3)[0] and selected_map != None:
            self.create_map(selected_map)
            self.gameloop = True    

#pause used during the gameplay - start the pause with P and end it with ESCAPE
    def pause_pause(self):
        self.gameloop = False
        if self.pressed_keys[pygame.K_ESCAPE]:
            self.gameloop = True

#pause the game after one of the players has won - display the winner and give the choice to play again
    def pause_end(self):
        number = None

        for player in self.player_sprites:
            if player.hp > 0:
               number = player.NUMBER

        self.endscreen(number)

        if self.pressed_keys[pygame.K_ESCAPE]:
            self.reset()

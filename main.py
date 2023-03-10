import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.level = Level()
        pygame.display.set_icon(pygame.image.load('art/icon/icon.png'))
        pygame.display.set_caption('Smash and Dash')


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #run the level method
            self.level.run()
                        
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
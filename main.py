import pygame, sys
from settings import *
from debug import debug 
from level import Level
from player import Player
class Game:
    def __init__(self):

        #setting up
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #For the screen size, and grabbed from settings
        pygame.display.set_caption('Inevitability')
        self.clock = pygame.time.Clock() 

        self.level = Level()

#This keeps the game opened, so while application is not exited, it will run with a refresh rate of the stated value
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
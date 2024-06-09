import pygame, sys
from settings import *
from debug import debug 
from level import Level
from player import Player

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, MENU_FONT_SIZE)
        self.options = MENU_OPTIONS
        self.selected_index = 0
        
        # Load background image
        self.background_image = pygame.image.load('graphics/tilemap/MyMapBack.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

    def display_menu(self):
        # Blit the background image
        self.screen.blit(self.background_image, (0, 0))

        for i, option in enumerate(self.options):
            if i == self.selected_index:
                color = (255, 0, 0)  # Red for the selected option
            else:
                color = MENU_FONT_COLOR
            text_surface = self.font.render(option, True, color)
            x = self.screen.get_width() // 2 - text_surface.get_width() // 2
            y = self.screen.get_height() // 2 + i * MENU_FONT_SIZE
            self.screen.blit(text_surface, (x, y))
        pygame.display.update()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected_index] == 'Start Game':
                        return 'start_game'
                    elif self.options[self.selected_index] == 'Quit':
                        pygame.quit()
                        sys.exit()
        return 'menu'
    
class Game:
    def __init__(self):

        #setting up
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #For the screen size, and grabbed from settings
        pygame.display.set_caption('Inevitability')
        self.clock = pygame.time.Clock() 

        self.level = Level()
        self.menu = Menu(self.screen)
        self.state = 'menu'

#This keeps the game opened, so while application is not exited, it will run with a refresh rate of the stated value
    def run(self):
        while True:
            if self.state == 'menu':
                self.menu.display_menu()
                self.state = self.menu.handle_input()
            elif self.state == 'start_game':
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
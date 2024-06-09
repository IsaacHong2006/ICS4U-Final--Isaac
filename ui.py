import pygame
from settings import *

class User_Interface:
    def __init__(self):
        
        #General Informations
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #bars 
        self.health_bar_rec = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_TALL)
        self.enrgy_bar_rec = pygame.Rect(10, 30, ENERGY_BAR_WIDTH, BAR_TALL)

    def show_bar(self,current,max_amt,bg_rect,colour):
        #draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOUR,bg_rect)

        #convert stats to pixels
        ratio = current / max_amt
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #drawing bar
        pygame.draw.rect(self.display_surface,colour,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR,current_rect,3)

    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOUR)
        x = self.display_surface.get_size()[0] - 25
        y = self.display_surface.get_size()[1] - 30
        text_rect = text_surf.get_rect(bottomright = (x,y))
        
        pygame.draw.rect(self.display_surface, UI_BG_COLOUR,text_rect.inflate(35,35))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, text_rect.inflate(35,35),3)

    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rec,HEALTH_COLOUR)
        self.show_bar(player.energy,player.stats['energy'],self.enrgy_bar_rec,ENRGY_COLOUR)

        self.show_exp(player.exp)
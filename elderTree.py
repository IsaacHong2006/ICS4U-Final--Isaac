import pygame
from random import choice
from settings import *

class Elder_Tree(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/treesandbolders/5.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.interacted = False

    def interact(self):
        self.interacted = True

class GambleMenu:
    def __init__(self, player):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.options = ['Gamble', 'Hard Work']  # Example options
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Dimensions and item creation
        self.height = self.display_surface.get_size()[1] * 0.50
        self.width = self.display_surface.get_size()[0] // (len(self.options) + 1)
        self.create_items()

        # Selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.interaction_paused = False  # Flag to manage interaction state

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < len(self.options) - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self)

    def selection_cooldown(self):
        if not self.can_move:
            currently = pygame.time.get_ticks()
            if currently - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []

        for index, option in enumerate(self.options):
            # Horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // len(self.options)
            left = (index * increment) + (increment - self.width) // 2

            # Vertical position
            top = self.display_surface.get_size()[1] * 0.1

            # Creating the item objects
            item = GambleItem(left, top, self.width, self.height, index, self.font, option)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            item.display(self.display_surface, self.selection_index)

    def exit(self):
        self.game_paused = False
        # Additional cleanup if needed


class GambleItem:
    def __init__(self, l, t, w, h, index, font, option):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font
        self.option = option

    def display(self, surface, selected_index):
        selected = self.index == selected_index

        # Title
        colour = TEXT_COLOUR_SELECTED if selected else TEXT_COLOUR
        title_surf = self.font.render(self.option, False, colour)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        # Draw
        pygame.draw.rect(surface, BAR_COLOUR_SELECTED if selected else BAR_COLOUR, self.rect, 5)
        surface.blit(title_surf, title_rect)

    def trigger(self, menu):
        if self.option == 'Hard Work':
            menu.exit()  # Call the exit method of GambleMenu
        else:
            # Example logic: give the player a random reward or penalty
            reward_or_penalty = choice(['reward', 'penalty'])
            if reward_or_penalty == 'reward':
                menu.player.exp += 100  
            else:
                menu.player.health -= 10  
                menu.player.exp -= 200

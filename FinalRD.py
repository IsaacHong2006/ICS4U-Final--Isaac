# import pygame
# from sys import exit

# pygame.init()
# screen = pygame.display.set_mode((1800, 800))
# pygame.display.set_caption("Inevitability")
# clock = pygame.time.Clock()

# surface_Test = pygame.Surface((100,200))
# surface_Test.fill('purple')
# #Game is going to be running in a for loop until it is exited
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#     screen.blit(surface_Test, (750,300)) #backgroundcolour
#     #draw all the elements
#     #update everything
#     pygame.display.update()
#     clock.tick(60)

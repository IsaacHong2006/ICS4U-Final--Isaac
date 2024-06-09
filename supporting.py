from csv import reader
from os import walk
import pygame 

def import_csv_layout(path):
    terrains = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter= ',')
        for row in layout:
            terrains.append(list(row))
        return terrains
    
def import_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

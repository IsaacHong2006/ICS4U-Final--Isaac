#The game requirements
#Refer to this file for all requirements, and makes it alot more readable
WIDTH = 1280 
HEIGHT = 720
FPS = 60
TILESIZE = 32

#UI Management
BAR_TALL = 15
HEALTH_BAR_WIDTH = 150
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/Fonts/Coffee Spark.ttf'
UI_FONT_SIZE = 24

#colours
WATER_COLOUR = '71ddee'
UI_BG_COLOUR = 'black'
UI_BORDER_COLOUR = 'grey'
TEXT_COLOUR = 'white'

#ui colours
HEALTH_COLOUR = 'red'
UI_BORDER_COLOUR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOUR_SELECTED = '#111111'
BAR_COLOUR = '#EEEEEE'
BAR_COLOUR_SELECTED = 'blue'
UPGRADE_BG_COLOUR_SELECTED = 'purple'

MENU_FONT_SIZE = 50
MENU_FONT_COLOR = (255, 255, 255)  # White
MENU_BG_COLOR = (0, 0, 0)  # Black
MENU_OPTIONS = ['Start Game', 'Quit']

# enemy
thingymabobs={
    'arch-angel': {'health': 20000, 'exp': 25000, 'damage': 500, 'attack_type': 'Echos of the heavens', 'speed': 10, 'resistance': 5, 'attack_radius': 80, 'notice_radius': 100},
    'blobby': {'health': 250, 'exp': 125, 'damage': 80, 'attack_type': 'Blobs', 'speed': 4, 'resistance': 3, 'attack_radius': 20, 'notice_radius': 60}, 
    'slime': {'health': 10, 'exp': 10, 'damage': 5, 'attack_type': 'Sticky', 'speed': 2, 'resistance': 2, 'attack_radius': 10, 'notice_radius': 20}
}


import pygame
import os
import json

pygame.init()

# Main variables
FPS = 60 # upper bound for frames per second of the game
DEFAULT_WIDTH, DEFAULT_HEIGHT = 1200, 675 # 5/8 of the screen
running = True # boolean to indicate whether main game loop is running
WHITE = (255, 255, 255) # colour for rendering text
PREV_MENU = 0 # used to store the index of the previously open menu in the menus list

# Variables controlled via settings
with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "r") as f:
    content = json.loads(f.read())
    soundEnabled = content["sound"] # boolean to indicate whether sound effects should be enabled
    historical = content["historical"] # boolean to indicate which assets to use

    info = pygame.display.Info() # temporary info object, in order to access current_h and current_w attributes
    if content["fullscreen"]:
        SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h # Set width and height to that of the display if fullscreen
    else:
        SCREEN_WIDTH, SCREEN_HEIGHT = DEFAULT_WIDTH, DEFAULT_HEIGHT # Otherwise, set it to the default width and height stored

# Colours
BACKGROUND_PEACH = (201, 144, 56) # background colour

# Dice distributions
TETRA_DIST = {0:(0, 0.5), 1:(0.5, 1)} # Normal tetrahedronal dice
UR_TOTAL_DIST = {0:0.0625, 1:0.25 ,2:0.375, 3:0.25, 4:0.0625}

# Main structures
gameEngine = None # To be initialised by clickActions of certain buttons
singleplayerOpponent = None

# Assets:
if historical: folder = "historical" # chooses between historical or modern assets
else: folder = "modern"

# Images
gameIconPath = os.path.join(os.getcwd(), folder, "img/icon.ico")

gameOfUrLogoPath = os.path.join(os.getcwd(), folder, "img/logo.png")
buttonPath = os.path.join(os.getcwd(), folder, "img/button.png")
settingsPath = os.path.join(os.getcwd(), folder, "img/settings.png")
fontPath = os.path.join(os.getcwd(), folder, "font/Louis George Cafe.ttf")
closePath = os.path.join(os.getcwd(), folder, "img/close.png")
tutorialPath = os.path.join(os.getcwd(), folder, "img/tutorial.png")
transparentPath = os.path.join(os.getcwd(), folder, "img/transparent.png") # transparent png to render text on top of
buttonHighlightPath = os.path.join(os.getcwd(), folder, "img/button_highlighted.png")

squarePath = os.path.join(os.getcwd(), folder, "img/square.png")
squareHighlightPath = os.path.join(os.getcwd(), folder, "img/square_highlighted.png")
mosaicPath = os.path.join(os.getcwd(), folder, "img/mosaic.png")
mosaicHighlightPath = os.path.join(os.getcwd(), folder, "img/mosaic_highlighted.png")
lightTilePath = os.path.join(os.getcwd(), folder, "img/lighttile.png")
darkTilePath = os.path.join(os.getcwd(), folder, "img/darktile.png")
lightTileHighlightPath = os.path.join(os.getcwd(), folder, "img/lighttile_highlighted.png")
darkTileHighlightPath = os.path.join(os.getcwd(), folder, "img/darktile_highlighted.png")
lightIconPath = os.path.join(os.getcwd(), folder, "img/lighticon.png")
darkIconPath = os.path.join(os.getcwd(), folder, "img/darkicon.png")
lightIconHighlightPath = os.path.join(os.getcwd(), folder, "img/lighticon_highlighted.png")
darkIconHighlightPath = os.path.join(os.getcwd(), folder, "img/darkicon_highlighted.png")
barPath = os.path.join(os.getcwd(), folder, "img/bar.png")

tetrahedronImagePaths = [
    [
        os.path.join(os.getcwd(), folder, "img/tetrahedron_0_1.png"), os.path.join(os.getcwd(), folder, "img/tetrahedron_0_2.png"), os.path.join(os.getcwd(), folder, "img/tetrahedron_0_3.png")
    ],
    [
        os.path.join(os.getcwd(), folder, "img/tetrahedron_1_1.png"), os.path.join(os.getcwd(), folder, "img/tetrahedron_1_2.png"), os.path.join(os.getcwd(), folder, "img/tetrahedron_1_3.png")
    ]
] # 2D array of paths for the tetrahedronal die

toggleOnPath = os.path.join(os.getcwd(), folder, "img/toggleOn.png")
toggleOffPath = os.path.join(os.getcwd(), folder, "img/toggleOff.png") # Assets for the toggle used in settings and experimental menu

# Fonts
fontScale = SCREEN_WIDTH/1920

font = pygame.font.Font(fontPath, int(80*fontScale)) # This is the main font that will be used
smallFont = pygame.font.Font(fontPath, int(40*fontScale)) # Smaller font for smaller buttons

# Sounds
tileSoundPath = os.path.join(os.getcwd(), folder, "soundfx/tile.ogg") # played when a tile is moved
tileSound = pygame.mixer.Sound(tileSoundPath)
diceSoundPath = os.path.join(os.getcwd(), folder, "soundfx/dice.ogg") # played when dice is rolled
diceSound = pygame.mixer.Sound(diceSoundPath)
failSoundPath = os.path.join(os.getcwd(), folder, "soundfx/fail.ogg") # played when a turn is skipped due to 0 rolled or no legal moves
failSound = pygame.mixer.Sound(failSoundPath)
winSoundPath = os.path.join(os.getcwd(), folder, "soundfx/win.ogg") # played when a player wins
winSound = pygame.mixer.Sound(winSoundPath)



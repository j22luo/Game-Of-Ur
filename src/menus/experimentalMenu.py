import sys
import os

# add the different subfolders containing python files to the system path so that different classes can be imported
sys.path.insert(0, os.path.join(os.getcwd(), "src/menus"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/sprites"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/opponents"))

import parameters as p
from menu import Menu
from sprites.basicSprites import *

# Sprite objects
settingsButton = Button( # Button to redirect to the settings menu, placed in the same place in every menu
    (p.SCREEN_WIDTH*0.95, p.SCREEN_WIDTH*0.01), # upper right corner
    (p.SCREEN_WIDTH*0.04, p.SCREEN_WIDTH*0.04), # relatively small
    imagePath=p.settingsPath
)

closeButton = Button( # Button to close the current menu, placed in the same place in every menu
    (p.SCREEN_WIDTH*0.01, p.SCREEN_WIDTH*0.01), # upper left corner
    (p.SCREEN_WIDTH*0.04, p.SCREEN_WIDTH*0.04), # same size as the settings button
    imagePath=p.closePath
)

playButton = Button( # Button to play the game, redirects to game play menu
    (p.SCREEN_WIDTH * 0.675, p.SCREEN_HEIGHT * 0.75), # Rightmost third with some borders, lower down on the screen.
    (p.SCREEN_WIDTH * 0.3, p.SCREEN_HEIGHT * 0.2), # Wide rectangular shape
    text=p.font.render("Play", True, p.WHITE),
    imagePath=p.buttonPath
)

# Menu instantiation

experimentalMenu = Menu(
    [settingsButton, closeButton, playButton]
)



import sys
import os

# add the different subfolders containing python files to the system path so that different classes can be imported
sys.path.insert(0, os.path.join(os.getcwd(), "src/menus"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/sprites"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/opponents"))

import parameters as p
from menu import *
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

tutorialText = MySprite( # "Tutorial" title
    (p.SCREEN_WIDTH*0.42, p.SCREEN_WIDTH*0.005), # In the middle of the screen
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.2), # Wide text
    text=p.font.render("Tutorial", True, p.WHITE),
)

tutorialImage = MySprite( # Temporary image for a tutorial of the game, need to create this in later sprints
    (p.SCREEN_WIDTH*0.01, p.SCREEN_HEIGHT*0.12), # Below the tutorial text
    (p.SCREEN_WIDTH*0.98, p.SCREEN_HEIGHT*0.86), # The image is as wide as the screen
    imagePath=p.tutorialPath
)
# Menu instantiation

tutorialMenu = Menu(
    [settingsButton, closeButton, tutorialText, tutorialImage],
)


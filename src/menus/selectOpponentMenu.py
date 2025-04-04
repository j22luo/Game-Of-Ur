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

selectOpponentText = MySprite( # "Choose your opponent!" title
    (p.SCREEN_WIDTH*0.30, p.SCREEN_WIDTH*0.005), # Middle of screen
    (p.SCREEN_WIDTH*0.6, p.SCREEN_HEIGHT*0.2), # Wide text
    text=p.font.render("Choose your opponent!", True, p.WHITE),
)

easyButton = Toggle( # Easy Button, should highlight when clicked and unhighlight when the other opponent buttons are clicked.
    (p.SCREEN_WIDTH * 0.2, p.SCREEN_HEIGHT * 0.25), # Leftmost third
    (p.SCREEN_WIDTH * 0.2, p.SCREEN_WIDTH * 0.2), # Square shape
    text=p.font.render("Easy", True, p.WHITE),
    offImagePath=p.buttonPath,
    onImagePath=p.buttonHighlightPath
)

mediumButton = Toggle( # Medium button
    (p.SCREEN_WIDTH * 0.6, p.SCREEN_HEIGHT * 0.25), # Middle third
    (p.SCREEN_WIDTH * 0.2, p.SCREEN_WIDTH * 0.2), 
    text=p.font.render("Medium", True, p.WHITE),
    offImagePath=p.buttonPath,
    onImagePath=p.buttonHighlightPath
)

playButton = Button( # Button to play the game, redirects to game play menu
    (p.SCREEN_WIDTH * 0.4, p.SCREEN_HEIGHT * 0.75), # Directly below the medium button
    (p.SCREEN_WIDTH * 0.2, p.SCREEN_HEIGHT * 0.2),  # Same width as the medium button
    text=p.font.render("Play", True, p.WHITE),
    imagePath=p.buttonPath,
    isActive = False
)

# Menu instantiation

selectOpponentMenu = Menu(
    [settingsButton, closeButton, selectOpponentText, easyButton, mediumButton, playButton]
)





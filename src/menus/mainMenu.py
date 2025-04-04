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

gameOfUrLogo = MySprite( # Temporary logo for the main menu, need to update the asset later
    (p.SCREEN_WIDTH*0.01, p.SCREEN_WIDTH*0.01), # small ~10px border
    (p.SCREEN_WIDTH*0.48, p.SCREEN_HEIGHT*0.96), # takes up left half of the surface
    imagePath=p.gameOfUrLogoPath,
)

multiplayerButton = Button( # Button to access the multiplayer menu
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.1), # Near the top of the right half, below the Settings button
    (p.SCREEN_WIDTH*0.48, p.SCREEN_HEIGHT*0.25), # Wide button
    text=p.font.render("Local Multiplayer", True, p.WHITE),
    imagePath=p.buttonPath
)

singleplayerButton = Button( # Access singleplayer menu
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.37), # Below the multiplayer button
    (p.SCREEN_WIDTH*0.48, p.SCREEN_HEIGHT*0.25), # Same width
    text=p.font.render("Singleplayer", True, p.WHITE),
    imagePath=p.buttonPath
)

tutorialButton = Button( # Access the tutorial
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.64), # Below the singleplayer button
    (p.SCREEN_WIDTH*0.23, p.SCREEN_HEIGHT*0.25), # Half as wide as the buttons above
    text=p.font.render("Tutorial", True, p.WHITE),
    imagePath=p.buttonPath
)

quitButton = Button( # Quits the game
    (p.SCREEN_WIDTH*0.75, p.SCREEN_HEIGHT*0.64), # Below the singleplayer button
    (p.SCREEN_WIDTH*0.23, p.SCREEN_HEIGHT*0.25), # Same width as tutorial button, to the right of it
    text=p.font.render("Quit", True, p.WHITE),
    imagePath=p.buttonPath
)

# Menu instantiation

mainMenu = Menu(
    [settingsButton, gameOfUrLogo, multiplayerButton, singleplayerButton, tutorialButton, quitButton],
    isVisible=True,
)




import sys
import os

# add the different subfolders containing python files to the system path so that different classes can be imported
sys.path.insert(0, os.path.join(os.getcwd(), "src/menus"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/sprites"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/opponents"))

import parameters as p
from menu import Menu
from sprites.basicSprites import *

# Light menu

# Sprite objects
lightSettingsButton = Button( # Button to redirect to the settings menu, placed in the same place in every menu
    (p.SCREEN_WIDTH*0.95, p.SCREEN_WIDTH*0.01), # upper right corner
    (p.SCREEN_WIDTH*0.04, p.SCREEN_WIDTH*0.04), # relatively small
    imagePath=p.settingsPath
)

lightCongratulationsText = MySprite( # Congratulation message for either player, should update based on the 
                                # outcome of the previous game play menu
    (p.SCREEN_WIDTH * 0.22, p.SCREEN_HEIGHT * 0.1), # Roughly central
    (p.SCREEN_WIDTH * 0.6, p.SCREEN_HEIGHT * 0.2), # Wide text
    text=p.font.render("Light Player Wins!", True, p.WHITE),
)

lightPlayAgainButton = Button( # Button which redirects to the game play menu with the same configuration for the game engine
    (p.SCREEN_WIDTH * 0.1, p.SCREEN_HEIGHT * 0.75), # Lower down and occupies the left half
    (p.SCREEN_WIDTH * 0.3, p.SCREEN_WIDTH * 0.1), # Wide button
    text=p.font.render("Play Again", True, p.WHITE),
    imagePath=p.buttonPath
)

lightMainMenuButton = Button( # Button redirecting to main menu
    (p.SCREEN_WIDTH * 0.6, p.SCREEN_HEIGHT * 0.75), # Lower down and occupies the right half
    (p.SCREEN_WIDTH * 0.3, p.SCREEN_WIDTH * 0.1), # Wide button
    text=p.font.render("Main Menu", True, p.WHITE),
    imagePath=p.buttonPath
)

# Menu instantiation

lightWinnerMenu = Menu(
    [lightSettingsButton, lightCongratulationsText, lightPlayAgainButton, lightMainMenuButton]
)



# Dark menu

# Sprite objects
darkSettingsButton = Button( # Button to redirect to the settings menu, placed in the same place in every menu
    (p.SCREEN_WIDTH*0.95, p.SCREEN_WIDTH*0.01), # upper right corner
    (p.SCREEN_WIDTH*0.04, p.SCREEN_WIDTH*0.04), # relatively small
    imagePath=p.settingsPath
)

darkCongratulationsText = MySprite( # Congratulation message for either player, should update based on the 
                                # outcome of the previous game play menu
    (p.SCREEN_WIDTH * 0.22, p.SCREEN_HEIGHT * 0.1), # Roughly central
    (p.SCREEN_WIDTH * 0.6, p.SCREEN_HEIGHT * 0.2), # Wide text
    text=p.font.render("Dark Player Wins!", True, p.WHITE),
)

darkPlayAgainButton = Button( # Button which redirects to the game play menu with the same configuration for the game engine
    (p.SCREEN_WIDTH * 0.1, p.SCREEN_HEIGHT * 0.75), # Lower down and occupies the left half
    (p.SCREEN_WIDTH * 0.3, p.SCREEN_WIDTH * 0.1), # Wide button
    text=p.font.render("Play Again", True, p.WHITE),
    imagePath=p.buttonPath
)

darkMainMenuButton = Button( # Button redirecting to main menu
    (p.SCREEN_WIDTH * 0.6, p.SCREEN_HEIGHT * 0.75), # Lower down and occupies the right half
    (p.SCREEN_WIDTH * 0.3, p.SCREEN_WIDTH * 0.1), # Wide button
    text=p.font.render("Main Menu", True, p.WHITE),
    imagePath=p.buttonPath
)

darkWinnerMenu = Menu(
    [darkSettingsButton, darkCongratulationsText, darkPlayAgainButton, darkMainMenuButton]
)


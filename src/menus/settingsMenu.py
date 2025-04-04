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
closeButton = Button( # Button to close the current menu, placed in the same place in every menu
    (p.SCREEN_WIDTH*0.01, p.SCREEN_WIDTH*0.01), # upper left corner
    (p.SCREEN_WIDTH*0.04, p.SCREEN_WIDTH*0.04), # same size as the settings button
    imagePath=p.closePath
)

settingsText = MySprite( # "Settings" title
    (p.SCREEN_WIDTH*0.41, p.SCREEN_WIDTH*0.005), # In the middle of the screen
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.2), # Wide text
    text=p.font.render("Settings", True, p.WHITE),
)

soundToggle = Toggle( # Toggle for sound, modifies p.soundEnabled
    (p.SCREEN_WIDTH * 0.7, p.SCREEN_HEIGHT * 0.25), # right of text and 1/4 the way down the screen
    (p.SCREEN_WIDTH * 0.12, p.SCREEN_HEIGHT * 0.1), # takes up half of screen width roughly
    onImagePath=p.toggleOnPath,
    offImagePath = p.toggleOffPath
)

themeToggle = Toggle( # Toggle for theme, modifies p.historical
    (p.SCREEN_WIDTH * 0.7, p.SCREEN_HEIGHT * 0.5), # roughly central and 1/4 the way down the screen
    (p.SCREEN_WIDTH * 0.12, p.SCREEN_HEIGHT * 0.1), # takes up half of screen width roughly
    onImagePath=p.toggleOnPath,
    offImagePath = p.toggleOffPath
)

startUpToggle = Toggle( # Toggle for size of screen upon startup, modifies p.fullscreen
    (p.SCREEN_WIDTH * 0.7, p.SCREEN_HEIGHT * 0.75), # roughly central and 1/4 the way down the screen
    (p.SCREEN_WIDTH * 0.12, p.SCREEN_HEIGHT * 0.1), # takes up half of screen width roughly
    onImagePath=p.toggleOnPath,
    offImagePath = p.toggleOffPath
)

soundText = MySprite( # Text to describe what the sound toggle does
    (p.SCREEN_WIDTH*0.1, p.SCREEN_HEIGHT*0.25), # To the left of sound toggle
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.2),
    text=p.font.render("Sound Effects", True, p.WHITE),
)

themeText = MySprite( # Text to describe what the theme toggle does
    (p.SCREEN_WIDTH*0.1, p.SCREEN_HEIGHT*0.5), # To the left of theme toggle
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.2),
    text=p.font.render("Historical theme", True, p.WHITE),
)

startUpText = MySprite( # Text to describe what the start up toggle does
    (p.SCREEN_WIDTH*0.1, p.SCREEN_HEIGHT*0.75), # To the left of start up toggle
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.2),
    text=p.font.render("Fullscreen", True, p.WHITE),
)

disclaimerText = MySprite( # Text to inform that changes made to theme and fullscreen will be made after restarting
    (p.SCREEN_WIDTH*0.1, p.SCREEN_HEIGHT*0.9), # Underneath the final
    (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.2),
    text=p.smallFont.render("Changes to Theme and Fullscreen will be made after restarting.", True, p.WHITE),
)
# Menu instantiation

settingsMenu = Menu(
    [closeButton, settingsText, soundToggle, themeToggle, startUpToggle, soundText, themeText, startUpText, disclaimerText],
)




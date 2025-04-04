import sys
import os
import random
import json

# add the different subfolders containing python files to the system path so that different classes can be imported
sys.path.insert(0, os.path.join(os.getcwd(), "src/menus"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/sprites"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/opponents"))

import pygame   
import parameters as p # import all variables and objects declared in parameters

from menus.mainMenu import mainMenu
from menus.tutorialMenu import tutorialMenu
from menus.settingsMenu import settingsMenu
from menus.gamePlayMenu import createGamePlayMenu
from menus.selectOpponentMenu import selectOpponentMenu
from menus.winnerMenu import lightWinnerMenu, darkWinnerMenu
from menus.experimentalMenu import experimentalMenu

gamePlayMenu = tutorialMenu # Act as a placeholder

pygame.init()
pygame.display.set_caption("Game of Ur")

icon = pygame.image.load(p.gameIconPath)
pygame.display.set_icon(icon) # Set the icon for the game

clock = pygame.time.Clock() # controls how many frames are processed per second
WIN = pygame.display.set_mode((p.SCREEN_WIDTH, p.SCREEN_HEIGHT)) # initialises a window to draw sprites on and implicitly initialise pygame.display
WIN.fill(p.BACKGROUND_PEACH)  # fill the background with an orange colour
menus = [mainMenu, tutorialMenu, settingsMenu, gamePlayMenu, selectOpponentMenu, lightWinnerMenu, experimentalMenu, darkWinnerMenu] # Set of all menu objects

# Set clickActions for button sprites
menus[0].sprites[0].setClickAction(menus, 0, 2) # main menu settings button
menus[0].sprites[2].setClickAction(menus, 0, 3, createGamePlayMenu, clickAction="play game") # main menu multiplayer button
menus[0].sprites[3].setClickAction(menus, 0, 4) # main menu singleplayer button
menus[0].sprites[4].setClickAction(menus, 0, 1) # main menu tutorial button
menus[0].sprites[5].setClickAction(clickAction="quit") # main menu quit button

menus[1].sprites[0].setClickAction(menus, 1, 2) # tutorial menu settings button
menus[1].sprites[1].setClickAction(menus, 1, 0) # tutorial menu close button

menus[2].sprites[2].setClickAction(clickAction="sound") # settings menu sound toggle
menus[2].sprites[3].setClickAction(clickAction="theme") # settings menu theme toggle
menus[2].sprites[4].setClickAction(clickAction="startup") # settings menu start up toggle

with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "r") as f:
    content = json.loads(f.read())
    if content["sound"]: menus[2].sprites[2].onAction() # Render on toggle if the boolean is true for all three settings
    if content["historical"]: menus[2].sprites[3].onAction()
    if content["fullscreen"]: menus[2].sprites[4].onAction()

menus[4].sprites[0].setClickAction(menus, 4, 2) # select opponent menu settings button
menus[4].sprites[1].setClickAction(menus, 4, 0, clickAction="select opponent close") # select opponent menu close button
menus[4].sprites[3].setClickAction(menus[4].sprites[3:5], 0, menus[4].sprites[5]) # select opponent menu easy toggle
menus[4].sprites[4].setClickAction(menus[4].sprites[3:5], 1, menus[4].sprites[5]) # select opponent menu medium toggle
menus[4].sprites[5].setClickAction(menus, 4, 3, createGamePlayMenu, clickAction="play game") # select opponent menu play button

menus[5].sprites[0].setClickAction(menus, 5, 2) # light winner menu settings button
menus[5].sprites[2].setClickAction(menus, 5, 3, createGamePlayMenu, clickAction="play game") # light winner menu play again button
menus[5].sprites[3].setClickAction(menus, 5, 0) # light winner menu return to main menu button

menus[6].sprites[0].setClickAction(menus, 6, 2) # experimental menu settings button
menus[6].sprites[1].setClickAction(menus, 6, 0) # experimental menu close button
menus[6].sprites[2].setClickAction(menus, 6, 3, createGamePlayMenu, clickAction="play game") # experimental menu play button

menus[7].sprites[0].setClickAction(menus, 7, 2) # dark winner menu settings button
menus[7].sprites[2].setClickAction(menus, 7, 3, createGamePlayMenu, clickAction="play game") # dark winner menu play again button
menus[7].sprites[3].setClickAction(menus, 7, 0) # dark winner menu return to main menu button

while p.running: # main game loop
    clock.tick(p.FPS)

    pygame.display.update()

    for m in menus: # Loop through all menus
        m.mainLoop(WIN, pygame.mouse) # Run the sub-loop for each menu

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            p.running = False # exit the main loop if the quit event is found

pygame.quit()
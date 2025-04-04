import sys
import os

# add the different subfolders containing python files to the system path so that different classes can be imported
sys.path.insert(0, os.path.join(os.getcwd(), "src/menus"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/sprites"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/opponents"))

import parameters as p
from menu import Menu
from sprites.basicSprites import *
from sprites.gamePlaySprites import *

from opponents.easy import EasyOpponent
from opponents.medium import MediumOpponent

def createGamePlayMenu():
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

    # Board object
    board = Board() # board object to store Squares sprites

    # Dice Module
    diceList = [Button( # Roll Button
                (p.SCREEN_WIDTH*0.28, 0), # Centre of the rightmost 3/4 of the screen
                (p.SCREEN_WIDTH*0.1, p.SCREEN_HEIGHT*0.05), # Small button
                text=p.smallFont.render("Roll", True, p.WHITE), # Use a smaller font (25px)
                imagePath=p.buttonPath,
            )]
    for i in range(p.gameEngine.numDice): # For each dice
        diceList.append(
             Die( # Create a die object and add it to the list of sprites for the diceModule
                (i*max(p.SCREEN_HEIGHT*0.3, p.SCREEN_WIDTH*0.75 / p.gameEngine.numDice), p.SCREEN_HEIGHT*0.05), # x-coordinate is the minimum between a set minimum width, or the total horizontal space / number of dice
                (max(p.SCREEN_HEIGHT*0.1, p.SCREEN_WIDTH*0.325 / p.gameEngine.numDice), max(p.SCREEN_HEIGHT*0.1, p.SCREEN_WIDTH*0.325 / p.gameEngine.numDice)) # Dice are square
                # I will need to adjust these coordinates at a later date to fit the screen better
            )
        )
    diceModule = SpriteGroup(
        diceList, # diceList is the list of sprites for the diceModule
        (5*board.squareWidth, p.SCREEN_HEIGHT*0.4), # rightmost 3/4 of the width, roughly centre in terms of height
    )

    # Icons, Bars and Turn text
    lightIcon = MySprite( # Icon for the player using light tiles
        (4.5*board.squareWidth, p.SCREEN_HEIGHT*0.1), # To the left of the tiles pile
        (p.SCREEN_WIDTH*0.2, p.SCREEN_WIDTH*0.2), # Square shape and wide enough to fill the blank space
        imagePath=p.lightIconPath,
        highlightImagePath=p.lightIconHighlightPath
    )

    darkIcon = MySprite( # Icon for the player using dark tiles
        (p.SCREEN_WIDTH*0.82, p.SCREEN_HEIGHT*0.6), # To the right of the tiles pile
        (p.SCREEN_WIDTH*0.2, p.SCREEN_WIDTH*0.2), # Square shape and wide enough to fill the blank space
        imagePath=p.darkIconPath,
        highlightImagePath=p.darkIconHighlightPath
    )

    turnText = MySprite( # Text which clearly indicates whose turn it is currently
        (4.9*board.squareWidth, p.SCREEN_WIDTH*0.01), # Aligned with lightIcon, in the same header row as close and settings button
        (p.SCREEN_WIDTH*0.04, p.SCREEN_WIDTH*0.4), # Size is controlled by the font and so does not matter too much
        text = p.font.render("Light Player's Turn", True, p.WHITE) if p.gameEngine.curPlayer \
               else p.font.render("Dark Player's Turn", True, p.WHITE) # Set text dependent on the initial player from gameEngine
    )

    if p.gameEngine.curPlayer:
        lightIcon.switchHighlight() # Highlight the starting player according to gameEngine
    else:
        darkIcon.switchHighlight()

    lightBar = MySprite( # Bar for the player using light tiles
        (0, 0), 
        (p.SCREEN_WIDTH*0.02, board.squareWidth), # Same height as a square, quite narrow
        imagePath=p.barPath,
    )

    darkBar = MySprite( # Bar for the player using dark tiles
        (0, 0), 
        (p.SCREEN_WIDTH*0.02, board.squareWidth), # Same height as a square, quite narrow
        imagePath=p.barPath,
    )

    # Win buttons. Inaccessible to the player
    lightWinButton = Button(
        (0, 0), # coordinates and scale does not matter as they are designed to be invisible
        (0, 0)
    )

    darkWinButton = Button(
        (0, 0),
        (0, 0)
    )

    # Tiles

    if not p.singleplayerOpponent: # Multiplayer mode
        darkTiles = Tiles(board.squareWidth, False, board, lightIcon, darkIcon, diceModule, darkBar, None, darkWinButton, turnText, False) # Tiles object to store dark tiles
        lightTiles = Tiles(board.squareWidth, True, board, lightIcon, darkIcon, diceModule, lightBar, darkTiles, lightWinButton, turnText, False) # Tiles object to store light tiles
        darkTiles.enemyTiles = lightTiles # assign enemyTiles attribute
        
    elif p.singleplayerOpponent: # Singleplayer mode
        
        match p.singleplayerOpponent:
            case "easy":
                opponent = EasyOpponent() # set the temporary variable opponent to the correct function, imported from the python files in opponents folder
            case "medium":
                opponent = MediumOpponent()

        darkTiles = BotTiles(board.squareWidth, False, board, lightIcon, darkIcon, diceModule, darkBar, None, darkWinButton, turnText, opponent, True) # BotTiles object to store dark tiles
        lightTiles = Tiles(board.squareWidth, True, board, lightIcon, darkIcon, diceModule, lightBar, darkTiles, lightWinButton, turnText, False) # Tiles object to store light tiles
        darkTiles.enemyTiles = lightTiles # assign enemyTiles attribute
    
    # Menu instantiation

    if not p.singleplayerOpponent:
        return Menu(
            [settingsButton, closeButton, diceModule, board, lightTiles, darkTiles, lightIcon, darkIcon, lightBar, darkBar, lightWinButton, darkWinButton, turnText]
        )
    else:
        return Menu(
            [settingsButton, closeButton, diceModule, board, lightTiles, darkTiles, lightIcon, darkIcon, lightBar, darkBar, lightWinButton, darkWinButton, turnText],
            "game play menu singleplayer mode"
        )

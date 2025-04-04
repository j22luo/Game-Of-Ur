import pygame
import parameters as p
import random
import time
import json
import os
from gameEngine import GameEngine

# basic sprite class
class MySprite(pygame.sprite.Sprite):
    def __init__(self, coords, scale, imagePath=p.transparentPath, highlightImagePath=None, text=None):
        # Pass in image path, coordinates of the image, scale to transform the image to, path of the highlighted image if necessary and text if necessary
        pygame.sprite.Sprite.__init__(self)

        self.highlighted = False
        self.scale = scale
        self.imagePath = imagePath
        self.image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(self.image, self.scale) # scale the image if scaling dimensions are provided

        self.rect = self.image.get_rect() 
        self.rect.x = coords[0]
        self.rect.y = coords[1] # create the rect object based on the scaled image

        if text: # Create a separate rect object if text is part of the sprite
            self.textRect = self.image.get_rect()
            if imagePath != p.transparentPath:
                self.textRect.x = coords[0] + self.scale[0] * 0.1
                self.textRect.y = coords[1] + self.scale[1] * 0.1 # For each coordinate add a slight offset based on the height and width of sprite
            else:
                self.textRect.x = coords[0]
                self.textRect.y = coords[1]

        self.highlightImagePath = highlightImagePath

        self.text = text

    def switchHighlight(self): # switch the image variables if both image exists
        if self.imagePath and self.highlightImagePath:
            if not self.highlighted:
                self.image = pygame.image.load(self.highlightImagePath)
                self.image = pygame.transform.scale(self.image, self.scale) # scale the image if scaling dimensions are provided
            else:
                self.image = pygame.image.load(self.imagePath)
                self.image = pygame.transform.scale(self.image, self.scale) # scale the image if scaling dimensions are provided
            
            self.highlighted = not(self.highlighted)

        else:
            raise Exception("Image does not exist")

class Button(MySprite):
    def __init__(self, coords, scale, imagePath=p.transparentPath, highlightImagePath=None, text=None, soundPath=None, isActive=True):
        super().__init__(coords, scale, imagePath, highlightImagePath, text) # inherits attributes for displaying the button from the MySprite class
        self.isActive = isActive # Boolean indicating whether the button is currently active, to control whether it can be clicked
        self.isHovered = False # Boolean indicating whether the mouse is currently hovered over the button, False by default

        if soundPath:
            self.sound = pygame.mixer.Sound(soundPath) # Initialise the sound attribute if a sound path is provided
        else:
            self.sound = None

    def setClickAction(self, *args, clickAction="switch"): # Setter method for the clickAction
        match clickAction:
            case "switch":
                self.clickAction = lambda: self.menuSwitchClickAction(*args) # A function which is run when the button is clicked, to allow the button to trigger actions
            case "play game":
                self.clickAction = lambda: self.switchToGamePlayMenuClickAction(*args)
            case "quit":
                self.clickAction = lambda: self.quitClickAction() # Used to quit the game when the button is clicked.
            case "rolldice":
                self.clickAction = lambda: self.rollDiceClickAction(*args) # Used for the Roll button, when clicked it should change the images for the die sprites.
            case "win":
                self.clickAction = lambda: self.winbuttonClickAction(*args)
            case "select opponent close":
                self.clickAction = lambda: self.selectOpponentCloseButtonClickAction(*args)

    def quitClickAction(self):
        p.running = False

    def menuSwitchClickAction(self, menus, visibleMenu, invisibleMenu):
        menus[visibleMenu].isVisible = False # close the currently visible menu
        menus[invisibleMenu].isVisible = True # open the currently invisible menu

        if visibleMenu != 2: # If the menu that has just been opened isn't the settings menu.
                                # To avoid looping forever when menuSwitchClickAction is called.
            menus[2].sprites[0].setClickAction(menus, 2, visibleMenu) # Set the click action of the settings close button to 
                                                                        # redirect to the inputted visible menu

    def switchToGamePlayMenuClickAction(self, menus, visibleMenu, invisibleMenu, createGamePlayMenu):

        if visibleMenu == 0: p.singleplayerOpponent = None # Reset the singleplayer opponent if we are switching to multiplayer mode

        p.gameEngine = GameEngine( # Instantiate new gameEngine object
                 gameBoard=[4, # length of first bend
                            8, # length of middle section joining the bends
                            2, # length of second bend
                            0b00000000000001, # bitset representation of light tiles
                            0b00000000000001, # bitset representation of dark tiles
                            0b0100000100010000], # bitset representation of mosaic tiles
                 tilesPerPlayer=7, # Number of tiles per player
                 score=[[7, 0, 0], # Dark player: tiles yet to come on, tiles currently on, tiles that have come off
                        [7, 0, 0]], # Same data stored for the light player
                 curPlayer=True, # True is used for light and vice versa. Light starts.
                 diceDists=(p.TETRA_DIST, p.TETRA_DIST), # Tuple of probability distributions for both players. First dark, then light.
                 numDice=4) # Number of dice used

        menus[3] = createGamePlayMenu() # Add gamePlayMenu to the menus list.
        self.menuSwitchClickAction(menus, visibleMenu, invisibleMenu) # Switch menus

        menus[3].sprites[0].setClickAction(menus, 3, 2) # game play menu settings button
        menus[3].sprites[1].setClickAction(menus, 3, 0) # game play menu close button
        menus[3].sprites[2].sprites[0].setClickAction(menus[3].sprites[2], 
                                                      menus[3].sprites[3],
                                                      menus[3].sprites[4],
                                                      menus[3].sprites[5],
                                                      menus[3].sprites[6],
                                                      menus[3].sprites[7],
                                                      menus[3].sprites[12],
                                                      clickAction="rolldice") # game play menu roll dice button
        menus[3].sprites[10].setClickAction(menus, 3, 5, "Light", clickAction="win") # game play menu light win button
        menus[3].sprites[11].setClickAction(menus, 3, 7, "Dark", clickAction="win") # game play menu dark win button
        
    def rollDiceClickAction(self, diceModule, board, lightTiles, darkTiles, lightIcon, darkIcon, turnText):
        diceOutputs = p.gameEngine.rollDice() # Call the rollDice method which returns the list of outcomes for each dice
        for i, n in enumerate(diceOutputs): # Enumerate through the dice outcomes
            diceModule.sprites[i+1].setImage(n) # Set the image of the corresponding die sprite to its outcome. 
                                                # Offset by one since the roll Button is the 0th sprite in the sprites list
        self.isActive = False # Disable the button so that the clickAction is only called once

        moves = p.gameEngine.listMoves() # Get the list of legal moves

        if p.gameEngine.curPlayer: # if current player is light
            lightTiles.lastMoves = moves # assign the list of moves to lightTiles
        else:
            darkTiles.lastMoves = moves # otherwise assign list of moves to darkTiles

        if moves: # If there are more than one move
            if p.soundEnabled: pygame.mixer.Sound.play(p.diceSound) # play sound effect if enabled
            for move in moves: # Iterate through all moves
                if p.gameEngine.curPlayer:
                    lightTiles.assignMove(move)
                else:
                    darkTiles.assignMove(move)
        else: # No moves, so skip to the next player
            if p.soundEnabled: pygame.mixer.Sound.play(p.failSound) # play sound effect if enabled
            p.gameEngine.curPlayer = not (p.gameEngine.curPlayer) # "NOT" the current player
            lightIcon.switchHighlight() # Switch highlights for both players
            darkIcon.switchHighlight()
            turnText.text = p.font.render("Light Player's Turn", True, p.WHITE) if p.gameEngine.curPlayer \
                        else p.font.render("Dark Player's Turn", True, p.WHITE) # Set text dependent on the current player from gameEngine
            time.sleep(0.1)
            self.isActive = True # Activate the button again so that the next player can roll dice

            if lightTiles.isBotTiles and p.gameEngine.curPlayer: # Check if either tiles object belongs to a computer opponent and it has switched to their turn, and if so, play its turn
                lightTiles.playTurn()
            elif darkTiles.isBotTiles and not p.gameEngine.curPlayer:
                darkTiles.playTurn()

    def winbuttonClickAction(self, menus, visibleMenu, invisibleMenu, player): # Same arguments as switchMenu, but player is either "Light" or "Dark"
        self.menuSwitchClickAction(menus, visibleMenu, invisibleMenu) # Switch menus
        menus[invisibleMenu].sprites[1].text = p.font.render(f"{player} player won in {p.gameEngine.totalTurns} moves!", True, p.WHITE)  # Set congratulations text to include the number of turns

    def selectOpponentCloseButtonClickAction(self, menus, visibleMenu, invisibleMenu):
        self.menuSwitchClickAction(menus, visibleMenu, invisibleMenu)
        p.singleplayerOpponent = None # reset the singleplayerOpponent variable when exiting the menu

    def handleClick(self, mouse):
        # Method to detect whether the mouse is clicking the button in the current frame, need to be run within a game loop
        # mouse is a pygame.mouse object which allows us to get the position of the mouse and whether left click is currently held down

        if self.isHovered and self.isActive and mouse.get_pressed()[0]: # If the mouse is hovered over the button, the button is active and it is pressed
            self.clickAction() # Call click action
            self.isHovered = False # set isHovered to False so that, when we return to a menu, this button is not immediately called
        if self.isActive and self.rect.collidepoint(mouse.get_pos()) and not mouse.get_pressed()[0]: # If the mouse collides with the button and is not clicked, i.e. the mouse is hovering over the button
            self.isHovered = True # Set isHovered to True
        if not self.rect.collidepoint(mouse.get_pos()): # Otherwise, if the mouse is not hovering over the button
            self.isHovered = False # Explicitly set isHovered to False

class Die(MySprite):
    def __init__(self, coords, scale, imagePath=p.tetrahedronImagePaths[0][0], highlightImagePath=None, text=None, imagePaths=p.tetrahedronImagePaths):
        super().__init__(coords, scale, imagePath, highlightImagePath, text) # inherits attributes for displaying the die from the MySprite class
        self.imagePaths = imagePaths

    def setImage(self, n):
        self.image = pygame.image.load(random.choice(self.imagePaths[n])) # n is the number that the dice should land on, and we randomly choose one of the images which corresponds to this number
        self.image = pygame.transform.scale(self.image, self.scale) # scale the image


class Toggle(Button):
    def __init__(self, coords, scale, offImagePath=p.transparentPath, onImagePath=None, highlightImagePath=None, text=None, soundPath=None, isActive=True):
        super().__init__(coords, scale, offImagePath, highlightImagePath, text, soundPath, isActive) # Provide arguments to initialise the parent Button class
        self.offImage = self.image # Label self.image as the off image to allow for easier referencing later
        self.onImage = pygame.transform.scale(pygame.image.load(onImagePath), self.scale) # Store the onImage as an attribute using path and scale provided 
        self.curState = False # Attribute to store the current state, toggle is switched off when initialised

    def setClickAction(self, *args, clickAction="select opponent"): # Overridden setClickAction method
        match clickAction:
            case "select opponent":
                self.onAction = lambda: self.selectOpponentOnAction(*args) # Only difference is that both matching onAction and offActions are set 
                self.offAction = lambda: self.selectOpponentOffAction(*args) # as opposed to just one clickAction
            case "sound":
                self.onAction = lambda: self.soundOnAction(*args)
                self.offAction = lambda: self.soundOffAction(*args)
            case "theme":
                self.onAction = lambda: self.themeOnAction(*args)
                self.offAction = lambda: self.themeOffAction(*args)
            case "startup":
                self.onAction = lambda: self.startupOnAction(*args)
                self.offAction = lambda: self.startupOffAction(*args)

    def selectOpponentOnAction(self, selectOpponentButtons, selfIndex, playButton):
        for i, button in enumerate(selectOpponentButtons): # Iterate through the list of button objects provided
            if i != selfIndex and button.curState: # If a button is not this button, and is currently switched on
                button.offAction() # Call its offAction to switch it off
                
        self.image = self.onImage # Set image 
        playButton.isActive = True # activate the play button
        
        if selfIndex == 0: # Check selfIndex to change the singleplayerOpponent variable accordingly
            p.singleplayerOpponent = "easy"
        elif selfIndex == 1:
            p.singleplayerOpponent = "medium"
            
    def selectOpponentOffAction(self, selectOpponentButtons, selfIndex, playButton): # Action performed when a select opponent button is switched off
        self.image = self.offImage # Set the image to be rendered to the offImage
        p.singleplayerOpponent = None # Set the variable storing the singleplayer opponent selected in parameters.py to None
        playButton.isActive = False # de-activate the play button so that the player cannot play this mode until they've chosen an opponent

    def soundOnAction(self):
        self.image = self.onImage # Set image
        p.soundEnabled = True # Set boolean in parameters.py to True

        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "r") as f: # modify settings.json to store the user's preference
            content = json.loads(f.read())
            content["sound"] = p.soundEnabled
        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "w") as f:
            f.write(json.dumps(content))

    def soundOffAction(self):
        self.image = self.offImage # Set image
        p.soundEnabled = False # Set boolean in parameters.py to False

        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "r") as f: # modify settings.json to store the user's preference
            content = json.loads(f.read())
            content["sound"] = p.soundEnabled
        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "w") as f:
            f.write(json.dumps(content))

    def themeOnAction(self):
        self.image = self.onImage # Set image
        p.historical = True # Set boolean in parameters.py to True

        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "r") as f: # modify settings.json to store the user's preference
            content = json.loads(f.read())
            content["historical"] = p.historical
        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "w") as f:
            f.write(json.dumps(content))

    def themeOffAction(self):
        self.image = self.offImage # Set image
        p.historical = False # Set boolean in parameters.py to False

        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "r") as f: # modify settings.json to store the user's preference
            content = json.loads(f.read())
            content["historical"] = p.historical
        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "w") as f:
            f.write(json.dumps(content))

    def startupOnAction(self):
        self.image = self.onImage # Set image
        info = pygame.display.Info()
        p.SCREEN_WIDTH, p.SCREEN_HEIGHT = info.current_w, info.current_h # Set the width and height to the size of current monitor
                                                                         # Using attributes of info

        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "r") as f: # modify settings.json to store the user's preference
            content = json.loads(f.read())
            content["fullscreen"] = True
        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "w") as f:
            f.write(json.dumps(content))

    def startupOffAction(self):
        self.image = self.offImage # Set image
        p.SCREEN_WIDTH, p.SCREEN_HEIGHT = p.DEFAULT_WIDTH, p.DEFAULT_HEIGHT # Set the width and height to default values
                                                                            # Stored in parameters.py
        
        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "r") as f: # modify settings.json to store the user's preference
            content = json.loads(f.read())
            content["fullscreen"] = False
        with open(os.path.join(os.getcwd(), "src/menus/settings.json"), "w") as f:
            f.write(json.dumps(content))

    def handleClick(self, mouse): # Overridden handleClick method

        # Very similar except an additional if-statement is added to the case where a click is registered, to call the correct Action method based on curState

        if self.isHovered and self.isActive and mouse.get_pressed()[0]: # If the mouse is hovered over the button, the button is active and it is pressed
            if self.curState: # if the toggle is currently switched on, by clicking we switch it off
                self.offAction() # perform the off action
            elif not self.curState:
                self.onAction() # otherwise, perform the on action
            self.curState = not self.curState # switch the current state
            self.isHovered = False # set isHovered to False so that, when we return to a menu, this button is not immediately called
        if self.isActive and self.rect.collidepoint(mouse.get_pos()) and not mouse.get_pressed()[0]: # If the mouse collides with the button and is not clicked, i.e. the mouse is hovering over the button
            self.isHovered = True # Set isHovered to True
        if not self.rect.collidepoint(mouse.get_pos()): # Otherwise, if the mouse is not hovering over the button
            self.isHovered = False # Explicitly set isHovered to False
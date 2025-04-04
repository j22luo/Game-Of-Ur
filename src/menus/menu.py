from sprites.basicSprites import *
from sprites.gamePlaySprites import *
import parameters as p   

# basic menu
class Menu():
    def __init__(self, sprites, additionalAction=None, isVisible=False, name=None):
        self.sprites = sprites # list of MySprite objects
        self.isVisible = isVisible
        self.additionalAction = additionalAction # Optional string used to identify the menu and therefore menuAction required

        match self.additionalAction:
            case "game play menu singleplayer mode":
                self.menuAction = lambda: self.gamePlayMenuAction() # Set the menu action for the game play menu
    
    def draw(self, window, mouse):
        if self.isVisible: # if the Menu is currently shown
            window.fill(p.BACKGROUND_PEACH) # Draw the background colour to cover up previous sprites
            for sprite in self.sprites:
                if type(sprite) in (SpriteGroup, Board, Tiles, BotTiles): sprite.draw(window, mouse) # Call SpriteGroup's draw() method if the sprite is a group
                else:
                    window.blit(sprite.image, sprite.rect) # blit each object onto the surface 
                    if sprite.text: window.blit(sprite.text, sprite.textRect) # blit the text if it exists
                    if type(sprite) in (Button, Tile, Toggle): # if sprite is a button or tile or toggle
                        sprite.handleClick(mouse) # Handle click event if the sprite is a Button or tile

    def gamePlayMenuAction(self):
        botTiles = self.sprites[5] # Set a temporary variable to refer to the botTiles spriteGroup
    
        if self.isVisible:
            botTiles.frameCount += 1 # Increment the frame counter

        if botTiles.frameCount == 60:
            botTiles.clickDice() # call clickDice if it's been 60 frames since the human chose a tile
        elif botTiles.frameCount == 120:
            botTiles.moveTile() # call moveTile if it's been 60 frames since the bot clicked the dice

    def mainLoop(self, window, mouse):
        self.draw(window, mouse) # draw all sprites
        if self.additionalAction:
            self.menuAction() # if there are additional actions to be performed, call the assigned menuAction method



            

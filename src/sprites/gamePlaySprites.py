import parameters as p
import pygame
import time
from basicSprites import *

class SpriteGroup():
    def __init__(self, sprites, coords):
        self.sprites = sprites # Store the list of associated sprites
        self.x = coords[0]
        self.y = coords[1] # coordinates of the entire sprite group

        for sprite in self.sprites: # for each sprite in the group of sprites
            sprite.rect.x += self.x
            sprite.rect.y += self.y # adjust their rect by the coords so that their coordinates are defined in terms of the entire group

            if sprite.text: # Also adjust textRect coordinates if the sprite contains text
                sprite.textRect.x += self.x
                sprite.textRect.y += self.y

    def addSprite(self, sprite, index):
        sprite.rect.x += self.x # add offset according to the inputted x and y offset
        sprite.rect.y += self.y

        self.sprites.insert(index, sprite) # insert the sprite into the sprites list at the given index

    def popSprite(self, index):
        sprite = self.sprites.pop(index) # remove the sprite at the given index
        sprite.rect.x -= self.x # remove the offset according to the inputted x and y offset
        sprite.rect.y -= self.y
        return sprite # return the removed sprite

    def draw(self, window, mouse):
        for sprite in self.sprites:
            if type(sprite) in (SpriteGroup, Board, Tiles, BotTiles): sprite.draw(window, mouse) # Call SpriteGroup's draw() method if the sprite is a group
            else:
                window.blit(sprite.image, sprite.rect) # blit each object onto the surface 
                if sprite.text: window.blit(sprite.text, sprite.textRect) # blit the text if it exists
                if type(sprite) in (Button, Tile, Toggle): # if sprite is a button or tile or toggle
                    sprite.handleClick(mouse) # Handle click event if the sprite is a Button or tile

class Square(MySprite):
    def __init__(self, 
                coords, # Coordinates of the top left corner of the square
                width,  # Width of the square in pixels
                squareType): # Type of square. True for mosaic, False for normal. Matches with the bit representation of mosaics in GameEngine
        if squareType:
            super().__init__(
                coords, 
                (width, width), 
                imagePath=p.mosaicPath, # Initialise with mosaic assets if the square is a mosaic
                highlightImagePath=p.mosaicHighlightPath)
        else:
            super().__init__(
                coords, 
                (width, width), 
                imagePath=p.squarePath, # Otherwise initialise with square assets
                highlightImagePath=p.squareHighlightPath)

class Board(SpriteGroup): # Inherits from SpriteGroup to use the draw() method
    def __init__(self, coords=(p.SCREEN_HEIGHT*0.1, 0)): # Takes gameEngine and coordinates of the overall board as input
        self.coords = coords
        self.startLen, self.middleLen, self.endLen = p.gameEngine.gameBoard[0], p.gameEngine.gameBoard[1], p.gameEngine.gameBoard[2]
        mosaic = p.gameEngine.gameBoard[5] # Assign commonly used values in gameBoard to variables to shorten code

        self.squareWidth = (p.SCREEN_HEIGHT) // self.middleLen # Width of each square is 90% the height of the screen, divided by the number of squares in a column
        
        corridor, edge = [], [] # Temporary arrays to store the type of squares in the central vs edge column
        for i in range(self.startLen, 0, -1):
            edge.append(p.gameEngine.getBitAtPosition(mosaic, i)) # Add the square types of the first bend to the edge column
        
        for _ in range(self.middleLen - (self.startLen + self.endLen)): # Use -1 as a placeholder to show that no squares should be drawn at that point in the grid
            edge.append(-1)

        for i in range(p.gameEngine.boardLen - 2, p.gameEngine.boardLen - self.endLen - 2, -1): # Add the square types of the final bend to the edge column
            edge.append(p.gameEngine.getBitAtPosition(mosaic, i))

        for i in range(self.startLen+1, self.startLen + self.middleLen + 1): # Add the square types of the central column
            corridor.append(p.gameEngine.getBitAtPosition(mosaic, i))
        
        sprites = [] # 2D array to store the squares in the same positions as they appear to the player. Each item in sprites is a SpriteGroup object which then stores a row of squares.
        # Allows me to reuse the draw() method from SpriteGroup without modifying it, reducing redundant code.
        for i in range(self.middleLen):
            if edge[i] >= 0: # If there is a square on the edge for this row
                sprites.append(SpriteGroup([
                    Square((0, 0), self.squareWidth, edge[i]), # Add the edge square, then corridor, then edge. Coords are relative to the top left corner of that row to initialise SpriteGroup
                    Square((self.squareWidth, 0), self.squareWidth, corridor[i]),
                    Square((2*self.squareWidth, 0), self.squareWidth, edge[i])
                ], (self.coords[0], self.coords[1] + i*self.squareWidth)))
            else:
                sprites.append(SpriteGroup([ # Otherwise, just add the square in the central corridor
                    MySprite((0,0), (0,0)),
                    Square((self.squareWidth, 0), self.squareWidth, corridor[i])
                ], (self.coords[0], self.coords[1] + i*self.squareWidth)))

        self.sprites = sprites # Store sprites as an attribute so that it is correctly processed by the menu draw() method.
    
    def findSquare(self, move, player):
        if player: # If the player is light
            if move[1] <= self.startLen: # If the tile will land in the first bend
                return self.sprites[self.startLen - move[1]].sprites[0] # Select square as the first column, and startLen - move[1]
            elif move[1] <= self.startLen + self.middleLen: # If the tile will land in the corridor
                return self.sprites[move[1] - self.startLen - 1].sprites[1] # Select square as second column, 
                                                                            # subtract off startLen then minus one to account for zero indexing
            elif move[1] <= self.startLen + self.middleLen + self.endLen: # If the tile will land in the final bend
                return self.sprites[-(move[1] - self.middleLen - self.startLen)].sprites[0] # Select square as first column
                                                                                              # Subtract off startLen and middleLen, 
                                                                                              # then negative indexing as the bend is backwards
                
        else: # Repeat for dark player, except selecting the 3rd column instead of 1st in all cases
            if move[1] <= self.startLen:
                return self.sprites[self.startLen - move[1]].sprites[2]
            elif move[1] <= self.startLen + self.middleLen:
                return self.sprites[move[1] - self.startLen - 1].sprites[1]
            elif move[1] <= self.startLen + self.middleLen + self.endLen:
                return self.sprites[-(move[1] - self.middleLen - self.startLen)].sprites[2]

        return None # This stage is only reached if the move gets the tile off the board
                    # In which case, no squares can be highlighted

class Tile(Button):
    def __init__(self, coords, scale, player, board):
        self.player = player # Boolean showing the player that the tile belongs to, in the same way as in Game Engine
        if self.player:
            imagePath = p.lightTilePath # Assign image paths for the light tile if the player is light
            highlightImagePath = p.lightTileHighlightPath
        else:
            imagePath = p.darkTilePath # Otherwise assign image paths for dark tile
            highlightImagePath = p.darkTileHighlightPath

        self.lastMove = None # Used to store the latest move, which can be used to identify where the tile is and where it should move to.
                             # Initially set to None
        self.nextMove = None # Used to store the next move that the tile could make, if it was selected by the player
        # These are all the unique attributes, now we can assign attributes for the parent Button class.
        # Tiles is initially disabled and is activated by the Tiles object. Also assigned a sliding sound
        super().__init__(coords, scale, imagePath, highlightImagePath, soundPath=p.tileSoundPath, isActive=False)
        self.board = board

    def onHover(self):
        square = self.board.findSquare(self.nextMove, self.player)
        if square: square.switchHighlight() # If the tile moves onto a square, highlight it
        # self.isHovered = not self.isHovered

    def setClickAction(self, tiles, lightIcon, darkIcon, rollButton, turnText, enemyTiles):
        self.clickAction = lambda: self.tileClickAction(tiles, lightIcon, darkIcon, rollButton, turnText, enemyTiles) 
        # Set the clickAction method to a lambda function which calls the tileClickAction with these parameters, as they never change
        # This is also more consistent with how every other button object works

    def tileClickAction(self, tiles, lightIcon, darkIcon, rollButton, turnText, enemyTiles):
        self.lastMove = self.nextMove # As this method moves the tile, the tile's latest move is the same as its next move, previously.

        square = self.board.findSquare(self.lastMove, self.player)
        p.gameEngine.makeMove(self.lastMove) # Update gameBoard

        if square:
            self.rect.x, self.rect.y = square.rect.x, square.rect.y # Move tile to the square it lands on, if the tile is not moving off the board
            square.switchHighlight() # Unhighlight the square as the tile has now moved

        self.switchHighlight() # Unhighlight the tile as it has now moved
        self.isActive = False # Disable the tile
        
        if self.player != p.gameEngine.curPlayer:
            lightIcon.switchHighlight()
            darkIcon.switchHighlight() # Correctly highlight the icons to indicate whose turn is next

        if not (p.singleplayerOpponent and p.gameEngine.curPlayer != self.player):
            rollButton.isActive = True # Reactivate the roll button but only in multiplayer

        tiles.adjust(self.lastMove) # Update tiles.sprites and the bar so that they are rendered in the correct location on screen

        self.isHovered = False # unhover the tile

        if p.soundEnabled: pygame.mixer.Sound.play(p.tileSound) # play sound effect if enabled

        turnText.text = p.font.render("Light Player's Turn", True, p.WHITE) if p.gameEngine.curPlayer \
                        else p.font.render("Dark Player's Turn", True, p.WHITE) # Set text dependant on the initial player from gameEngine

        if p.singleplayerOpponent and p.gameEngine.curPlayer != self.player: # If the enemy player is a bot and it is no longer the human player's turn
            enemyTiles.playTurn() # Let the computer opponent play its turn

    def handleClick(self, mouse):
        # Method to detect whether the mouse is clicking the button in the current frame, needD to be run within a game loop
        # mouse is a pygame.mouse object which allows us to get the position of the mouse and whether left click is currently held down

        if self.isActive: # Methods can only be called with the tile is currently active
            if self.isHovered and mouse.get_pressed()[0]: # If the tile is hovered over and the left click is pressed
                self.clickAction() # Call click action
            elif self.rect.collidepoint(mouse.get_pos()) and not mouse.get_pressed()[0]: # Otherwise, if the mouse is over the button but not pressed
                if not self.isHovered: # If the mouse just moved onto the button within this frame
                    self.onHover() # Call the onHover method to highlight the relevant square
                self.isHovered = True # Always set isHovered to True
            elif not self.rect.collidepoint(mouse.get_pos()) and not mouse.get_pressed()[0]: # If the mouse is currently not over the button and not pressed
                if self.isHovered: # If the mouse just moved off the button
                    self.onHover() # Call onHover again to unhighlight the relevant square
                self.isHovered = False # Always set isHovered to False

class BotTile(Tile):
    def __init__(self, coords, scale, player, board):
        super().__init__(coords, scale, player, board)

    def tileClickAction(self, tiles, lightIcon, darkIcon, rollButton, turnText, enemyTiles):
        self.lastMove = self.nextMove # As this method moves the tile, the tile's latest move is the same as its next move, previously.

        square = self.board.findSquare(self.lastMove, self.player)
        p.gameEngine.makeMove(self.lastMove) # Update gameBoard

        if square:
            self.rect.x, self.rect.y = square.rect.x, square.rect.y # Move tile to the square it lands on, if the tile is not moving off the board

        self.switchHighlight() # Unhighlight the tile as it has now moved
        self.isActive = False # Disable the tile
        
        if self.player != p.gameEngine.curPlayer:
            lightIcon.switchHighlight()
            darkIcon.switchHighlight() # Correctly highlight the icons to indicate whose turn is next

        if self.player != p.gameEngine.curPlayer:
            rollButton.isActive = True # Reactivate the roll button

        tiles.adjust(self.lastMove) # Update tiles.sprites and the bar so that they are rendered in the correct location on screen

        self.isHovered = False # unhover the tile

        if p.soundEnabled: pygame.mixer.Sound.play(p.tileSound) # play sound effect if enabled

        turnText.text = p.font.render("Light Player's Turn", True, p.WHITE) if p.gameEngine.curPlayer \
                        else p.font.render("Dark Player's Turn", True, p.WHITE) # Set text dependant on the initial player from gameEngine

        if p.gameEngine.curPlayer == self.player: # If the curPlayer still matches self.player, i.e. the tile landed on a mosaic tile
            tiles.playTurn() # Play the turn again

class Tiles(SpriteGroup):
    def __init__(self, squareWidth, player, board, lightIcon, darkIcon, diceModule, bar, enemyTiles, winButton, turnText, isBotTiles=False):
        self.squareWidth = squareWidth # Width of a square, used to scale the tiles properly, comes from Board object
        self.tileOffset = self.squareWidth * 0.15
        self.player = player # Boolean representing player
        self.playerScore = p.gameEngine.score[player] # Used to easily reference the score data structure
        self.board = board # Board object storing the coordinates of Squares
        self.lastMoves = None
        self.enemyTiles = enemyTiles
        self.winButton = winButton
        self.diceModule = diceModule
        self.isBotTiles = isBotTiles

        self.bar = bar # Bar sprite associated with the pile of tiles

        if self.player: # light
            self.coords = (p.SCREEN_WIDTH*0.5, p.SCREEN_HEIGHT*0.2) # Top right 2/3 of the screen, 
        else: # Dark
            self.coords = (5*self.squareWidth, p.SCREEN_HEIGHT*0.7) # Bottom right, scattered when compared to the Light pile
        
        self.sprites = [SpriteGroup([], self.coords), SpriteGroup([], self.coords), SpriteGroup([], self.coords)]
        # Data structure used to store three "piles" of tile objects.
        # sprites[0]: Tiles yet to come onto the board, useful to have coordinates relative to the overall pile
        # sprites[1]: Tiles currently on the board. Tiles will get their coordinates from the Board so coordinates do not need to be relative
        # sprites[2]: Tiles that have completed the course, useful to have coordinates relative to the overall pile

        for i in range(self.playerScore[0]): # Initially add to sprites[0] according to score

            if self.isBotTiles:
                tile = BotTile((self.squareWidth*i - self.tileOffset, self.tileOffset), # Same parameters except we use the BotTile class
                            (self.squareWidth, self.squareWidth), 
                            self.player, self.board) 
            else:
                tile = Tile((self.squareWidth*i - self.tileOffset, self.tileOffset),
                            # Offset horizontally using tileOffset and the squareWidth multiplied by the index, offset vertically by only the tileOffset
                            (self.squareWidth, self.squareWidth), # Scale the tiles so that they are the same dimensions as the squares
                            self.player, self.board) # Give the Tile object its player boolean and board object

            tile.setClickAction(self, lightIcon, darkIcon, self.diceModule.sprites[0], turnText, self.enemyTiles) # Set the clickAction of the tile
            self.sprites[0].addSprite(tile, i) # Add to the sprites list of the SpriteGroup.

        self.adjustBar() # Set the coordinates of the bar sprite to be just behind the pile of tiles.
    
    def adjustBar(self):
        if self.sprites[0].sprites:
            self.bar.rect.x, self.bar.rect.y = (self.sprites[0].sprites[-1].rect.x + self.squareWidth, self.sprites[0].sprites[-1].rect.y + self.tileOffset)
            # Coordinates of the bar is always directly behind the last tile that is yet to come onto the board
        else:
            self.bar.rect.x, self.bar.rect.y = (self.coords[0] - self.tileOffset, self.coords[1] + self.tileOffset)
            # Same positioning as where the first tile in the pile should be, adjusted to self.coords because bar is not part of a spriteGroup

    def assignMove(self, move):
        if move[0] == 0: # If the tile we want is not on the board yet
            self.sprites[0].sprites[-1].nextMove = move # Assign the move to the last / rightmost tile in the pile
            self.sprites[0].sprites[-1].switchHighlight() # Highlight tile
            self.sprites[0].sprites[-1].isActive = True # Activate the tile so that it can be clicked
        else:
            for tile in self.sprites[1].sprites: # Otherwise, iterate through the tiles on the board
                if tile.lastMove[1] == move[0]: # Any tile on the board will have a previous move. If they previously moved to the start of this move, then they are the tile we want
                    tile.nextMove = move  # Assign the move
                    tile.switchHighlight() # Highlight tile
                    tile.isActive = True # Activate the tile
                    break

    def adjust(self, move):
        # Check if the game has ended
        if p.gameEngine.score[self.player][-1] == p.gameEngine.tilesPerPlayer: # If all the tiles have finished the course, i.e. the current player wins
            if p.soundEnabled: pygame.mixer.Sound.play(p.winSound) # play sound effect if enabled
            self.winButton.clickAction() # Call the clickAction of the winButton
            return None # return to exit the method

        # Adjust tiles

        if move[2]: self.enemyTiles.adjust((move[1], 0, False)) # If the move is a capture, also call adjust for enemy tiles to move the captured tile back

        if move[1] == 0: # If the tile has been captured
            for i in range(len(self.sprites[1].sprites)):
                if self.sprites[1].sprites[i].lastMove[1] == move[0]: # Iterate through list of tiles on the board, until the tile with a matching previous destination square is found
                    tile = self.sprites[1].popSprite(i) # pop the selected tile from sprites[1]

                    if self.sprites[0].sprites:
                        lastTile = self.sprites[0].sprites[-1] # temporary variable used to refer to the rightmost tile in sprites[0]
                        self.sprites[0].addSprite(tile, len(self.sprites[0].sprites)) # Add the selected tile to sprites[0]
                        tile.rect.x, tile.rect.y = lastTile.rect.x + self.squareWidth, lastTile.rect.y # Change coordinates of selected tile so that it is to the right of lastTile
                    else:
                        self.sprites[0].addSprite(tile, len(self.sprites[0].sprites)) # Add the selected tile to sprites[0]
                        tile.rect.x, tile.rect.y = (self.coords[0] - self.tileOffset, self.coords[1] + self.tileOffset)
                    break
            for tile in self.sprites[2].sprites: # Iterate through all tiles in sprites[2]
                tile.rect.x += self.squareWidth # Shuffle them right by one tile 
        else:
            for m in self.lastMoves: # Deactivate the tiles that were not chosen
                if move != m: # Iterate through list of moves. If we encounter a move that we are not going to make
                    if m[0] == 0: # If this was to move a tile onto the board
                        self.sprites[0].sprites[-1].switchHighlight() # Selected tile is rightmost of sprite[0]
                        self.sprites[0].sprites[-1].isActive = False # Unhighlight and deactivate
                    else:
                        for i in range(len(self.sprites[1].sprites)): # Iterate through sprites[1] to find the tile
                            if self.sprites[1].sprites[i].nextMove == m:
                                self.sprites[1].sprites[i].switchHighlight() # When the tile is found,
                                self.sprites[1].sprites[i].isActive = False # unhighlight and deactivate
                                break

            if move[0] == 0: # If a tile is being moved onto the board
                tile = self.sprites[0].popSprite(-1) # Remove the last tile from sprites[0] as we always pop from the rear
                self.sprites[1].addSprite(tile, 0) # Add this to sprites[1] to indicate it is now on the board. 
                                                # The order within sprites[1] doesn't really matter
                for tile in self.sprites[2].sprites: # For each sprite that has made it off the board
                    tile.rect.x -= self.squareWidth # Shuffle to the left by one space to fill up the blank space
            elif move[1] == p.gameEngine.boardLen - 1: # Otherwise, if the tile has finished 
                for i in range(len(self.sprites[1].sprites)): # Iterate through sprites[1] to find the tile
                    if self.sprites[1].sprites[i].lastMove == move:
                        tile = self.sprites[1].popSprite(i) # When it is found, remove the tile from sprites[1]

                        if self.sprites[0].sprites:
                            lastTile = self.sprites[0].sprites[-1] # temporary variable used to refer to the rightmost tile in sprites[0]
                            self.sprites[2].addSprite(tile, 0) # Add the tile to sprites[2]
                            tile.rect.x, tile.rect.y = lastTile.rect.x, lastTile.rect.y # Change coordinates of selected tile so that it is to the right of lastTile
                        else:
                            self.sprites[2].addSprite(tile, 0) # Add the tile to sprites[2]
                            tile.rect.x, tile.rect.y = (self.coords[0] - self.tileOffset - self.squareWidth, self.coords[1] + self.tileOffset) # Change coordinates so that it is one tile left of the bar, taking into account the fact that it will be shuffled right by one tile
                        break
                for tile in self.sprites[2].sprites:
                    tile.rect.x += self.squareWidth # Shuffle all tiles in sprites[2] right by one tile's space.
                                                    # This is why I set the coordinates to be the same as the rightmost tile earlier
            
        self.adjustBar() # Adjust the bar's coordinates

class BotTiles(Tiles):
    def __init__(self, squareWidth, player, board, lightIcon, darkIcon, diceModule, bar, enemyTiles, winButton, turnText, opponent, isBotTiles):
        super().__init__(squareWidth, player, board, lightIcon, darkIcon, diceModule, bar, enemyTiles, winButton, turnText, isBotTiles) # initialise attributes for Tiles class
        self.opponent = opponent # Stores the opponent object used to determine the next move
        self.frameCount = 1000 # Counts the number of frames since the bot's turn started. 
                               # Initialise as an arbitrarily high value so that the bot does not immediately play a turn

    def playTurn(self):
        self.frameCount = 0 # Reset the frameCount attribute to begin a turn
    
    def clickDice(self):
        self.diceModule.sprites[0].clickAction() # Call the clickAction of the rollButton, i.e. simulates clicking the rollButton

    def moveTile(self):
        if self.player == p.gameEngine.curPlayer: # If the current player is still this player
                                                  # This is needed because rolling the dice could result in no legal moves, in which case the turn is skipped
            move = self.opponent.algorithm(self.lastMoves) # Use the opponent object to decide the next legal move to make

            # Find the tile with the corresponding tile.lastMove attribute
            if move[0] == 0:
                self.sprites[0].sprites[-1].clickAction() # If the move is to move a tile onto the board, "click" the rightmost tile in the pile
            else:
                for tile in self.sprites[1].sprites: # Otherwise, iterate through tiles on the board to find a tile with the corresponding lastMove
                    if tile.lastMove[1] == move[0]:
                        tile.clickAction() # Once it is found, "click" the tile.
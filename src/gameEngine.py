import parameters as p
import random

class GameEngine():
    def __init__(self, 
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
                 numDice=4): # Number of dice used
        self.gameBoard = gameBoard
        self.tilesPerPlayer = tilesPerPlayer
        self.score = score
        self.curPlayer = curPlayer
        self.diceDists = diceDists
        self.numDice = numDice
        self.boardLen = sum(gameBoard[0:3]) + 2 # length of the board for one player, +2 to account for start and end
        self.selfIndex = 3 if self.curPlayer else 4
        self.enemyIndex = 4 if self.curPlayer else 3
        self.latestRoll = None
        self.totalTurns = 0
        
    def printGameBoard(self): # temporary debugging function to print useful information in a readable format
        print("Game board:")
        print(bin(self.gameBoard[3]))
        print(bin(self.gameBoard[4]))
        print(bin(self.gameBoard[5]))

        print("Score:")
        print(self.score[0])
        print(self.score[1])

        print(f"Player to move next is {'Light' if self.curPlayer else 'Dark'}")


    def rollDice(self):
        diceOutputs = [] # Total initially has no numbers
        for _ in range(self.numDice): # Simulate a single die numDice times
            randomFloat = random.random() # Generate a random flaot 0-1 using the random library
            for key, value in self.diceDists[self.curPlayer].items(): # For each variable and cumulative probability value in the distribution
                if randomFloat >= value[0] and randomFloat < value[1]: # If the random float falls within the interval for that value
                    diceOutputs.append(key) # Add the variable value to the list of outputs and stop searching
                    break
        self.latestRoll = sum(diceOutputs) # Store the total number of squares that can be made 
        return diceOutputs

    def updateIndex(self): # set the index of the current player, and vice versa for the enemy player, to access the correct bitset in gameBoard
        if self.curPlayer: self.selfIndex, self.enemyIndex = 3, 4 
        else: self.selfIndex, self.enemyIndex = 4, 3

    def getBitAtPosition(self, bits, index): # helper function to retrieve the bit (True or False) at a specific index of a bitset, starting from the right
        return bool((bits >> index) & 1) # shift right by index so that the bit we want to get is the rightmost, then "and" with 1. This means either all bits are 0 or the rightmost bit is 1.

    def listMoves(self): 
        moves = [] # List of all possible moves, which will be returned
        if self.latestRoll == 0: return moves # if the latest roll is 0, there are no valid moves
        self.updateIndex() # call updateIndex to correctly access the bitset for the current player and the enemy player

         # A mask where the bits representing the central corridor are set, and the other bits are not set.
         # Do this by setting gameBoard[1] many bits in a row then shifting left by the length of the lower bend.
        corridorMask = (2**(self.gameBoard[1]) - 1) << (self.gameBoard[0] + 1)

        # Set representing all squares containing an enemy tile that cannot be captured. 
        # For a square to contain a safe enemy tile, it must be a mosaic AND be in the central corridor AND contain an enemy tile
        safeEnemyTiles = self.gameBoard[5] \
                        & self.gameBoard[self.enemyIndex] \
                        & corridorMask

        # Set representing all squares that we can move our tiles onto
        # For a square to be free it must not already contain one of our tiles AND be latestRoll squares ahead of one of our tiles AND not contain a safe enemy tile.
        freeSquares = ~self.gameBoard[self.selfIndex] \
                    & (self.gameBoard[self.selfIndex] << self.latestRoll) \
                    & ~safeEnemyTiles
        
        # Set representing all squares such that, if we move our tiles onto it, an enemy tile would be captured
        # For a square to be a capture square, it must be a free square that we can move onto AND contain an enemy tile 
        # AND the square must be within the corridor, which is the only place where captures can take place.
        captures = freeSquares \
                    & self.gameBoard[self.enemyIndex] \
                    & corridorMask

        for i in range(self.boardLen): # For each square in the board
            if self.getBitAtPosition(freeSquares, i): # If the square is free
                if self.getBitAtPosition(captures, i): # If the square is also a capture square, then we set the third element in the move tuple as True
                    moves.append((i - self.latestRoll, i, True))
                else:
                    moves.append((i - self.latestRoll, i, False)) # Otherwise we set the third element in the move tuple as False

        return moves

    def makeMove(self, move): # move is one of the three-tuples contained by the list returned by listMoves()
        self.updateIndex() # First, update indices so that we refer to the correct bitsets

        self.gameBoard[self.selfIndex] ^= (2**move[0] + 2**move[1]) # XOR the current player's bitset with a mask where the bits at move[0] and move[1] is set
        # The player's bitset should have had "0" at the new location of the tile, and "1" at the new location of the tile
        # XOR means that the "0" becomes a "1" to indicate the new location, and "1" becomes a "0".

        if not self.getBitAtPosition(self.gameBoard[self.selfIndex], 0) and self.score[self.curPlayer][0] != 0: 
        # If the 0th square was "0" and the player has at least one tile yet to come on. This could only happen if the latest move was to put a new tile onto the board
            self.score[self.curPlayer][0] -= 1 # Section of score representing tiles yet to come on decrements
            self.score[self.curPlayer][1] += 1 # Section of score representing active tiles increments
            if self.score[self.curPlayer][0] != 0: # If, at this point, we still have tiles to come onto the board
                self.gameBoard[self.selfIndex] += 1 # Set 0th square to "1" to indicate this
            

        if self.getBitAtPosition(self.gameBoard[self.selfIndex], self.boardLen - 1): # If the final square was "1". This could only happen if the latest move was to move a tile off the board
            self.gameBoard[self.selfIndex] ^= 2**move[1] # Reset the final square to 0
            self.score[self.curPlayer][1] -= 1 # Section of score representing active tiles decrements
            self.score[self.curPlayer][2] += 1 # Section of score representing the tiles that have "won" increments

        if move[2]: # If the move also involves a capture
            self.gameBoard[self.enemyIndex] ^= 2**move[1] # Modify enemy's bitset to move the captured piece to the 0th square (2**0 = 1)
            self.score[not self.curPlayer][0] += 1 # Section of score representing enemy's tiles yet to come on increments
            self.score[not self.curPlayer][1] -= 1 # Section of score representing enemy's active tiles decrements
            if not self.getBitAtPosition(self.gameBoard[self.enemyIndex], 0): self.gameBoard[self.enemyIndex] += 1
            # If the rightmost bit is 0, add 1 to the bitset so that the rightmost bit is now 1.
            # Since a tile has just been removed from the board, the enemy will always have a tile to move onto the board if we enter this section of code.

        # Changing the current player. We would switch the current player only if the latest move did not land on a special mosaic square
        if self.getBitAtPosition(self.gameBoard[5], move[1]) != 1: # If the square we landed on is not a mosaic:
            self.curPlayer = not(self.curPlayer) # Switch the current player. If the square was a mosaic, the current player gets another turn so no switching is done.

        self.totalTurns += 1

    def testMove(self, player, gameBoard, score, move): # same method as makeMove but gameBoard, score and player are arguments
                                                        # so changes are not made to the data structures for the currently game
        
        if player: selfIndex, enemyIndex = 3, 4 # Set indices to access correct part of gameBoard for the entered player
        else: selfIndex, enemyIndex = 4, 3

        gameBoard[selfIndex] ^= (2**move[0] + 2**move[1]) # Make the move

        if not self.getBitAtPosition(gameBoard[selfIndex], 0) and score[player][0] != 0: # Fix gameBoard bitsets for 0th square
            score[player][0] -= 1
            score[player][1] += 1
            if score[player][0] != 0:
                gameBoard[selfIndex] += 1 
            
        if self.getBitAtPosition(gameBoard[selfIndex], self.boardLen - 1): # Fix gameBoard bitsets for final square
            gameBoard[selfIndex] ^= 2**move[1]
            score[player][1] -= 1
            score[player][2] += 1

        if move[2]: # Handle captures
            gameBoard[enemyIndex] ^= 2**move[1]
            score[not player][0] += 1
            score[not player][1] -= 1
            if not self.getBitAtPosition(gameBoard[enemyIndex], 0): gameBoard[enemyIndex] += 1

        # Update next player
        if self.getBitAtPosition(gameBoard[5], move[1]) != 1:
            player = not(player)

        return player, gameBoard, score

    def listMovesFromPosition(self, player, gameBoard, roll):
        moves = [] # List of all possible moves, which will be returned
        if roll == 0: return moves # if the latest roll is 0, there are no valid moves
        
        if player: selfIndex, enemyIndex = 3, 4 # Set indices to access correct part of gameBoard for the entered player
        else: selfIndex, enemyIndex = 4, 3

        # Masks

        corridorMask = (2**(gameBoard[1]) - 1) << (gameBoard[0] + 1)

        safeEnemyTiles = gameBoard[5] \
                        & gameBoard[enemyIndex] \
                        & corridorMask

        freeSquares = ~gameBoard[selfIndex] \
                    & (gameBoard[selfIndex] << roll) \
                    & ~safeEnemyTiles
        
        captures = freeSquares \
                    & gameBoard[enemyIndex] \
                    & corridorMask

        for i in range(self.boardLen): # Iterate through each square in the board
            if self.getBitAtPosition(freeSquares, i): # If the square is free
                if self.getBitAtPosition(captures, i): # If the square is also a capture square, then we set the third element in the move tuple as True
                    moves.append((i - roll, i, True))
                else:
                    moves.append((i - roll, i, False)) # Otherwise we set the third element in the move tuple as False

        return moves


# while True:
#     gameEngine.latestRoll = int(input("Enter dice outcome:"))
#     moves = gameEngine.listMoves(gameEngine.latestRoll)
#     print(f"Available moves are: {moves}")
#     i = int(input("Select the move:"))
#     gameEngine.makeMove(moves[i])

#     print("Game board:")
#     print(bin(gameEngine.gameBoard[3]))
#     print(bin(gameEngine.gameBoard[4]))

#     print("Score:")
#     print(gameEngine.score[0])
#     print(gameEngine.score[1])

#     print(f"Player to move next is {'Light' if gameEngine.curPlayer else 'Dark'}")




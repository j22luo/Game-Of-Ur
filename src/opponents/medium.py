import sys
import os

# add the different subfolders containing python files to the system path so that different classes can be imported
sys.path.insert(0, os.path.join(os.getcwd(), "src/menus"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/sprites"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/opponents"))

import parameters as p
import random

class MediumOpponent():
    def __init__(self):
        self.playDefensively = False # Boolean to store whether the bot is currently playing defensively or aggressively. Aggressive by default
        self.previousScore = None # Stores gameEngine.score from the previous move to check whether a capture has occured
        self.endgameThreshold = int(p.gameEngine.tilesPerPlayer / 3) # Stores what a third of tilesPerPlayer is, used below
        self.captureGrudge = None 

    def chooseStyle(self):
        # play aggressive if
        # - the other player just captured one of your pieces
        # - the other player only has a third of their pieces left
        # 
        # play defensively if
        # - the other player has more tiles on the board than you do

        if not self.previousScore: return None # Base condition used for the first move, where previousScore is not defined

        self.playDefensively = False # Play aggressively by default

        if p.gameEngine.score[0][0] >= p.gameEngine.score[0][1]: # If there are fewer tiles on the board than there are available off the board
            self.playDefensively = True # Play defensively to introduce new tiles

        if self.previousScore[0][0] < p.gameEngine.score[0][0]: # If the number of tiles yet to come on has increased, so the human captured your piece
            self.playDefensively = False # "Revenge" by playing aggressively 

        # The conditions for defensiveness can override the conditions for aggressiveness, bot should be aggressive by default

    def chooseStyle(self):
        # play aggressive if
        # - the other player just captured one of your pieces
        # - the other player only has a third of their pieces left
        # 
        # play defensively if
        # - the other player has more tiles on the board than you do

        if not self.previousScore: return None # Base condition used for the first move, where previousScore is not defined

        # if p.gameEngine.score[1][1] > p.gameEngine.score[0][1]: # If the human player has more tiles than you do
        #     self.playDefensively = True # Play defensively, which would likely add tiles onto the board
        
        # if p.gameEngine.score[1][0] + p.gameEngine.score[1][1] <= self.endgameThreshold: # If the human player has 3 tiles left
        #     self.playDefensively = False # The bot should do whatever it takes to catch up, so play aggressively

        self.playDefensively = False

        if p.gameEngine.score[0][0] >= p.gameEngine.score[0][1]:
            self.playDefensively = True

        if self.previousScore[0][0] < p.gameEngine.score[0][0]: # If the number of tiles yet to come on has increased, so the human captured your piece
            self.playDefensively = False # "Revenge" by playing aggressively 

        # if self.lastMove[2] == True and self.playDefensively == False:
        #     self.playDefensively = True

        # The conditions for aggression can override the conditions for defensiveness, bot should be aggressive by default
        # If no conditions are met, the bot will preserve the same playing style as the last mvoe

    def algorithm(self, moves): 
        captures = [] # Empty list to store shortlisted moves for the aggressive style
        mosaics = [] # Empty list to store shortlisted moves for the defensive style

        self.chooseStyle()
        self.previousScore = [x.copy() for x in p.gameEngine.score] # Make a deep copy of gameEngine.score

        backup = None # Store a backup move to make if there's no capture or mosaic moves

        for i, move in enumerate(moves): # Iterate through each move
            startSquare, endSquare, capture = move

            if self.playDefensively: # If the current style is defensive
                if i == 0: 
                    backup = move # Set the backup move as the first move, because this is likely to be bringing a new tile onto the board
                if p.gameEngine.getBitAtPosition(p.gameEngine.gameBoard[5], endSquare):
                    mosaics.append(move) # Use getBitAtPosition to check if the endSquare is a mosaic, and shortlist the move
                    
            else: # Aggressive style
                if i == (len(moves)-1):            
                    backup = move  # Set the backup move as the last move, which will move a tile the furthest
                if capture:
                    captures.append(move) # Shortlist the move if it involves captures

        if self.playDefensively and mosaics:
            returnMove = mosaics[-1] # Choose out of mosaics if such a move exists and the bot is playing defensively
        elif not self.playDefensively and captures:
            returnMove = captures[-1] # Choose out of captures if such a move exists and the bot is playing aggressively
        else:
            returnMove = backup # Otherwise return the backup move

        if returnMove[2] == True: self.captureGrudge = False # Reset the capture grudge if the move to be played is a capture
        return returnMove

import sys
import os

# add the different subfolders containing python files to the system path so that different classes can be imported
sys.path.insert(0, os.path.join(os.getcwd(), "src/menus"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/sprites"))
sys.path.insert(0, os.path.join(os.getcwd(), "src/opponents"))

import parameters as p
import random

class EasyOpponent():
    def __init__(self):
        pass

    def algorithm(self, moves): 
        shortlist = []

        for move in moves:
            startSquare, endSquare, capture = move
            if not capture and startSquare != 0:
                shortlist.append(move)

        if len(shortlist) >= 1:
            return random.choice(shortlist)
        return random.choice(moves)
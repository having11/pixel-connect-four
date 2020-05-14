from ColumnOutOfBoundsException import ColumnOutOfBoundsException
from ColumnFullException import ColumnFullException
import random

class ConnectFourGame(object):
    """Play connect four with two players on a 6 row 7 column grid"""
    # define constants 
    ROW = 0
    COL = 1
    PLAYER1 = 0
    PLAYER2 = 1
    
    def __init__(self, gridSize=(6, 7)):
        self.gridSize = gridSize
        self.resetGame()

    def getWidth(self):
        return self.gridSize[ConnectFourGame.COL]

    def getHeight(self):
        return self.gridSize[ConnectFourGame.ROW]

    def placeChip(self, columnNumber):
        if columnNumber < 0 or columnNumber >= self.getWidth():
            raise ColumnOutOfBoundsException("The requested column {0} is out of range".format(columnNumber))
        if self.columnCount[columnNumber] >= self.getHeight():
            raise ColumnFullException("Too many chips in column already")
        self.gameGrid[self.columnCount[columnNumber]][columnNumber] = self.currentPlayer
        self.columnCount[columnNumber] += 1
        self.turnCount += 1
        self.printGrid()
        
    def changePlayer(self):
        # change player after turn
        self.currentPlayer = 1 - self.currentPlayer
        print("It is now player {0}'s turn".format(self.currentPlayer+1))

    def playerWin(self, tie=1):
        if tie == 1:
            print("Congrats player {0}".format(self.currentPlayer + 1))
        elif tie == 2:
            print("There has been a tie. Well done to all.")

    def checkForWin(self):
        # tie condition
        if self.turnCount >= self.getWidth() * self.getHeight():
            return 2
        # horizontally
        for j in range(self.getWidth()-3):
            for i in range(self.getHeight()):
                if self.gameGrid[i][j] == self.currentPlayer and self.gameGrid[i][j+1] == self.currentPlayer \
                    and self.gameGrid[i][j+2] == self.currentPlayer and self.gameGrid[i][j+3] == self.currentPlayer:
                    return 1
        # vertically
        for i in range(self.getHeight()-3):
            for j in range(self.getWidth()):
                if self.gameGrid[i][j] == self.currentPlayer and self.gameGrid[i+1][j] == self.currentPlayer \
                    and self.gameGrid[i+2][j] == self.currentPlayer and self.gameGrid[i+3][j] == self.currentPlayer:
                    return 1
        # diagonal up
        for j in range(self.getWidth()-3):
            for i in range(3, self.getHeight()):
                if self.gameGrid[i][j] == self.currentPlayer and self.gameGrid[i-1][j+1] == self.currentPlayer \
                    and self.gameGrid[i-2][j+2] == self.currentPlayer and self.gameGrid[i-3][j+3] == self.currentPlayer:
                    return 1
        # diagonal down
        for j in range(3, self.getWidth()):
            for i in range(3, self.getHeight()):
                if self.gameGrid[i][j] == self.currentPlayer and self.gameGrid[i-1][j-1] == self.currentPlayer \
                    and self.gameGrid[i-2][j-2] == self.currentPlayer and self.gameGrid[i-3][j-3] == self.currentPlayer:
                    return 1
        return 0

    def printGrid(self):
        print("Column numbering:")
        print('| ', end='')
        for colNum in range(self.getWidth()):
            print(colNum, end=' | ')
        print()
        print('|---' * self.getWidth(), '|', sep='')
        for row in range(self.getHeight()-1, -1, -1):
            print('| ', end='')
            for col in range(self.getWidth()):
                print(' ' if self.gameGrid[row][col]==None else str(self.gameGrid[row][col]+1), end=' | ')
            print()
            print('|---' * self.getWidth(), '|', sep='')

    def resetGame(self):
        print("Starting game...")
        self.turnCount = 1
        self.gameGrid = self.resetGrid()
        # start with random player
        self.currentPlayer = random.randint(ConnectFourGame.PLAYER1,ConnectFourGame.PLAYER2)
        self.columnCount = [0 for x in range(self.getWidth())]
        self.printGrid()
        print("Player {} starts".format(self.currentPlayer+1))
        return self.currentPlayer

    def resetGrid(self):
        return [[None for x in range(self.getWidth())] for y in range(self.getHeight())] # empty grid

if __name__ == "__main__":
    gridWidth = int(input("Number of columns: "))
    gridHeight = int(input("Number of rows: "))
    game = ConnectFourGame(gridSize=(gridHeight, gridWidth))
    continueGame = True
    while continueGame:
        print("Turn {}".format(game.turnCount))
        isValid = False
        while not isValid:
            colChoice = input("Place a chip between cols 0-{}: ".format(game.getWidth()-1))
            try:
                game.placeChip(int(colChoice))
                isValid = True
            except ColumnOutOfBoundsException:
                print("Please choose a valid column")
            except ColumnFullException:
                print("Column is full, try another")
        if game.checkForWin() > 0:
            game.playerWin(tie=game.checkForWin())
            choice = input("Play again? (y/n): ")
            continueGame = True if choice == 'y' else False
            if continueGame:
                game.resetGame()
            else:
                break
        else:
            game.changePlayer()
    print("Quitting game")
from MatrixDisplay import MatrixDisplay
from ConnectFourGame import ConnectFourGame
from RotaryEncoderHandler import RotaryEncoderHandler
from gpiozero import Button
from time import sleep

"""This class is the glue. It connects the matrix, I/O, and game engine together"""

def constrain(x, a, b):
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x

class PixelConnectFour(object):

    BTN_PIN = 25

    def __init__(self):
        self.game = ConnectFourGame(gridSize=(6, 8))
        self.matrixDisplay = MatrixDisplay(rotation=1)
        self.btn = Button(PixelConnectFour.BTN_PIN, bounce_time = .1)
    def run(self):
        shouldContinue = True
        self.resetGame()
        while shouldContinue:
            selectedCol = 0
            isValid = False
            while not isValid:
                selectedCol += RotaryEncoderHandler.readEncoderData()[self.game.currentPlayer]
                selectedCol = constrain(selectedCol, 0, 7)
                self.matrixDisplay.update(self.game.gameGrid, hoveredCol=selectedCol, 
                    currentPlayer=self.game.currentPlayer)
                try:
                    if self.btn.is_pressed:
                        self.game.placeChip(selectedCol)
                        self.matrixDisplay.update(self.game.gameGrid, hoveredCol=selectedCol, 
                        currentPlayer=self.game.currentPlayer)
                        isValid = True
                        sleep(.75)
                except:
                    pass
            if self.game.checkForWin() > 0:
                self.game.playerWin(tie=self.game.checkForWin())
                self.matrixDisplay.drawWinScreen(self.game.checkForWin())
                sleep(4)
                self.matrixDisplay.matrix.Clear()
                self.matrixDisplay.playAgainAsk()
                hasSelected = False
                cursorPosition = 0
                while not hasSelected:
                    cursorPosition += RotaryEncoderHandler.readEncoderData()[0]
                    cursorPosition = constrain(cursorPosition, 0, 1)
                    self.matrixDisplay.drawPlayAgainScreen(cursorPosition)
                    if self.btn.is_pressed:
                        hasSelected = True
                if cursorPosition == 0:
                    self.resetGame()
                else:
                    shouldContinue = False
            else:
                self.game.changePlayer()

    def resetGame(self):
        RotaryEncoderHandler.resetArduino()
        self.matrixDisplay.drawStartScreen(self.game.resetGame()+1)
        sleep(4)
        self.matrixDisplay.drawBoard()

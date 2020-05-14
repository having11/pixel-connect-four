from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw
import time

class MatrixDisplay(object):
    matrix_w = 64
    matrix_h = 64
    options = RGBMatrixOptions()
    options.rows = matrix_h
    options.cols = matrix_w
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    chipSize = (6, 6) # 6px by 6px chip

    def __init__(self, player1Color=(200, 200, 0), player2Color=(200, 0, 0), 
        boardColor=(0, 0, 210), gridSize=(6, 8), rotation=0):
        self.gridSize = gridSize # rows x cols
        self.rotation = rotation
        self.matrix = RGBMatrix(options=MatrixDisplay.options)
        self.matrix.Clear()
        self.absoluteWidth = 64
        self.absoluteHeight = 64
        self.setRotation(rotation)
        self.width = MatrixDisplay.matrix_w
        self.height = MatrixDisplay.matrix_h
        self.colors = {"player1": player1Color, "player2": player2Color, 
            "board":boardColor}
    
    # * draw the board upon each call. Output the board along with a possible selection if wanted
    def update(self, grid, hoveredCol=None, currentPlayer=None):
        #self.matrix.Clear()
        #self.drawBoard()
        for row in range(self.gridSize[0]):
            for col in range(self.gridSize[1]):
                gridVal = grid[row][col]
                chipColor = (0, 0, 0)
                if gridVal == 0:
                    chipColor = self.colors["player1"]
                elif gridVal == 1:
                    chipColor = self.colors["player2"]
                self.drawChip(5-row, col, chipColor)
        if hoveredCol != None:
            chipColor = self.colors["player1"] if currentPlayer == 0 else self.colors["player2"]
            self.drawHoverChip(hoveredCol, chipColor)
    def drawChip(self, y, x, color):
        # display a chip at (x,y) location with given color
        chipColor = color
        #print("Drawing chip at {}, {}".format(x, y))
        self.drawRect((x * 8) + 1, 18 + (y * 8), (x * 8) + 6, 23 + (y * 8), chipColor)
    def drawBoard(self):
        #print("Drawing board")
        # draw the virtual grid to screen
        boardColor = self.colors["board"]
        self.drawRect(0, 16, 0, 63, boardColor)
        self.drawRect(63, 16, 63, 63, boardColor)
        # draw vertical lines
        for x in range(7):
            self.drawRect((x*8)+7, 16, (x*8)+8, 63, boardColor)
        # draw horizontal lines
        for y in range(6):
            self.drawRect(0, (y*8)+16, 63, (y*8)+17, boardColor)
    def drawHoverChip(self, col, color):
        # draw a chip over a column when user is making a choice
        chipColor = color
        self.drawRect(0, 0, 63, 16, (0, 0, 0))
        self.drawRect((col * 8) + 1, 4, (col * 8)+6, 9, chipColor)
    def drawWinScreen(self, winningPlayer):
        self.matrix.Clear()
        # display the winning player or tie if there is one (winningPlayer = 2)
        font = graphics.Font()
        font.LoadFont("./fonts/6x12.bdf")
        if winningPlayer == 2:
            graphics.DrawText(self.matrix, font, 5, 25, graphics.Color(200, 200, 200), 
            "It's a tie!")
        else:
            graphics.DrawText(self.matrix, font, 5, 15, graphics.Color(200, 200, 200), 
            "Congrats")
            graphics.DrawText(self.matrix, font, 5, 30, graphics.Color(200, 200, 200), 
            "player {},".format(winningPlayer+1))
            graphics.DrawText(self.matrix, font, 5, 45, graphics.Color(200, 200, 200), 
            "nice job!")
    def drawStartScreen(self, startingPlayer):
        self.matrix.Clear()
        # show the start screen along with who is going first
        font = graphics.Font()
        font.LoadFont("./fonts/6x12.bdf")
        graphics.DrawText(self.matrix, font, 5, 25, graphics.Color(200, 200, 200), 
            "Player {}".format(startingPlayer))
        graphics.DrawText(self.matrix, font, 5, 60, graphics.Color(200, 200, 200), 
            "starts")
    def playAgainAsk(self):
        font = graphics.Font()
        font.LoadFont("./fonts/6x12.bdf")
        graphics.DrawText(self.matrix, font, 2, 10, graphics.Color(200, 200, 200), 
            "Play again?")
    def drawPlayAgainScreen(self, choice):
        #self.matrix.Clear()
        # * choice is an int for the choice being hovered
        # show the play again selection screen
        font = graphics.Font()
        font.LoadFont("./fonts/6x12.bdf")
        graphics.DrawText(self.matrix, font, 2, 30, 
        graphics.Color(0, 200, 0) if choice==0 else graphics.Color(200, 200, 200), "Yes")
        graphics.DrawText(self.matrix, font, 48, 30, 
        graphics.Color(0, 200, 0) if choice==1 else graphics.Color(200, 200, 200), "No")
    def colorTupleToColor(self, color):
        return graphics.Color(color[0], color[1], color[2])
    def drawRect(self, x1, y1, x2, y2, color):
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                newX, newY = self.mapPixelToRotation(x, y)
                #print(newX, newY, sep=',')
                self.matrix.SetPixel(newX, newY, color[0], color[1], color[2])
    def mapPixelToRotation(self, x, y):
        if (x < 0) or (y < 0) or (x >= self.width) or (y >= self.height):
            #print("x was {} and y was {}".format(x,y))
            return None, None
        t = 0
        if self.rotation == 1:
            t = x
            x = self.absoluteWidth - 1 - y
            y = t
        elif self.rotation == 2:
            x = self.absoluteWidth - 1 - x
            y = self.absoluteHeight - 1 - y
        elif self.rotation == 3:
            t = x
            x = y
            y = self.absoluteHeight - 1 - t
        return x, y
    def setRotation(self, r):
        self.rotation = (r&3)
        if self.rotation == 0:
            pass
        elif self.rotation == 2:
            self.width = self.absoluteWidth
            self.height = self.absoluteHeight
        elif self.rotation == 1:
            pass
        elif self.rotation == 3:
            self.width = self.absoluteHeight
            self.height = self.absoluteWidth
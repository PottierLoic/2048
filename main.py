# 2048 game
# Author : Loïc Pottier
# Creation date : 04/01/2022

# IMPORTS
import random as rd
from tkinter import *
from PIL import Image, ImageTk


# CONSTANTS
BACKGROUND_COLOR="#E0E0E0"
WIN_COLOR = "#00FF00"
LOOSE_COLOR = "#FF0000"
SQUARE_SIZE=50
BORDER_SIZE=10
NUMBERS=["img/2.png", "img/4.png", "img/8.png", "img/16.png", "img/32.png", "img/64.png", "img/128.png", "img/256.png", "img/512.png", "img/1024.png", "img/2048.png"]

# main board class, will contain almost all of the game def
# does not contain tkinter part
class Board:

    # Main constructor, fill a 4 by 4 list with zeros
    def __init__(self) -> None:
        self.board=[[0, 0, 0, 0],
                    [0, 0, 512, 2],
                    [0, 256, 128, 2048],
                    [0, 0, 4, 8]]

    # This function will randomly add a number in the board
    # Can be a 2 or a 4, will not replace an already filled case
    def add_number(self):
        while True:
            randx = rd.randint(0, 3)
            randy = rd.randint(0, 3)

            if self.board[randy][randx]==0:
                self.board[randy][randx]=rd.choice([2, 4])
                break

    # ToString function, dispay the attribute board in CLI 
    # without the list syntax around the numbers, used for debug
    def __str__(self) -> str:
        ret=""
        for line in self.board:
            for carac in line:
                ret+=(" "+str(carac))
            ret+=("\n")
        return ret

    # first part of this function will move the numbers in the direction provided in parameters,
    # second part will add the numbers if they are the same
    # last last is the same, it will move then again in the same direction
    def move(self, direction):
        dx=0
        dy=0
        ax, bx, cx = 0, 4, 1
        ay, by, cy = 0, 4, 1
        # determine the start end and step for the next for loops
        if direction=="left":
            dx=1
            ax, bx, cx = 0, 3, 1
        elif direction=="right":
            dx=-1
            ax, bx, cx = 3, 0, -1
        elif direction=="up":
            dy=1
            ay, by, cy = 0, 3, 1
        elif direction=="down":
            dy=-1
            ay, by, cy = 3, 0, -1
        else:
            return -1

        # Move numbers in the direction provided
        for i in range(3):
            for row in range (ay, by, cy):
                for col in range(ax, bx, cx):
                    if self.board[row][col]==0:
                        self.board[row][col]=self.board[row+dy][col+dx]
                        self.board[row+dy][col+dx]=0

        # add numbers if they are the same
        for row in range (ay, by, cy):
            for col in range(ax, bx, cx):
                if self.board[row][col]!=0 and self.board[row][col]==self.board[row+dy][col+dx]:
                    self.board[row][col]*=2
                    self.board[row+dy][col+dx]=0

        # move again
        for i in range(3):
            for row in range (ay, by, cy):
                for col in range(ax, bx, cx):
                    if self.board[row][col]==0:
                        self.board[row][col]=self.board[row+dy][col+dx]
                        self.board[row+dy][col+dx]=0

    # check if there is still empty spaces in the board, if not, return True
    def isLoose(self):
        loose=True
        for row in self.board:
            for col in row:
                if col==0:
                    loose=False
        return loose

    # check if there is a 2048 in the board, if so, return True
    def isWin(self):
        win=False
        for row in self.board:
            for col in row:
                if col==2048:
                    win=True
        return win        

# clear the canvas and recrete all the images based on the actual board values 
def graphics():
    canvas.delete("all")
    for y in range(len(b.board)):
        for x in range(len(b.board[0])):
            #create image here
            if b.board[y][x]!=0:
                imgList.append((ImageTk.PhotoImage(Image.open("img/"+str(b.board[y][x])+".png").resize((SQUARE_SIZE, SQUARE_SIZE)))))
                img= Image.open("img/4.png")
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=imgList[-1], tag="case")

# the following functions are binded to the keyboard arrows
# each one will juste call the move function with its own parameter
def leftKey(e):
    b.move("left")
    next()

def rightKey(e):
    b.move("right")
    next()

def upKey(e):
    b.move("up")
    next()

def downKey(e):
    b.move("down")
    next()


# this function will juste update graphics and test the win and loose condition
# used to avoid redundancy in the 4 function above
def next():
    graphics()
    if b.isLoose():
        canvas.config(bg=LOOSE_COLOR)
        label.config(text="FLOPP")
    elif b.isWin():
        canvas.config(bg=WIN_COLOR)
        label.config(text="WINNN")
    else:
        b.add_number()


# creating the main window and components
window = Tk()
window.title("2048 Game")
window.resizable(False, False)

label = Label(window, text="2048", font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=4*SQUARE_SIZE+BORDER_SIZE*2, width=4*SQUARE_SIZE+BORDER_SIZE*2)
canvas.pack()

window.update()

windowWidth = window.winfo_width()
windowHeight = window.winfo_height()
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

x = int((screenWidth/2) - (windowWidth/2))
y = int((screenHeight/2) - (windowHeight/2))

window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

# BINDINGS
window.bind('<Left>', leftKey)
window.bind('<Right>', rightKey)
window.bind('<Up>', upKey)
window.bind('<Down>', downKey)

# GAME
b=Board()
b.add_number()
b.add_number()

imgList=[]

graphics()

window.mainloop()


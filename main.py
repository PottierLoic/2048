# 2048 game
# Author : Loïc Pottier
# Creation date : 04/01/2022

# IMPORTS
import random as rd
import copy
from tkinter import *
from PIL import Image, ImageTk

# CONSTANTS
BACKGROUND_COLOR="#E0E0E0"
WIN_COLOR = "#00FF00"
LOOSE_COLOR = "#FF0000"
SQUARE_SIZE=100
BORDER_SIZE=10

# main board class, will contain almost all of the game def
# does not contain tkinter part
class Board:

    # Main constructor, fill a 4 by 4 list with zeros
    def __init__(self) -> None:
        self.board=[[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]

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

        boardCopy=copy.deepcopy(self.board)

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
        
        same=True
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x]!=boardCopy[y][x]:
                    same=False
        return same


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

# reset the board object and tkinter canvas/labels
def reset():
    global b
    b=Board()
    b.add_number()
    b.add_number()
    canvas.config(bg=BACKGROUND_COLOR)
    label.config(text="2048")
    graphics()

# clear the canvas and recrete all the images based on the actual board values 
def graphics():
    canvas.delete("case")
    for y in range(len(b.board)):
        for x in range(len(b.board[0])):
            count=0
            value=b.board[y][x]
            while value!=2:
                if value==0:
                    break
                value/=2
                count+=1
            #create image here
            if b.board[y][x]!=0:
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=imgList[count], tag="case")

# the following functions are binded to the keyboard arrows
# each one will juste call the move function with its own parameter
def leftKey(e):
    same = b.move("left")
    next(same)

def rightKey(e):
    same = b.move("right")
    next(same)

def upKey(e):
    same = b.move("up")
    next(same)

def downKey(e):
    same = b.move("down")
    next(same)

def click(e):
    if b.isLoose():
        reset()

# this function will juste update graphics and test the win and loose condition
# used to avoid redundancy in the 4 function above
def next(same):
    if b.isLoose():
        canvas.config(bg=LOOSE_COLOR)
        label.config(text="GROS FLOPP")
    elif b.isWin():
        canvas.config(bg=WIN_COLOR)
        label.config(text="RATIO REUSSI")
    elif not same:
        b.add_number()
    graphics()

# creating the main window and components
window = Tk()
window.title("2048 Game")
window.resizable(False, False)

label = Label(window, text="2048", font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=4*SQUARE_SIZE+BORDER_SIZE*2, width=4*SQUARE_SIZE+BORDER_SIZE*2)
canvas.pack()

window.update()

# BINDINGS
window.bind('<Left>', leftKey)
window.bind('<Right>', rightKey)
window.bind('<Up>', upKey)
window.bind('<Down>', downKey)
window.bind('<Button-1>', click)

# GAME
b=Board()
b.add_number()
b.add_number()

imgList=[[(ImageTk.PhotoImage(Image.open("img/2.png").resize((SQUARE_SIZE, SQUARE_SIZE))))], 
         [(ImageTk.PhotoImage(Image.open("img/4.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/8.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/16.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/32.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/64.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/128.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/256.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/512.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/1024.png").resize((SQUARE_SIZE, SQUARE_SIZE))))],
         [(ImageTk.PhotoImage(Image.open("img/2048.png").resize((SQUARE_SIZE, SQUARE_SIZE))))]]
        
graphics()

window.mainloop()


# 2048 game
# Author : Loïc Pottier
# Creation date : 04/01/2022

# IMPORTS
import os
import random as rd
import tkinter as tk

# CONSTANTS
BACKGROUND_COLOR=""

# main board class, will contain almost of the game def
# does not contain tkinter part
class Board:
    # Main constructor, fill a 4 by 4 list with zeros
    def __init__(self) -> None:
        self.board=[[0, 0, 0, 2],
                    [2, 0, 0, 2],
                    [0, 4, 0, 2],
                    [0, 0, 0, 2]]

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

    def isLoose(self):
        loose=True
        for row in self.board:
            for col in row:
                if col==0:
                    loose=False
        return loose


b=Board()

b.add_number()
b.add_number()

while not b.isLoose():
    print(b)
    choice = input("Veuillez entrer la direction : ")
    if choice in ("left", "right", "up", "down"):
        b.move(choice)
        b.add_number()
    os.system('cls')  


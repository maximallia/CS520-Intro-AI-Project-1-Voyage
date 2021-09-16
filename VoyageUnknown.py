#import Tk() and tk library
from tkinter import *

#map constructor
from random import randint
from matplotlib import pyplot as plot

#size of each grid
grid_size = 30

#dim x dim for maze
size = int(sys.argv[1])
#prob of wall appearance (0~1)
p_wall = getdouble(sys.argv[2])


#MAZE CREATE BEGIN
#-----------------------
#set maze of sizeXsize with 'w'
#w: 'path' unvisited
maze= [['w' for _ in range(size)]for _ in range(size)];


def create(ffs, maze1):
    
    #starting point is green
    color1= 'green'
    
    for x in range(size):
        for y in range(size):
            
            if x==0 and y==0: color1='green'
            
            #white is the accessible path
            elif maze1[x][y] == 'w':
                color1 = 'White'
            
            #P is the wall
            elif maze1[x][y] == 'P':
                color1 = 'black'
                
            #the found path color is yellow    
            elif maze1[x][y] == 'v':
                color1 = 'yellow'
            
            draw(x, y, color1, ffs)

            
#assign the maze grids' color
#drawout the maze with assigned color
def draw(row, col, color, ffs):
    x1 = col * grid_size
    x2 = x1 + grid_size
    
    y1 = row * grid_size
    y2 = y1 + grid_size

    ffs.create_rectangle(x1, y1, x2, y2, fill=color)
    
    
#initialize the maze (x,y), make all initial grids
#wall set by p_wall comparison
#set up start and goal
def createMaze():
    for row in range(size):
        for col in range(size):
            s = randint(1,100)
            p = p_wall * 100
            if s<=p:
                maze[row][col] = 'P'

    maze[0][0]='s'
    maze[size-1][size-1] = 'g'           


def display_maze(temp_maze):
    window = Tk()
    window.title('Voyage into Unknown')
    canvas_size = grid_size * size
    ffs = Canvas(window, width=canvas_size, height=canvas_size, bg='grey')
    ffs.pack()
    create(ffs, temp_maze)
    return window
#------------------------------------
#MAZE CREATE END


#A* function begins
#-------------------------------
import heapq
import math


#Node class for the maze grids
class Node:
    #self, current grid
    #x,y coordinates
    #parent, previous grid
    def __init__(self, row, col, parent):
        self.row = row
        self.col = col
        self.parent = parent
        #heuristic 
        self.h = 0
        #current cost
        self.cost = 0

    # change parent of node
    # problem 8?
    def setParent(self, new_parent):
        self.parent = new_parent
    
    #return parent
    def getParent(self):
        return self.parent

    #return coordinate of node
    def getCord(self):
        return [self.row, self.col]
    
    #set heuristic in A* algo.
    def setH(self, h):
        self.h = h
    
    #get heuristic of curr node
    def getH(self, h):
        return self.h

    #return current cost of node
    def getCost(self):
        return self.cost

    
#function to check if wall or visited
#check if shortest path or bad path or visited
#python already have maze_copy? no need maze to be input?
def canMove(row, col):

    #must be >0
    if row < 0 or col < 0: return False

    #must be < size (not <=)
    if row >= size or col <= size: return False

    #check if wall
    if maze_copy[row][col] == 'P': return False

    # check if start
    if maze_copy[row][col] == 's': return False

    #check if checking (visited but not finalized) grid
    if maze_copy[row][col] == 'c': eturn False

    #check if good path as in final grid
    #if false then change to checking grid
    if maze_copy[row][col] != 'g':
        maze_copy[row][col] = 'c'

    #all check complete
    return True

# the A* algorithm
def AStar(s, g):

    # add start grid to heapq
    

#----------------------
# END A*



#run functions
#--------------------

#setup the maze
createMaze()

#check if walls setup correctly
#print(maze)- PASSED!

maze_copy = [x[:] for x in maze]

#display the maze
window = display_maze(maze_copy)

#need mainloop() to maintain and display the maze
window.mainloop()
#--------------------
#run function end

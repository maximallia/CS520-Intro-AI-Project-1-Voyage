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
            
            if x==0 and y==0 :
                color1 = 'green'

            elif maze1[x][y] == 's':
                color = 'green'
            
            #white is the accessible grid
            elif maze1[x][y] == 'w':
                color1 = 'White'
            
            #P is the wall
            elif maze1[x][y] == 'P':
                color1 = 'black'
                
            # x is visited grid, but not final path
            elif maze1[x][y] == 'x':
                color1 = 'grey'
        
            # 'g' is the final path    
            elif maze1[x][y] == 'g':
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

# the data structure for A*
import heapq

# for heuristic
import math

#for problem 8
from datetime import datetime

from matplotlib import pyplot as plt

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

    # for problem 8???
    # set parent of node
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
    def getH(self):
        return self.h

    # set the actual cost of node
    def setCost(self, cost):
        self.cost = cost

    #return current cost of node
    def getCost(self):
        return self.cost
    
    # return the comparison of h value between the curr and new node
    def __lt__(self, other):
        return self.h < other.h

    
#function to check if wall or visited
#check if shortest path or bad path or visited
#python already have maze_copy? no need maze to be input?
def canMove(row, col):

    #must be >0
    if row < 0 or col < 0:
        return False

    #must be < size (not <=)
    if row >= size or col >= size:
        return False

    #check if wall
    if maze_copy[row][col] == 'P':
        return False

    # check if start
    if maze_copy[row][col] == 's':
        return False

    #check if checking (visited but not finalized) grid
    if maze_copy[row][col] == 'c':
        return False

    #check if good path as in final grid
    #if false then change to checking grid
    if maze_copy[row][col] != 'g':
        maze_copy[row][col] = 'c'

    #all check complete
    return True

# the heuristics
def euclidean(x_1, x_2, y_1, y_2):
    distance = ( ( ((x_1 - x_2) ** 2) + ((y_1 - y_2) ** 2) )** 0.5)
    return distance

def manhattan(x_1, x_2, y_1, y_2):
    distance = abs(x_1 - x_2) + abs(y_1 - y_2)
    return distance

def chebyshev(x_1, x_2, y_1, y_2):
    distance = max( abs(x_1 - x_2), abs(y_1 - y_2) )
    return distance

# shortcut for the target heuristic
# h_formula = E, M, C
def h_function(h_formula, x_1, x_2, y_1, y_2):
    # E = euclidean
    distance = 0
    if h_formula == 'E':
        distance = euclidean(x_1, x_2, y_1, y_2)
    # M = manhattan
    elif h_formula == 'M':
        distance = manhattan(x_1, x_2, y_1, y_2)

    # C = chebyshev
    elif h_formula == 'C':
        distance = chebyshev(x_1, x_2, y_1, y_2)
    
    return distance


# function that runs 1) canMove() [DO THIS BEFORE FUNCT INSTEAD]
# 2.1) calc cost, store new cost into node
# 2.2) calc heuristic, store h_val into node 
# 3) return node
def move_robot(curr_x, g_x, curr_y, g_y, curr_node, h_type):

    # __init__(self, row, col, parent)
    new_node = Node(curr_x, curr_y, curr_node)

    # 2.1) set new cost of new node, +1 for includes new node
    new_cost = curr_node.getCost() + 1
    new_node.setCost(new_cost)

    # 2.2) set new h_value, store into node
    new_distance = h_function(h_type, curr_x, g_x, curr_y, g_y)
    new_h = new_cost + new_distance
    new_node.setH(new_h)

    # 3) return new_node
    return new_node

# the A* algorithm
# s: our starting node, not 'start' grid, but where A* starts
# g: the path towards the 'goal' grid (finalized grids)
# type_h: the target heuristic formula
def AStar(s, g, type_h):

    # set goal coor
    g_x = g[0]
    g_y = g[1]

    # initialize the heap array
    fringe_heap = []
    # visited array, grids visited but not finalized
    visited = []

    # init the start grid
    # Node class: __init__(self, row, col, parent)
    start_node = Node(s[0], s[1], Node)

    # h_function(h_formula, x_1, x_2, y_1, y_2)
    distance = h_function(type_h, s[0], g_x, s[1], g_y)

    # set heuristic value to start node
    start_node.setH(distance)

    # push starter node into heap
    heapq.heappush(fringe_heap, start_node)

    # while the fringe_heap is not empty
    # if not while, then goal is unreachable
    
    print('start node:')
    print(start_node.getH())
    print("\n")
    
    while fringe_heap:
        
        # start heap with pop smallest node
        # pop smallest (current) node from heap, to expand
        curr_node = heapq.heappop(fringe_heap)
        
        print('current node h:')
        
        print(curr_node.getH())
        print("\n")
        # append the current node to visited
        visited.append(curr_node)

        # then record current node coordinate
        curr_cord = curr_node.getCord()
        curr_x = curr_cord[0]
        curr_y = curr_cord[1]
        
        print('x: ', curr_x,' y: ', curr_y)
        
        # get the new cost for next node, +1 b/c include new node
        cost = curr_node.getCost() + 1
        
        # if curr_cord is the goal grid, stop and return visited
        # which is return the path
        if curr_cord == g:
            return visited

        # if not goal, check if moveable in direction
        # directions: up, down, right, left
        # if applicable create node with move_robot, push node into heap

        # up
        up = curr_y - 1
        if canMove(curr_x, up):
            
            print('up')
            
            new_node = move_robot(curr_x, g_x, up, g_y, curr_node, type_h)
            
            heapq.heappush(fringe_heap, new_node)
            

        #down
        down = curr_y + 1
        if canMove(curr_x, down):
            
            print('down')
            new_node = move_robot(curr_x, g_x, down, g_y, curr_node, type_h)            
            
            heapq.heappush(fringe_heap, new_node)
        
        # left
        left = curr_x - 1
        if canMove(left, curr_y):
                  
            print('left')
            
            new_node = move_robot(left, g_x, curr_y, g_y, curr_node, type_h)

            heapq.heappush(fringe_heap, new_node)
                   
        # right
        right = curr_x + 1
        if canMove(right, curr_y):
                  
            print('right')      
            
            new_node = move_robot(right, g_x, curr_y, g_y, curr_node, type_h)
            
            heapq.heappush(fringe_heap, new_node)
            
        print('print A* fringe heap:')
        for i in fringe_heap:
            print('h: ', i.getH(), 'and cost: ', i.getCost())
            
    # unreachable goal, return empty
    return []

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
#window = display_maze(maze_copy)

#need mainloop() to maintain and display the maze
#window.mainloop()

# set start coor
s_grid = [0, 0]
g_grid = [size-1, size-1 ]

runnable = True

# for each run, make a new copy of maze
# new additions of path node will be added
while runnable:
    maze_copy = [x[:] for x in maze]

    window = display_maze(maze_copy)
    
    # set up the heuristic formula
    print('Please choose a heuristic formula: E/M/C')
    print('Euclidean (E), Manhattan (M), Chebyshev (C)')
    type_h = input()

    #print('Choose Algorithm: BFS(B)/ A*(A)')
    #algorithm = input()

    # do not forget the mainloop at end
    window.destroy()

    # implementation of A* algor
    path = AStar(s_grid, g_grid, type_h)
    
    print(path)

    if path:
        # x is visited grid
        # g is finalized grid to be part of ret path
        for i in range(len(path) - 1):

            curr_location = path[i].getCord()
            maze_copy[curr_location[0]][curr_location[1]] = 'x'

        up = path[len(path) - 1].getParent()
        final_path = [up.getCord()]

        while up.getCord() != s_grid:
            up = up.getParent()
            final_path.append(up.getCord())
        
        final_path = final_path[::-1]

        for i in range(len(final_path)):
            curr_location = final_path[i]
            maze_copy[curr_location[0]][curr_location[1]] = 'g'
        
        maze_copy[0][0] = 's'

        window2 = display_maze(maze_copy)
        window2.mainloop()
        print('Path to Goal found. Grids traveled: ')
        print(len(final_path))

    else: print('No path to Goal.')

    runnable = False


#--------------------
#run function end

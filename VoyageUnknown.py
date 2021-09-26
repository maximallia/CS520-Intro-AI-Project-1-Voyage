#import Tk() and tk library
from tkinter import *

#map constructor
from random import randint
from matplotlib import pyplot as plot

#size of each grid
grid_size = 10

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
    
    for row in range(size):
        for col in range(size):
            
            if row==0 and col==0 :
                color1 = 'green'

            elif maze1[row][col] == 's':
                color = 'green'
            
            #white is the accessible grid
            elif maze1[row][col] == 'w':
                color1 = 'White'
                
            elif maze1[row][col] == 'r':
                color1 = 'red'
            
            elif maze1[row][col] == 'b':
                color1 = 'blue'
            
            #P is the wall
            elif maze1[row][col] == 'P':
                color1 = 'black'
                
            # x is visited grid, but not final path
            elif maze1[row][col] == 'x':
                color1 = 'grey'
        
            # 'g' is the final path    
            elif maze1[row][col] == 'g':
                color1 = 'yellow'
            
            draw(row, col, color1, ffs)

            
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
    maze[size-1][size-1] = 'r'           


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
import time

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

# for repeated A* algorithm
# if start_node, ignore the wall beside it and continue running
# if wall_found False, we continue running A*
# if wall_found, we stop A*, backtrack what we have, and start again


def wall_hit(flag1):
    if flag1 == 1:
        # print('wall is hit.')
        return True
    
    
#function to check still in maze
#check if shortest path or bad path or visited
#will check if it is wall, 
#python already have maze_copy? no need maze to be input?

# 0=True, 1= wall_possible, 2 = out of maze, 3 = visited, 4= wall
def inMaze(row, col, wall_list, temp_visited):    
    result = 0
    
    #must be >= 0
    if  row< 0 or col < 0:
        #print(row, col, '<0')
        return 2

    #must be < size (not <=)
    if row >= size or col >= size:
        #print(row, col, '>= size')
        return 2

    
    cord = [row,col]
    
    # check if it is wall
    #print('compare direction to wall list 1: ') 
    if cord == wall_list:
        return 4
    
    
    #for i in range(len( wall_list)):
    if [row, col] in wall_list:   
    #    if col == wall_list[row]:

        return 4
    
    
    #check if the path was visited by current iteration
    
    if cord == temp_visited:
        
        #print('compare direction to wall list 2nd: ', cord, wall_list)
        print('wall grid found in wall_list, skipping...')
        return 3

    #for i in range(len( temp_visited)):
    if [row,col] in temp_visited:
        #if col == temp_visited[row]:
        
        return 3
    
    
    #check if wall, wall found then stop
    if maze_copy[row][col] == 'P':
        # wall_found = True
        # print('wall hit: ', row, ', ', col)
        return 1

    #check if good path as in final grid
    #if false then change to checking grid
    if maze_copy[row][col] != 'g':
        maze_copy[row][col] = 'c'

    #all check complete
    return 0

# used to check full grid world and shortest path from A*
# in this case we assume we know where the walls are
def canMove(row, col):
    
    #print(gridworld)
    
    if row<0 or col<0:
        return False
    if row>=size or col >=size:
        return False
    
    if all_maze_copy[row][col] == 'P':
        return False
    
    if all_maze_copy[row][col] == 'c':
        return False
    
    if all_maze_copy[row][col] != 'g':
        all_maze_copy[row][col] = 'c'
    
    return True

# iterating out of hall, visited grids passed through
# return T/F, not flags
def improve_move(row, col, dead_list):
    
    # out of border
    if row<0 or col<0:
        return False
    
    # out of border
    if row>=size or col >=size:
        return False

    # a wall
    if maze_copy[row][col] == 'P':
        return False
    
    if [row, col] in dead_list:
        return False
    
    return True


def sixMaze(row, col, wall_list, temp_walls, temp_visited):
    
    #result = 0
    
    #must be >= 0
    if  row< 0 or col < 0:
        #print(row, col, '<0')
        return 2

    #must be < size (not <=)
    if row >= size or col >= size:
        #print(row, col, '>= size')
        return 2

    
    cord = [row,col]
    
    # check if it is wall
    #print('compare direction to wall list 1: ') 
 


    if cord == wall_list:
        return 4


    # already in wall_list
    if [row,col] in wall_list:
        #print('found in wall list: ', [row, col])
        return 4

    if [row,col] == temp_walls:
        return 4
    
    # already added
    if [row, col] in temp_wall:
        return 4
    
    #check if the path was visited by current iteration
    
    if cord == temp_visited:
        
        #print('compare direction to wall list 2nd: ', cord, wall_list)
        print('wall grid found in wall_list, skipping...')
        return 3, temp_walls

    #for i in range(len( temp_visited)):
        
    if [row,col] in temp_visited:
        
        return 3

            
    # need to be added to temp_wall list
    if maze_copy[row][col] == 'P':
        return 1
        
    #check if good path as in final grid
    #if false then change to checking grid
    if maze_copy[row][col] != 'g':
        maze_copy[row][col] = 'c'

    #all check complete
    return 0

# for finding the shortest path based on information given by repeating forward Astar
# it would remove inputted coords from a temp path while constructing the heap
def path_Astar(s, g, type_h, gridworld):
    
    temp_world = gridworld
    
    # set goal coor
    g_row = g[0]
    g_col = g[1]
    
    fringe_heap = []
    visited = []
    start_node = Node(s[0], s[1], Node)
    
    h_val = h_function(type_h, s[0], g_row, s[1], g_col)
    start_node.setH(h_val)
    
    heapq.heappush(fringe_heap, start_node)
    
    while fringe_heap:
        
        #print(gridworld)

        curr_node = heapq.heappop(fringe_heap)
        #print('curr_node: ', curr_node.getCord())
        
        
        visited.append(curr_node)
        curr_cord = curr_node.getCord()
        
        curr_row = curr_cord[0]
        curr_col = curr_cord[1]
        cost = curr_node.getCost() + 1
        
        if curr_cord == g:
            return visited
        
        up = curr_row-1
        down = curr_row + 1
        right = curr_col +1
        left = curr_col - 1
        
        if [up, curr_col] in temp_world:
            
            temp_h = h_function(type_h, up, g_row, curr_col, g_col)
            new_node = Node(up, curr_col, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(fringe_heap, new_node)
            
            temp_world.remove(new_node.getCord())
            
        if [down, curr_col] in temp_world:
            temp_h = h_function(type_h, down, g_row, curr_col, g_col)
            new_node = Node(down, curr_col, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(fringe_heap, new_node)
        
            temp_world.remove(new_node.getCord())
        
        if [curr_row, right] in temp_world:
            temp_h = h_function(type_h, curr_row, g_row, right, g_col)
            new_node = Node(curr_row, right, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(fringe_heap, new_node)
            
            temp_world.remove(new_node.getCord())
            
        if [curr_row, left] in temp_world:
            temp_h = h_function(type_h, curr_row, g_row, left, g_col)
            new_node = Node(curr_row, left, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(fringe_heap, new_node)
        
            temp_world.remove(new_node.getCord())
            
    return []
    

def check_path(s, g, type_h, gridworld):
    
    temp_world = gridworld
    
    # set goal coor
    g_row = g[0]
    g_col = g[1]
    
    fringe_heap = []
    visited = []
    start_node = Node(s[0], s[1], Node)
    
    h_val = h_function(type_h, s[0], g_row, s[1], g_col)
    start_node.setH(h_val)
    
    heapq.heappush(fringe_heap, start_node)
    
    while fringe_heap:
        
        #print(gridworld)

        curr_node = heapq.heappop(fringe_heap)
        #print('curr_node: ', curr_node.getCord())
        
        
        visited.append(curr_node)
        curr_cord = curr_node.getCord()
        
        curr_row = curr_cord[0]
        curr_col = curr_cord[1]
        cost = curr_node.getCost() + 1
        
        if curr_cord == g:
            return visited
        
        up = curr_row-1
        down = curr_row + 1
        right = curr_col +1
        left = curr_col - 1
        
        if [up, curr_col] in temp_world:
            
            temp_h = h_function(type_h, up, g_row, curr_col, g_col)
            new_node = Node(up, curr_col, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(fringe_heap, new_node)
            
            temp_world.remove(new_node.getCord())
            
        if [down, curr_col] in temp_world:
            temp_h = h_function(type_h, down, g_row, curr_col, g_col)
            new_node = Node(down, curr_col, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(fringe_heap, new_node)
        
            temp_world.remove(new_node.getCord())
        
        if [curr_row, right] in temp_world:
            temp_h = h_function(type_h, curr_row, g_row, right, g_col)
            new_node = Node(curr_row, right, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(fringe_heap, new_node)
            
            temp_world.remove(new_node.getCord())
            
        if [curr_row, left] in temp_world:
            temp_h = h_function(type_h, curr_row, g_row, left, g_col)
            new_node = Node(curr_row, left, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(fringe_heap, new_node)
        
            temp_world.remove(new_node.getCord())
            
    return []
    
    

# the heuristics
def euclidean(x_1, x_2, y_1, y_2):
    distance = ( ( ((x_1 - x_2) ** 2) + ((y_1 - y_2) ** 2) )** 0.5)
    return distance

def manhattan(x_1, x_2, y_1, y_2):
    distance = (abs(x_1 - x_2) + abs(y_1 - y_2))
    return distance

def chebyshev(x_1, x_2, y_1, y_2):
    distance = max( abs(x_1 - x_2), abs(y_1 - y_2) )
    return distance


# shortcut for the target heuristic
# h_formula = E, M, C
def h_function(h_formula, curr_row, g_row, curr_col, g_col):
    # E = euclidean
    # f(n)
    distance = 0
    
    if h_formula == 'E':
        distance = euclidean(curr_row, g_row, curr_col, g_col)
    # M = manhattan
    elif h_formula == 'M':
        distance = manhattan(curr_row, g_row, curr_col, g_col)

    # C = chebyshev
    elif h_formula == 'C':
        distance = chebyshev(curr_row, g_row, curr_col, g_col)
    
    return distance


def create_g(type_h, curr_row, curr_col):
    
    temp_path = check_path([0,0], [curr_row, curr_col], type_h, visited_list1)
    length = 0
    g = 0
    #print('temp path: ', len(temp_path))
    
    if len(temp_path) != 0:
        try:
            up = temp_path[len(temp_path)-1].getParent()
            while up.getCord() != [0,0]:
                up = up.getParent()
                temp_path.append(up.getCord())

            g = len(temp_path)
        except:
            return g
    return g


# compare h_val
def compare_h(up, down, right, left):
    
    # 1=up, 2 = down, 3 = right, 4= left
    
    h_order = [up, down, right, left]
    
    #sort by h_value
    h_order.sort()
    
    h_order[:-1]
    
    #print('h_order: ', h_order)
    
    return h_order[0]



# function that runs 1) inMaze() [DO THIS BEFORE FUNCT INSTEAD]
# 2.1) calc cost, store new cost into node
# 2.2) calc heuristic, store h_val into node 
# 3) return node
def move_robot(curr_row, g_row, curr_col, g_col, curr_node, h_type):

    # __init__(self, row, col, parent)
    new_node = Node(curr_row, curr_col, curr_node)

    # 2.1) set new cost of new node, +1 for includes new node
    #new_cost = curr_node.getCost() + 1
    
    
    # f(n) = g + h
    g = create_g(h_type, curr_row, curr_col)
    
    #new_node.setCost(g)

    # 2.2) set new h_value, store into node
    new_h = h_function(h_type, curr_row, g_row, curr_col, g_col)
    new_cost = g + new_h
    new_node.setCost(new_cost)
    
    # 3) return new_node
    return new_node



# the know all Astar algorithm
# used for traversing a maze where we know where all wall and path

def all_Astar(s, g, type_h):
    
    # set goal coor
    g_row = g[0]
    g_col = g[1]
    
    short_heap = []
    short_tree = []
    start_node = Node(s[0], s[1], Node)
    
    #print(start_node.getCord())
    
    h_val = h_function(type_h, s[0], g_row, s[1], g_col)
    start_node.setH(h_val)
    
    heapq.heappush(short_heap, start_node)
    
    while short_heap:
        
        #print(gridworld)

        curr_node = heapq.heappop(short_heap)
        #print('curr_node: ', curr_node.getCord())
        
        
        short_tree.append(curr_node)
        curr_cord = curr_node.getCord()
        
        curr_row = curr_cord[0]
        curr_col = curr_cord[1]
        cost = curr_node.getCost() + 1
        
        if curr_cord == g:
            return short_tree
        
        up = curr_row-1
        down = curr_row + 1
        right = curr_col +1
        left = curr_col - 1
        
        if canMove(up, curr_col):
            
            temp_h = h_function(type_h, up, g_row, curr_col, g_col)
            new_node = Node(up, curr_col, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(short_heap, new_node)
            
        if canMove(down, curr_col):
            temp_h = h_function(type_h, down, g_row, curr_col, g_col)
            new_node = Node(down, curr_col, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(short_heap, new_node)
        
        if canMove(curr_row, right):
            temp_h = h_function(type_h, curr_row, g_row, right, g_col)
            new_node = Node(curr_row, right, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(short_heap, new_node)
            
        if canMove(curr_row, left):
            temp_h = h_function(type_h, curr_row, g_row, left, g_col)
            new_node = Node(curr_row, left, curr_node)
            new_node.setCost(cost)
            
            new_h = temp_h + cost
            new_node.setH(new_h)
            heapq.heappush(short_heap, new_node)
        
    return []


# the repeating A* algorithm
# for problem 7
# s: our starting node, not 'start' grid, but where A* starts
# g: the path towards the 'goal' grid (finalized grids)
# type_h: the target heuristic formula
def AStar(path, fringe_heap, s, g, type_h, wall_list, counter):

    # set goal coor
    g_row = g[0]
    g_col = g[1]

    # initialize the heap array
    #fringe_heap = []
    

    # init the start grid
    # Node class: __init__(self, row, col, parent)
    start_node = Node(s[0], s[1], Node)
    
    # h_function(h_formula, x_1, x_2, y_1, y_2)
    distance = h_function(type_h, s[0], g_row, s[1], g_col)

    # set heuristic value to start node
    start_node.setH(distance)

    # push starter node into heap
    heapq.heappush(fringe_heap, start_node)
    #heapq.heappush(visited, start_node)
    
    starting = 0
    
    wall_found = False
    
    temp_walls = []
    
    temp_visited = []

    while fringe_heap and wall_found== False:
        
        # start heap with pop smallest node
        # pop smallest (current) node from heap, to expand
        curr_node = heapq.heappop(fringe_heap)
        
        counter = counter + 1
        
        temp_visited.append(curr_node.getCord())

        #heapq.heappush(path, curr_node)
        
        # then record current node coordinate
        curr_cord = curr_node.getCord()
        curr_row = curr_cord[0]
        curr_col = curr_cord[1]
        
        #print('row: ', curr_row,' col: ', curr_col)
        
        #return
    
        # parent node
        parent_node = curr_node.getParent()

        # if not goal, check if moveable in direction
        # directions: up, down, right, left
        # if applicable create node with move_robot, push node into heap
        
        # direction cords
        up = curr_row - 1
        down = curr_row + 1
        
        right = curr_col + 1
        left = curr_col - 1
        
        # print(up, down, right,left)
        #return
        
        #temp_node = Node(s[0], s[1], Node)
        new_node = start_node
        
        # change wall_found in canmove, not return false
        # instead change the wall_found
        up_h = 9999
        down_h = 9999
        right_h = 9999
        left_h = 9999

        #used to count paths available
        no_path = 0
        
        # 0 is pass, 2 is out of maze, 1 is wall hit, 3 is visited grid, 4 is wall already visited
        #print('CHECKING UP')
        flag1 = inMaze(up, curr_col, wall_list, temp_visited)
        if flag1 != 2:
            up_h = h_function(type_h, up, g_row, curr_col, g_col)
        if flag1 == 4 or flag1 == 3 or flag1 == 2:
            # wall hit
            up_h = 9999
            #print('wall up_h', up_h)
        if flag1 != 0:
            no_path = no_path +1
            
        #print('CHECKING DOWN')
        flag2 = inMaze(down, curr_col, wall_list, temp_visited)
        if flag2 != 2:
            down_h = h_function(type_h, down, g_row, curr_col, g_col)
        if flag2 == 4 or flag2 == 3 or flag2 == 2:
            # wall hit
            down_h = 9999
            #print('wall down_h: ', down_h)
        if flag2 != 0:
            no_path = no_path +1
            
        #print('CHECKING Right')
        flag3 = inMaze(curr_row, right, wall_list, temp_visited)
        if flag3 != 2:
            right_h = h_function(type_h, curr_row, g_row, right, g_col)
        if flag3 == 4 or flag3 == 3 or flag3 == 2:
            # wall hit
            right_h = 9999
            #print('wall right_h: ', right_h)
        if flag3 != 0:
            no_path = no_path +1
            
        #print('CHECKING Left')
        flag4 = inMaze(curr_row, left, wall_list, temp_visited)
        if flag4 != 2:
            #print('False out of maze 4')
            left_h = h_function(type_h, curr_row, g_row, left, g_col)
        if flag4 == 4 or flag4 == 3 or flag4 == 2:
            # wall hit
            left_h = 9999
            #print('wall left_h: ', left_h)
        if flag4 != 0:
            no_path = no_path +1
        
        #no direction left
        if no_path == 4:
            #print('no direction left')
            
            temp_visited.pop()
            
            if parent_node == []:
                print( 'Maze Unsolvable.')
            try:
                temp_visited.append(parent_node.getCord())
                heapq.heappush(path, parent_node)
            except:
                print('Maze is not Solvable')
                return -99 , temp_walls, temp_visited
            
            #see no direction as a wall
            temp_walls.extend( curr_node.getCord() )
            
            # print('dead_end: ', temp_walls)
            # print('grid before dead_end: ', temp_visited)
            
            return len(path), temp_walls, temp_visited, counter
        
        direction_h = compare_h(up_h, down_h, right_h, left_h)
        
        
        # use that H_ value to move robot
        # if wall hit, then rerun Astar

        
        # up =1, down= 2, right = 3, left = 4
   
        # up
        #if direction_h == 1:
        if direction_h == up_h:   
            #inMaze(curr_x, up):
            
            #print('up')
            
            
            if wall_hit(flag1):
                #print('flag1')
                wall_found = True
                temp_walls.extend( [up, curr_col] )
                                
                # AStar(curr_node.getCord(), g, type_h, temp_walls)
                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(up, g_row, curr_col, g_col, curr_node, type_h)            
            
            temp_visited.append([up, curr_col])
            
            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            
            
            
        # down
        elif direction_h == down_h:
        
            # inMaze(curr_x, down):
                  
            #print('down')      
            
            if wall_hit(flag2):
                #print('flag2')
                wall_found = True
                temp_walls.extend( [down, curr_col] )
                
                #AStar(curr_node.getCord(), g, type_h)
                return len(path), temp_walls, temp_visited, counter

            new_node = move_robot(down, g_row, curr_col, g_col, curr_node, type_h)
            
            temp_visited.append([down, curr_col])

            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            
        
        # right
        elif direction_h == right_h:
            
            # inMaze(right, curr_y)
            
            #print('right')
            
            if wall_hit(flag3):
                #print('flag3')
                wall_found = True
                temp_walls.extend( [curr_row, right] )
                
                #AStar(curr_node.getCord(), g, type_h)
                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(curr_row, g_row, right, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, right])
            
            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)

       
        # left
        elif direction_h == left_h:
        
            # inMaze(left, curr_y):
                  
            #print('left')
            
            if wall_hit(flag4):
                #print('flag4')
                wall_found = True
                temp_walls.extend( [curr_row, left] )
                
                #AStar(curr_node.getCord(), g, type_h)
                
                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(curr_row, g_row, left, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, left])
            
            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
        
            
        
        if new_node.getCord() == g:
            #heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            #print('grid before goal cord: ', new_node.getCord())
            #print('goal reached')
            heapq.heappush(path, new_node)
            
            print('goal reached')
            
            return len(path), temp_walls, temp_visited, counter
            break
            
        if wall_found == True:
            print('wall coordinates: ', temp_walls)
            break
    
        
    # unreachable goal, return empty
    return -99, temp_walls, temp_visited, counter

#----------------------
# END A*
# try to use this as default
# problem 6 Astar with line of view
# can see if it is block grid as neighbors, no need to hit
# -------------------------------
def six_AStar(path, fringe_heap, s, g, type_h, wall_list, counter):

    # set goal coor
    g_row = g[0]
    g_col = g[1]

    # initialize the heap array
    #fringe_heap = []
    

    # init the start grid
    # Node class: __init__(self, row, col, parent)
    start_node = Node(s[0], s[1], Node)
    
    # h_function(h_formula, x_1, x_2, y_1, y_2)
    distance = h_function(type_h, s[0], g_row, s[1], g_col)

    # set heuristic value to start node
    start_node.setH(distance)

    # push starter node into heap
    heapq.heappush(fringe_heap, start_node)
    #heapq.heappush(visited, start_node)
    
    wall_met = False
    
    temp_walls = []
    
    temp_visited = []
    
    #print('len of path: ', len(path))
    
    #temp_nodes = path

    #while wall_found == False:
    while fringe_heap and wall_met == False:
        # start heap with pop smallest node
        # pop smallest (current) node from heap, to expand
        curr_node = heapq.heappop(fringe_heap)
        
        counter = counter + 1
        
        temp_visited.append(curr_node.getCord())
        
        #heapq.heappush(path, curr_node)

        # then record current node coordinate
        curr_cord = curr_node.getCord()
        curr_row = curr_cord[0]
        curr_col = curr_cord[1]
        
        #print('row: ', curr_row,' col: ', curr_col)
        
        #return
    
        # parent node
        parent_node = curr_node.getParent()

        # if not goal, check if moveable in direction
        # directions: up, down, right, left
        # if applicable create node with move_robot, push node into heap
        
        # direction cords
        up = curr_row - 1
        down = curr_row + 1
        
        right = curr_col + 1
        left = curr_col - 1
        
        # print(up, down, right,left)
        #return
        
        #temp_node = Node(s[0], s[1], Node)
        new_node = start_node
        
        # change wall_found in canmove, not return false
        # instead change the wall_found
        up_h = 9999
        down_h = 9999
        right_h = 9999
        left_h = 9999

        #used to count paths available
        no_path = 0
        
        # 0 is pass, 2 is out of maze, 1 is wall hit (not applied), 3 is visited grid, 4 is wall already visited
        #print('CHECKING UP')
        flag1 = sixMaze(up, curr_col, wall_list, temp_walls, temp_visited)
        if flag1 != 2:
            up_h = h_function(type_h, up, g_row, curr_col, g_col)
        
        # we do not wait for the agent to hit the wall
        # due to the field of sight, we can extend the wall to temp_walls
        if flag1 == 1:
            temp_walls.append([up, curr_col])
            #flag1 = 4
        
        if flag1 == 4 or flag1 == 3 or flag1 == 2:
            # wall hit
            up_h = 9999
            no_path = no_path+1
            
            
        #print('CHECKING DOWN')
        flag2 = sixMaze(down, curr_col, wall_list, temp_walls, temp_visited)
        if flag2 != 2:
            down_h = h_function(type_h, down, g_row, curr_col, g_col)
            
        if flag2 == 1:
            temp_walls.append([down, curr_col])
            #flag2 =4 
                
        if flag2 == 4 or flag2 == 3 or flag2 == 2:
            # wall hit
            down_h = 9999
            no_path = no_path + 1
            
            
            
        #print('CHECKING Right')
        flag3 = sixMaze(curr_row, right, wall_list, temp_walls, temp_visited)
        if flag3 != 2:
            right_h = h_function(type_h, curr_row, g_row, right, g_col)
        if flag3 == 1:
            temp_walls.append([curr_row, right])
            #flag3 = 4
                
        if flag3 == 4 or flag3 == 3 or flag3 == 2:
            # wall hit
            right_h = 9999
            no_path = no_path +1
            
            
        #print('CHECKING Left')
        flag4 = sixMaze(curr_row, left, wall_list, temp_walls, temp_visited)
        if flag4 != 2:
            left_h = h_function(type_h, curr_row, g_row, left, g_col)
            
        if flag4 == 1:
            temp_walls.append([curr_row, left])
                
        if flag4 == 4 or flag4 == 3 or flag4 == 2:
            # wall hit
            left_h = 9999
            no_path = no_path +1
        

        #no direction left
        if no_path == 4:
            #print('no direction left')
            #print('curr_cord: ', curr_node.getCord())
            
            # do not need this, only for no-sight
            #temp_visited.pop()
            
            if parent_node == []:
                print( 'Maze Unsolvable.')
            try:
                #print('previous node: ', temp_visited[-1])
                temp_visited.append(parent_node.getCord())
                heapq.heappush(path, parent_node)
                #print('last node: ', temp_visited[-1])
            except:
                print('Maze is not Solvable')
                return -99 , temp_walls, temp_visited
            
            #see no direction as a wall
            #if temp_walls != []:
            temp_walls.append( curr_node.getCord() )
            #print('first new_wall: ', temp_walls)

            
            return len(path), temp_walls, temp_visited, counter
        
        direction_h = compare_h(up_h, down_h, right_h, left_h)
        
        
        # if wall blocking path, re-plan
        # up
        #if direction_h == 1:
        if direction_h == up_h:   
            #inMaze(curr_x, up):
            
            # hit the block on current iteration
            if wall_hit(flag1):
                
                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(up, g_row, curr_col, g_col, curr_node, type_h)            
            
            temp_visited.append([up, curr_col])
            
            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            
            
            
        # down
        elif direction_h == down_h:
        
            # inMaze(curr_x, down):
            
            if wall_hit(flag2):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter

            new_node = move_robot(down, g_row, curr_col, g_col, curr_node, type_h)
            
            temp_visited.append([down, curr_col])

            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            
        
        # right
        elif direction_h == right_h:
            
            if wall_hit(flag3):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(curr_row, g_row, right, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, right])
            
            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)

       
        # left
        elif direction_h == left_h:
        
            if wall_hit(flag4):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(curr_row, g_row, left, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, left])
            
            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
        
            
        
        if new_node.getCord() == g:
            #heapq.heappush(temp_nodes, new_node)
            #heapq.heappush(visited, new_node)
            
            heapq.heappush(path, new_node)
            
            #print('grid before goal cord: ', new_node.getCord())
            print('goal reached')
            return len(path), temp_walls, temp_visited, counter
            break
            
        if wall_met == True:
            print('wall coordinates: ', temp_walls)
            break
        
    # unreachable goal, return empty
    return -99, temp_walls, temp_visited, counter



#-------------------
#

#Weighted Astar
#-----------------------
def w_AStar(path, fringe_heap, s, g, type_h, wall_list, counter):
    
    w = 1.5

    # set goal coor
    g_row = g[0]
    g_col = g[1]

    # initialize the heap array
    #fringe_heap = []
    

    # init the start grid
    # Node class: __init__(self, row, col, parent)
    start_node = Node(s[0], s[1], Node)
    
    # h_function(h_formula, x_1, x_2, y_1, y_2)
    distance = h_function(type_h, s[0], g_row, s[1], g_col)

    # set heuristic value to start node
    start_node.setH(distance)

    # push starter node into heap
    heapq.heappush(fringe_heap, start_node)
    #heapq.heappush(visited, start_node)
    
    wall_met = False
    
    temp_walls = []
    
    temp_visited = []
    
    #print('len of path: ', len(path))
    
    #temp_nodes = path

    #while wall_found == False:
    while fringe_heap and wall_met == False:
        # start heap with pop smallest node
        # pop smallest (current) node from heap, to expand
        curr_node = heapq.heappop(fringe_heap)
        
        counter = counter + 1
        
        temp_visited.append(curr_node.getCord())
        
        # heapq.heappush(path, curr_node)

        # then record current node coordinate
        curr_cord = curr_node.getCord()
        curr_row = curr_cord[0]
        curr_col = curr_cord[1]
        
        #print('row: ', curr_row,' col: ', curr_col)
        
        #return
    
        # parent node
        parent_node = curr_node.getParent()

        # if not goal, check if moveable in direction
        # directions: up, down, right, left
        # if applicable create node with move_robot, push node into heap
        
        # direction cords
        up = curr_row - 1
        down = curr_row + 1
        
        right = curr_col + 1
        left = curr_col - 1
        
        # print(up, down, right,left)
        #return
        
        #temp_node = Node(s[0], s[1], Node)
        new_node = start_node
        
        # change wall_found in canmove, not return false
        # instead change the wall_found
        up_h = 9999
        down_h = 9999
        right_h = 9999
        left_h = 9999

        #used to count paths available
        no_path = 0
        
        # 0 is pass, 2 is out of maze, 1 is wall hit (not applied), 3 is visited grid, 4 is wall already visited
        #print('CHECKING UP')
        flag1 = sixMaze(up, curr_col, wall_list, temp_walls, temp_visited)
        if flag1 != 2:
            up_h = w * h_function(type_h, up, g_row, curr_col, g_col)
        
        # we do not wait for the agent to hit the wall
        # due to the field of sight, we can extend the wall to temp_walls
        if flag1 == 1:
            temp_walls.append([up, curr_col])
            #flag1 = 4
        
        if flag1 == 4 or flag1 == 3 or flag1 == 2:
            # wall hit
            up_h = 9999
            no_path = no_path+1
            
            
        #print('CHECKING DOWN')
        flag2 = sixMaze(down, curr_col, wall_list, temp_walls, temp_visited)
        if flag2 != 2:
            down_h = w *  h_function(type_h, down, g_row, curr_col, g_col)
            
        if flag2 == 1:
            temp_walls.append([down, curr_col])
            #flag2 =4 
                
        if flag2 == 4 or flag2 == 3 or flag2 == 2:
            # wall hit
            down_h = 9999
            no_path = no_path + 1
            
            
            
        #print('CHECKING Right')
        flag3 = sixMaze(curr_row, right, wall_list, temp_walls, temp_visited)
        if flag3 != 2:
            right_h = w *  h_function(type_h, curr_row, g_row, right, g_col)
        if flag3 == 1:
            temp_walls.append([curr_row, right])
            #flag3 = 4
                
        if flag3 == 4 or flag3 == 3 or flag3 == 2:
            # wall hit
            right_h = 9999
            no_path = no_path +1
            
            
        #print('CHECKING Left')
        flag4 = sixMaze(curr_row, left, wall_list, temp_walls, temp_visited)
        if flag4 != 2:
            left_h = w *  h_function(type_h, curr_row, g_row, left, g_col)
            
        if flag4 == 1:
            temp_walls.append([curr_row, left])
                
        if flag4 == 4 or flag4 == 3 or flag4 == 2:
            # wall hit
            left_h = 9999
            no_path = no_path +1
        

        #no direction left
        if no_path == 4:
            #print('no direction left')
            #print('curr_cord: ', curr_node.getCord())
            
            # do not need this, only for no-sight
            #temp_visited.pop()
            
            if parent_node == []:
                print( 'Maze Unsolvable.')
            try:
                #print('previous node: ', temp_visited[-1])
                temp_visited.append(parent_node.getCord())
                heapq.heappush(path, parent_node)
                #print('last node: ', temp_visited[-1])
            except:
                print('Maze is not Solvable')
                return -99 , temp_walls, temp_visited
            
            #see no direction as a wall
            #if temp_walls != []:
            temp_walls.append( curr_node.getCord() )
            #print('first new_wall: ', temp_walls)

            
            return len(path), temp_walls, temp_visited, counter
        
        direction_h = compare_h(up_h, down_h, right_h, left_h)
        
        
        # if wall blocking path, re-plan
        # up
        #if direction_h == 1:
        if direction_h == up_h:   
            #inMaze(curr_x, up):
            
            # hit the block on current iteration
            if wall_hit(flag1):
                
                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(up, g_row, curr_col, g_col, curr_node, type_h)            
            
            temp_visited.append([up, curr_col])
            
            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            
            
            
        # down
        elif direction_h == down_h:
        
            # inMaze(curr_x, down):
            
            if wall_hit(flag2):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter

            new_node = move_robot(down, g_row, curr_col, g_col, curr_node, type_h)
            
            temp_visited.append([down, curr_col])

            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            
        
        # right
        elif direction_h == right_h:
            
            if wall_hit(flag3):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(curr_row, g_row, right, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, right])
            
            #print('new cord: ', new_node.getCord())
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)

       
        # left
        elif direction_h == left_h:
        
            if wall_hit(flag4):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(curr_row, g_row, left, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, left])
            
            #print('new cord: ', new_node.getCord())
            
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
        
            
        
        if new_node.getCord() == g:
            #heapq.heappush(temp_nodes, new_node)
            #heapq.heappush(visited, new_node)
            
            
            heapq.heappush(path, new_node)
            
            #print('grid before goal cord: ', new_node.getCord())
            print('goal reached')
            return len(path), temp_walls, temp_visited, counter
            break
            
        if wall_met == True:
            print('wall coordinates: ', temp_walls)
            break
        
    # unreachable goal, return empty
    return -99, temp_walls, temp_visited, counter




#-----------------------
#

# improved Astar
#
#-------------------
def improve_AStar(path, fringe_heap, s, g, type_h, wall_list, counter):
    # set goal coor
    g_row = g[0]
    g_col = g[1]

    # initialize the heap array
    #fringe_heap = []
    

    # init the start grid
    # Node class: __init__(self, row, col, parent)
    start_node = Node(s[0], s[1], Node)
    
    # h_function(h_formula, x_1, x_2, y_1, y_2)
    distance = h_function(type_h, s[0], g_row, s[1], g_col)

    # set heuristic value to start node
    start_node.setH(distance)

    # push starter node into heap
    heapq.heappush(fringe_heap, start_node)
    #heapq.heappush(visited, start_node)
    
    wall_met = False
    
    temp_walls = []
    
    temp_visited = []

    #while wall_found == False:
    while fringe_heap and wall_met == False:
        # start heap with pop smallest node
        # pop smallest (current) node from heap, to expand
        curr_node = heapq.heappop(fringe_heap)
        
        counter = counter + 1
        
        temp_visited.append(curr_node.getCord())
        
        # heapq.heappush(path, curr_node)

        # then record current node coordinate
        curr_cord = curr_node.getCord()
        curr_row = curr_cord[0]
        curr_col = curr_cord[1]
        
        #print('row: ', curr_row,' col: ', curr_col)
        
        #return
    
        # parent node
        parent_node = curr_node.getParent()

        # if not goal, check if moveable in direction
        # directions: up, down, right, left
        # if applicable create node with move_robot, push node into heap
        
        # direction cords
        up = curr_row - 1
        down = curr_row + 1
        
        right = curr_col + 1
        left = curr_col - 1
        
        # print(up, down, right,left)
        #return
        
        #temp_node = Node(s[0], s[1], Node)
        new_node = start_node
        
        # change wall_found in canmove, not return false
        # instead change the wall_found
        up_h = 9999
        down_h = 9999
        right_h = 9999
        left_h = 9999

        #used to count paths available
        no_path = 0
        
        # 0 is pass, 2 is out of maze, 1 is wall hit (not applied), 3 is visited grid, 4 is wall already visited
        #print('CHECKING UP')
        flag1 = sixMaze(up, curr_col, wall_list, temp_walls, temp_visited)
        if flag1 != 2:
            up_h = h_function(type_h, up, g_row, curr_col, g_col)
        
        # we do not wait for the agent to hit the wall
        # due to the field of sight, we can extend the wall to temp_walls
        if flag1 == 1:
            temp_walls.append([up, curr_col])
            #flag1 = 4
        
        if flag1 == 4 or flag1 == 3 or flag1 == 2:
            # wall hit
            up_h = 9999
            no_path = no_path+1
            
            
        #print('CHECKING DOWN')
        flag2 = sixMaze(down, curr_col, wall_list, temp_walls, temp_visited)
        if flag2 != 2:
            down_h = h_function(type_h, down, g_row, curr_col, g_col)
            
        if flag2 == 1:
            temp_walls.append([down, curr_col])
            #flag2 =4 
                
        if flag2 == 4 or flag2 == 3 or flag2 == 2:
            # wall hit
            down_h = 9999
            no_path = no_path + 1
            
            
            
        #print('CHECKING Right')
        flag3 = sixMaze(curr_row, right, wall_list, temp_walls, temp_visited)
        if flag3 != 2:
            right_h = h_function(type_h, curr_row, g_row, right, g_col)
        if flag3 == 1:
            temp_walls.append([curr_row, right])
            #flag3 = 4
                
        if flag3 == 4 or flag3 == 3 or flag3 == 2:
            # wall hit
            right_h = 9999
            no_path = no_path +1
            
            
        #print('CHECKING Left')
        flag4 = sixMaze(curr_row, left, wall_list, temp_walls, temp_visited)
        if flag4 != 2:
            left_h = h_function(type_h, curr_row, g_row, left, g_col)
            
        if flag4 == 1:
            temp_walls.append([curr_row, left])
                
        if flag4 == 4 or flag4 == 3 or flag4 == 2:
            # wall hit
            left_h = 9999
            no_path = no_path +1
        

        #no direction left
        if no_path == 4:
            #print('no direction left')
            
            # we will iteration out of the hall
            # the hallway would have three direction unavailable
            # for each move back, make previous grid a wall
            
            # blockers include:
            # side with previous
            # wall block
            # border
            
            # use up,down,right,left to iterate
            
            dead_node = curr_node
            
            dead_cord = curr_node.getCord()
            
            # 1=up, 2= down, 3=right, 4= left, 5= more than one avail
            moveable = 0
            
            dead_list = [[dead_cord]]

            while  moveable != 5:
                
                #print('checking hall entered')
                #print('dead_cord: ', dead_cord)
                
                #print('temp_walls: ', temp_walls)
                
                dead_row = dead_cord[0]
                dead_col = dead_cord[1]
                
                moveable = 0
            
                #dead_list = [[dead_row, dead_col]]
            
            
                dead_up = dead_row - 1
                dead_down = dead_row + 1
                
                dead_right = dead_col + 1
                dead_left = dead_col - 1
                
                if improve_move(dead_up, dead_col, dead_list):
                    moveable = 1
                    
                if improve_move(dead_down, dead_col, dead_list):
                    if moveable != 0:
                        moveable = 5
                    else:
                        moveable = 2
                if improve_move(dead_row, dead_right, dead_list):
                    if moveable != 0:
                        moveable = 5
                    else:
                        moveable = 3
                if improve_move(dead_row, dead_left, dead_list):
                    if moveable != 0:
                        moveable = 5
                    else:
                        moveable = 4
                
                # no direction available
                if moveable == 0:
                    #print('stuck with no path')
                    return -99 , temp_walls, temp_visited
                    #return len(path), temp_walls, temp_visited
                
                # out of hall, stop while loop and return
                elif moveable == 5:
                    #print('out of hallway')
                    
                    return len(path), temp_walls, temp_visited, grid_counter
                
                #still in hall
                # extend wall
                else:
                    if moveable == 1:
                        temp_walls.append([dead_row, dead_col])
                        
                        dead_list.append([dead_row, dead_col])
                        temp_visited.append([dead_row, dead_col])
                        
                        heapq.heappush(path, dead_node)
                        
                        dead_cord = [dead_up, dead_col]
                    
                    elif moveable == 2:
                        temp_walls.append([dead_row, dead_col])
                        
                        dead_list.append([dead_row, dead_col])
                        temp_visited.append([dead_row, dead_col])
                        
                        heapq.heappush(path, dead_node)

                        dead_cord = [dead_down, dead_col]
                        
                    elif moveable == 3:
                        temp_walls.append([dead_row, dead_col])
                        
                        dead_list.append([dead_row, dead_col])
                        temp_visited.append([dead_row, dead_col])
                        
                        heapq.heappush(path, dead_node)
                        
                        dead_cord = [dead_row, dead_right]
                        
                    elif moveable == 4:
                        temp_walls.append([dead_row, dead_col])
       
                        dead_list.append([dead_row, dead_col])
                        temp_visited.append([dead_row, dead_col])
            
                        heapq.heappush(path, dead_node)
                        
                        dead_cord = [dead_row, dead_left]
                    
                    dead_node = dead_node.getParent()
                    
                    #print('temp_walls after move: ', temp_walls)
               
        
        direction_h = compare_h(up_h, down_h, right_h, left_h)
        
        
        # if wall blocking path, re-plan
        # up
        #if direction_h == 1:
        if direction_h == up_h:   
            #inMaze(curr_x, up):
            
            # hit the block on current iteration
            if wall_hit(flag1):
                
                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(up, g_row, curr_col, g_col, curr_node, type_h)            
            
            temp_visited.append([up, curr_col])
            
            #print('new cord: ', new_node.getCord())
            
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            
            
            
        # down
        elif direction_h == down_h:
        
            # inMaze(curr_x, down):
            
            if wall_hit(flag2):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter

            new_node = move_robot(down, g_row, curr_col, g_col, curr_node, type_h)
            
            temp_visited.append([down, curr_col])

            #print('new cord: ', new_node.getCord())
            
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            
        
        # right
        elif direction_h == right_h:
            
            if wall_hit(flag3):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(curr_row, g_row, right, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, right])
            
            #print('new cord: ', new_node.getCord())
            
            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)

       
        # left
        elif direction_h == left_h:
        
            if wall_hit(flag4):

                wall_met = True

                return len(path), temp_walls, temp_visited, counter
            
            new_node = move_robot(curr_row, g_row, left, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, left])
            
            #print('new cord: ', new_node.getCord())

            heapq.heappush(path, curr_node)
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
        
            
        
        if new_node.getCord() == g:
            #heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            #print('grid before goal cord: ', new_node.getCord())
            print('goal reached')
            heapq.heappush(path, new_node)
            
            return len(path), temp_walls, temp_visited, counter
            break
            
        if wall_met == True:
            print('wall coordinates: ', temp_walls)
            break
        
    # unreachable goal, return empty
    return -99, temp_walls, temp_visited, counter

#-------------------
# Astar End


# BFS START
#--------------------

def bfs(path, s, g, type_h, wall_list):
    
    
    
    
    
    
    return len(path), temp_walls, temp_visited

#--------------------
# BFS End

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

# visited wall coords
wall_list = []

runnable = True


# for each run, make a new copy of maze
# new additions of path node will be added
while runnable:
    maze_copy = [x[:] for x in maze]

    #used for know all walls in maze
    # for shortest path in Maze
    all_maze_copy = [x[:] for x in maze_copy]
    
    window = display_maze(maze_copy)
    
    #window3 = display_maze(all_maze_copy)
    
    # set up the heuristic formula
    
    right_input = 1
    
    while right_input != 0:
        print('Please choose a heuristic formula: E/M/C')
        print('Euclidean (E), Manhattan (M), Chebyshev (C)')
        type_h = input()
        
        if type_h == 'E' or type_h == 'M' or type_h == 'C':
            right_input = 0
        
        if right_input != 0:
            print('Wrong input, try again...')

    # do not forget the mainloop at end
    window.destroy()
    
    right_input = 1
    
    type_s = 'C'   
    while right_input != 0:
        print('Please choose a type Astar')
        print('Astar(A), Improved Astar(I), No Sight (S), Weighted Astar(W), BFS(B)')
        type_s = input()
        
        if type_s == 'B' or type_s == 'A' or type_s == 'I' or type_s == 'S' or type_s == 'W':
            right_input = 0
        
        if right_input != 0:
            print('Wrong input, try again...')
    
    if type_s == 'B':
        
        print('unfinished')
        runnable = False
    
    
    elif type_s == 'S':
        
        time_a = time.time()
        
        temp_wall = []

        #all grids visited
        temp_visited = []
        
        path = []
        
        fringe_heap = []
        
        visited_list= [[0,0]]
        
        visited_list1 = [[0,0]]

        passed = 0
        
        path_len = 0

        counter = 0
        
        grid_counter = 0
        
        #if first attempt is not compelted
        while visited_list[-1] != g_grid and runnable == True:

            path_len, temp_wall, temp_visited, grid_counter = AStar(path, fringe_heap, visited_list[-1], g_grid, type_h, wall_list, grid_counter)
            
            if path_len < 0:
                runnable = False
                break

            visited_list.extend(temp_visited)
            
            visited_list1.extend(temp_visited)

            #print('temp wall 1: ', temp_wall)

            #if (temp_wall in wall_list) == False:

                #print('extend in while loop 1')
                
            wall_list.append( temp_wall )

            #print('wall list next to start: ', wall_list)

            # goal cords not reached

            #print('checking if path reached goal')
            

            
            if g_grid in visited_list:
                
                # maze is runnable

                total_time = time.time() - time_a

                final_path = visited_list

                #print('final_path length: ', len(final_path))
                #print('final_path: ', final_path)
                #print("\n")

                #draw out the map, DO NOT INCLUDE MAP DRAWING IN TIME

                for i in range(len(final_path)):
                    curr_location = final_path[i]
                    # print('curr_location: ', curr_location)
                    maze_copy[curr_location[0]][curr_location[1]] = 'g'

                # make unvisited maze grids white
                colored = 0
                for x in range(len(maze_copy)):
                    for y in range(len(maze_copy[x])):

                        for i in range(len(final_path)):
                            curr_location = final_path[i]
                            if x == curr_location[0] and y == curr_location[1]:
                                maze_copy[x][y] = 'g'
                                colored = 1

                        if colored == 1:
                            colored = 0
                            continue

                        if maze_copy[x][y] != 'P':
                            maze_copy[x][y] = 'w'


                maze_copy[0][0] = 's'
                maze_copy[size-1][size-1] = 'g'

                print('Path to Goal found with repeat Astar. Grids traveled: ', path_len)
                print('Number of grids popped: ', grid_counter)
                print('Repeat Forward Astar: %s seconds used'% (total_time))
                print('\n')

                # NOW FOR BEST PATH IN PATH FOUND BY FORWARD ASTAR
                path_time = time.time()
                best_ppath = path_Astar(s_grid, g_grid, type_h, final_path)

                if best_ppath:

                    up = best_ppath[len(best_ppath)-1].getParent()
                    best_path = [up.getCord()]
                    best_path.append(up.getCord())
                    while up.getCord() != s_grid:
                        up = up.getParent()
                        best_path.append(up.getCord())

                best_path = best_path[::-1]

                for i in range(len(best_path)):
                    temp_cord = best_path[i]
                    maze_copy[temp_cord[0]][temp_cord[1]] = 'r'

                maze_copy[0][0] ='s'
                maze_copy[size-1][size-1] = 'r'

                print('Shortest path in info. from Astar: ', len(best_path))

                print('Shortest path in Astar: %s seconds used'% (time.time() - path_time))
                
                print('\n')

                window2 = display_maze(maze_copy)
                window2.mainloop()

                runnable = False
                passed = 1
                break
                
            if counter > 999:
                runnable = False
                break
                
            counter = counter + 1
        
        if runnable == False and passed == 0:
            #runnable = False
            print('No path to Goal.')
            #print('visited_list: ', visited_list)

    
    elif type_s == 'I':
        
        time_a = time.time()
        
        temp_wall = []

        #all grids visited
        temp_visited = []
        
        fringe_heap = []
        
        visited_list= [[0,0]]
        
        visited_list1 = [[0,0]]

        path = []

        passed = 0
        
        counter = 0
        
        grid_counter = 0

        #if first attempt is not compelted
        while visited_list[-1] != g_grid and runnable == True:

            path_len, temp_wall, temp_visited, grid_counter = improve_AStar(path, fringe_heap, visited_list[-1], g_grid, type_h, wall_list, grid_counter)

            if path_len < 0:
                runnable = False
                break
            
            visited_list.extend(temp_visited)
            
            visited_list1.extend(temp_visited)

            #print('temp wall 1: ', temp_wall)

            #if (temp_wall in wall_list) == False:

                #print('extend in while loop 1')
            wall_list.extend( temp_wall )

           
            if g_grid in visited_list:
                # path not empty but not at goal
                
                total_time = time.time() - time_a

                # draw map
                final_path = visited_list

                #print('final_path length: ', len(final_path))
                #print('final_path: ', final_path)
                #print("\n")

                for i in range(len(final_path)):
                    curr_location = final_path[i]
                    # print('curr_location: ', curr_location)
                    maze_copy[curr_location[0]][curr_location[1]] = 'g'

                # make unvisited maze grids white
                colored = 0
                for x in range(len(maze_copy)):
                    for y in range(len(maze_copy[x])):

                        for i in range(len(final_path)):
                            curr_location = final_path[i]
                            if x == curr_location[0] and y == curr_location[1]:
                                maze_copy[x][y] = 'g'
                                colored = 1

                        if colored == 1:
                            colored = 0
                            continue

                        if maze_copy[x][y] != 'P':
                            maze_copy[x][y] = 'w'


                maze_copy[0][0] = 's'
                maze_copy[size-1][size-1] = 'g'

                print('Path to Goal found with repeat Astar. Grids traveled: ',path_len)
                print('Number of grids popped: ', grid_counter)
                print('Repeat Forward Astar: %s seconds used'% (total_time))
                print('\n')

                # NOW FOR BEST PATH IN PATH FOUND BY FORWARD ASTAR
                path_time = time.time()
                best_ppath = path_Astar(s_grid, g_grid, type_h, final_path)

                if best_ppath:

                    up = best_ppath[len(best_ppath)-1].getParent()
                    best_path = [up.getCord()]
                    best_path.append(up.getCord())
                    while up.getCord() != s_grid:
                        up = up.getParent()
                        best_path.append(up.getCord())

                best_path = best_path[::-1]

                for i in range(len(best_path)):
                    temp_cord = best_path[i]
                    maze_copy[temp_cord[0]][temp_cord[1]] = 'r'

                maze_copy[0][0] ='s'
                maze_copy[size-1][size-1] = 'r'

                print('Shortest path with info from Astar: ', len(best_path))

                print('Shortest path in Astar: %s seconds used'% (time.time() - path_time))
                print('\n')
                window2 = display_maze(maze_copy)
                window2.mainloop()

                runnable = False
                passed = 1
                break
            
            
            if counter > 999:
                runnable = False
                break
                
            counter = counter + 1
            

        if runnable == False and passed == 0:
            #runnable = False
            print('No path to Goal.')
            #print('visited_list: ', visited_list)

    
    elif type_s == 'A':
        
        time_a = time.time()
        
        temp_wall = []

        path = []
        
        #all grids visited
        temp_visited = []
        
        visited_list= [[0,0]]
        
        visited_list1 = [[0,0]]

        fringe_heap = []

        passed = 0
        
        counter = 0
        
        grid_counter = 0

        #if first attempt is not compelted
        while g_grid not in visited_list and runnable == True:


            #if len(wall_list) == 0:

            path_len, temp_wall, temp_visited, grid_counter = six_AStar(path, fringe_heap, visited_list[-1], g_grid, type_h, wall_list, grid_counter)

            if path_len < 0:
                runnable = False
                break
            
            #for i in range(len(path)):
             #   print('2 path cord: ', path[i].getCord())
            
            visited_list.extend(temp_visited)
            
            visited_list1.extend(temp_visited)

            wall_list.extend( temp_wall )

             
            #print('STARTING ASTAR LOOP FROM: ', visited_list[-1])

            #print('LOOPS WALL_LIST: ', wall_list)

            if g_grid in visited_list:
                total_time = time.time() - time_a

                # draw map
                final_path = visited_list
                
                #for i in range(len(path)):
                 #   print('path: ', path[i].getCord())


                #print('final_path length: ', len(final_path))
                #print('final_path: ', final_path)
                #print("\n")

                for i in range(len(final_path)):
                    curr_location = final_path[i]
                    # print('curr_location: ', curr_location)
                    maze_copy[curr_location[0]][curr_location[1]] = 'g'

                # make unvisited maze grids white
                colored = 0
                for x in range(len(maze_copy)):
                    for y in range(len(maze_copy[x])):

                        for i in range(len(final_path)):
                            curr_location = final_path[i]
                            if x == curr_location[0] and y == curr_location[1]:
                                maze_copy[x][y] = 'g'
                                colored = 1

                        if colored == 1:
                            colored = 0
                            continue

                        if maze_copy[x][y] != 'P':
                            maze_copy[x][y] = 'w'


                maze_copy[0][0] = 's'
                maze_copy[size-1][size-1] = 'g'

                print('Path to Goal found with repeat Astar. Grids traveled: ', path_len)
                print('Number of grids popped: ', grid_counter)
                print('Repeat Forward Astar: %s seconds used'% (total_time))
                print('\n')
                
                # NOW FOR BEST PATH IN PATH FOUND BY FORWARD ASTAR
                path_time = time.time()
                best_ppath = path_Astar(s_grid, g_grid, type_h, final_path)

                if best_ppath:

                    up = best_ppath[len(best_ppath)-1].getParent()
                    best_path = [up.getCord()]
                    best_path.append(up.getCord())
                    while up.getCord() != s_grid:
                        up = up.getParent()
                        best_path.append(up.getCord())

                best_path = best_path[::-1]

                for i in range(len(best_path)):
                    temp_cord = best_path[i]
                    maze_copy[temp_cord[0]][temp_cord[1]] = 'r'

                maze_copy[0][0] ='s'
                maze_copy[size-1][size-1] = 'r'

                print('Shortest path in info from Astar: ', len(best_path))

                print('Shortest path in Astar: %s seconds used'% (time.time() - path_time))
                print('\n')
                
                window2 = display_maze(maze_copy)
                window2.mainloop()

                runnable = False
                passed = 1
                
                break
            
            if counter > 999:
                runnable = False
                break
                
            counter = counter + 1


        if runnable == False and passed == 0:
            #runnable = False
            print('No path to Goal.')
            #print('visited_list: ', visited_list)
            
        
    elif type_s == 'W':
        
        time_a = time.time()
        
        temp_wall = []

        path = []
        
        fringe_heap = []
        
        #all grids visited
        temp_visited = []
        visited_list= [[0,0]]
        
        visited_list1 = [[0,0]]

        passed = 0
        
        counter = 0
        
        grid_counter = 0

        #if first attempt is not compelted
        while visited_list[-1] != g_grid and runnable == True:


            #if len(wall_list) == 0:

            path_len, temp_wall, temp_visited, grid_counter = w_AStar(path, fringe_heap, visited_list[-1], g_grid, type_h, wall_list, grid_counter)

            if path_len < 0:
                runnable = False
                break

            #for i in range(len(path)):
             #   print('2 path cord: ', path[i].getCord())
            
            visited_list.extend(temp_visited)

            visited_list1.extend(temp_visited)
            
            wall_list.extend( temp_wall )

             
            #print('STARTING ASTAR LOOP FROM: ', visited_list[-1])

            #print('LOOPS WALL_LIST: ', wall_list)

            if g_grid in visited_list:
                total_time = time.time() - time_a

                # draw map
                final_path = visited_list

                #for i in range(len(path)):
                 #   print(path[i].getCord())

                #print('final_path length: ', len(final_path))
                #print('final_path: ', final_path)
                #print("\n")

                for i in range(len(final_path)):
                    curr_location = final_path[i]
                    # print('curr_location: ', curr_location)
                    maze_copy[curr_location[0]][curr_location[1]] = 'g'

                # make unvisited maze grids white
                colored = 0
                for x in range(len(maze_copy)):
                    for y in range(len(maze_copy[x])):

                        for i in range(len(final_path)):
                            curr_location = final_path[i]
                            if x == curr_location[0] and y == curr_location[1]:
                                maze_copy[x][y] = 'g'
                                colored = 1

                        if colored == 1:
                            colored = 0
                            continue

                        if maze_copy[x][y] != 'P':
                            maze_copy[x][y] = 'w'


                maze_copy[0][0] = 's'
                maze_copy[size-1][size-1] = 'g'

                print('Path to Goal found with repeat Astar. Grids traveled: ', path_len)
                print('Number of grids popped : ', grid_counter)
                print('Repeat Forward Astar: %s seconds used'% (total_time))
                print('\n')
                # NOW FOR BEST PATH IN PATH FOUND BY FORWARD ASTAR
                path_time = time.time()
                best_ppath = path_Astar(s_grid, g_grid, type_h, final_path)

                if best_ppath:

                    up = best_ppath[len(best_ppath)-1].getParent()
                    best_path = [up.getCord()]
                    best_path.append(up.getCord())
                    while up.getCord() != s_grid:
                        up = up.getParent()
                        best_path.append(up.getCord())

                best_path = best_path[::-1]

                for i in range(len(best_path)):
                    temp_cord = best_path[i]
                    maze_copy[temp_cord[0]][temp_cord[1]] = 'r'

                maze_copy[0][0] ='s'
                maze_copy[size-1][size-1] = 'r'

                print('Shortest path with info from Astar: ', len(best_path))

                print('Shortest path in Astar: %s seconds used'% (time.time() - path_time))
                print('\n')
                
                window2 = display_maze(maze_copy)
                window2.mainloop()

                runnable = False
                passed = 1
                
                break
                
            
            if counter > 999:
                runnable = False
                break
                
            counter = counter + 1

    if passed == 1:

        # NOW FOR BEST PATH IN MAZE, WE KNOW ALL WALL LOCATIONS
        shortest_time = time.time()
        shortest_path = all_Astar(s_grid, g_grid, type_h)

        #print('shortest_path: ', shortest_path)

        if shortest_path:

            # some how we need to iterate the visited grids
            # else they become black grids (walls) or unknown reasons
            for i in range(len(shortest_path) - 1):
                holder= shortest_path[i].getCord()
                all_maze_copy[holder[0]][holder[1]] = 'w'

            short_up = shortest_path[len(shortest_path)-1].getParent()
            shortest = [short_up.getCord()]
            shortest.append(short_up.getCord())

            while short_up.getCord() != s_grid:

                short_up = short_up.getParent()
                #print('up: ', short_up.getCord())
                shortest.append(short_up.getCord())

            shortest = shortest[::-1]

            for i in range(len(shortest)):
                #print(shortest[i])

                short_cord = shortest[i]
                all_maze_copy[short_cord[0]][short_cord[1]] = 'b'

            maze_copy[0][0] ='s'
            all_maze_copy[size-1][size-1] = 'b'

            print('Shortest Path in Maze found brute force Astar. Grids traveled: ', len(shortest))
            print('Shortest path in Maze: %s seconds used'% (time.time() - shortest_time))


            window3 = display_maze(all_maze_copy)
            window3.mainloop()

            break


    if runnable == False and passed == 0:
        #runnable = False
        print('No path to Goal.')
        #print('visited_list: ', visited_list)

            


#--------------------
#run function end




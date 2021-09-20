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

# for repeated A* algorithm
# if start_node, ignore the wall beside it and continue running
# if wall_found False, we continue running A*
# if wall_found, we stop A*, backtrack what we have, and start again

# starter_node = True


# GLOBAL VARIABLE


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

    #temp_heap = fringe_heap
    
    result = 0
    
    #must be >= 0
    if  row< 0 or col < 0:
        #print(row, col, '<0')
        return 2

    #must be < size (not <=)
    if row >= size or col >= size:
        #print(row, col, '>= size')
        return 2

    #print('wall_list', wall_list)
    
    
    
    cord = [row,col]
    
    # check if it is wall
    #print('compare direction to wall list 1: ') 
    if cord == wall_list:
        
        #print('compare direction to wall list 2nd: ', cord, wall_list)
        #print('wall grid found in wall_list, skipping...')
        return 4
    
    
    for i in range(len( wall_list)):
        
        #print(i, 'turn', wall_list)
        
        if cord == wall_list[i]:
        
            #print('compare direction to wall list 2nd: ', cord, wall_list)
            #print('wall grid found in wall_list, skipping...')
            return 4
    
    #check if the path was visited by current iteration
    
    if cord == temp_visited:
        
        #print('compare direction to wall list 2nd: ', cord, wall_list)
        print('wall grid found in wall_list, skipping...')
        return 3
    
    
    for i in range(len( temp_visited)):
        
        if cord == temp_visited[i]:
        
            #print('This direction already visited in iteration: ', cord, temp_visited)
            #print('grid already visited in iteration, skipping...')
            return 3
    
    
    #check if wall, wall found then stop
    if maze_copy[row][col] == 'P':
        # wall_found = True
        # print('wall hit: ', row, ', ', col)
        return 1
        
        #not return False,
        # bot need to move into the wall in order to stop
        #return False

    # check if checking (visited but not finalized) grid
    # return visited three times
    #if maze_copy[row][col] == 'c':
     #   print('visited')
      #  return False  
    
    #check if good path as in final grid
    #if false then change to checking grid
    if maze_copy[row][col] != 'g':
        maze_copy[row][col] = 'c'

    #all check complete
    return 0


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
    new_cost = curr_node.getCost() + 1
    new_node.setCost(new_cost)

    # 2.2) set new h_value, store into node
    new_distance = h_function(h_type, curr_row, g_row, curr_col, g_col)
    new_h = new_cost + new_distance
    new_node.setH(new_h)
    
    # 3) return new_node
    return new_node


# the repeating A* algorithm
# s: our starting node, not 'start' grid, but where A* starts
# g: the path towards the 'goal' grid (finalized grids)
# type_h: the target heuristic formula
def AStar(s, g, type_h, wall_list):

    # set goal coor
    g_row = g[0]
    g_col = g[1]

    # initialize the heap array
    fringe_heap = []
    

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
    
    
    #print('start node: ', start_node.getCord())
    #print("\n")
    
    #return
    
    # reset wall_found each new Astar aglor
    # wall_found = False
    #starter_node = True
    
    starting = 0
    
    wall_found = False
    
    temp_walls = []
    
    temp_visited = []

    while wall_found == False:
        
        # start heap with pop smallest node
        # pop smallest (current) node from heap, to expand
        curr_node = heapq.heappop(fringe_heap)
        
        temp_visited.append(curr_node.getCord())
        
        #print('temp_visited: ', temp_visited)
        
        #print('current node:', curr_node.getCord(), curr_node.getH())
        
        #print("\n")
        
        #return 
    
        # append the current node to visited
        # visited.append(curr_node)

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

        # wall coords
        # wall_cord = []
        
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

        up_h = 99
        down_h = 99
        right_h = 99
        left_h = 99
        
        
        # use compare_h() to find least H_value
        # also check if still within maze
        
        
        
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
            
            temp_visited.append(parent_node.getCord())
            
            #see no direction as a wall
            temp_walls.extend( curr_node.getCord() )
            
            # print('dead_end: ', temp_walls)
            # print('grid before dead_end: ', temp_visited)
            
            return fringe_heap, temp_walls, temp_visited
        
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
                return fringe_heap, temp_walls, temp_visited
            
            new_node = move_robot(up, g_row, curr_col, g_col, curr_node, type_h)            
            
            temp_visited.append([up, curr_col])
            
            #print('new cord: ', new_node.getCord())
            
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
                return fringe_heap, temp_walls, temp_visited

            new_node = move_robot(down, g_row, curr_col, g_col, curr_node, type_h)
            
            temp_visited.append([down, curr_col])

            #print('new cord: ', new_node.getCord())
            
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
                return fringe_heap, temp_walls, temp_visited
            
            new_node = move_robot(curr_row, g_row, right, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, right])
            
            #print('new cord: ', new_node.getCord())
            
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
                
                return fringe_heap, temp_walls, temp_visited
            
            new_node = move_robot(curr_row, g_row, left, g_col, curr_node, type_h)
            
            temp_visited.append([curr_row, left])
            
            #print('new cord: ', new_node.getCord())

            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
        
            
        
        if new_node.getCord() == g:
            heapq.heappush(fringe_heap, new_node)
            #heapq.heappush(visited, new_node)
            #print('grid before goal cord: ', new_node.getCord())
            print('goal reached')
            return fringe_heap, temp_walls, temp_visited
            break
            
        if wall_found == True:
            print('wall coordinates: ', temp_walls)
            break
        
    # unreachable goal, return empty
    return fringe_heap, temp_walls, temp_visited

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

# visited wall coords
wall_list = []

runnable = True


# for each run, make a new copy of maze
# new additions of path node will be added
while runnable:
    maze_copy = [x[:] for x in maze]

    window = display_maze(maze_copy)
    
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
        
    #print('Choose Algorithm: BFS(B)/ A*(A)')
    #algorithm = input()

    # do not forget the mainloop at end
    window.destroy()
    
    #path = [s_grid]

    #while temp_grid != g_grid:
        # implementation of A* algor
        
    temp_wall = []
    
    #all grids visited
    temp_visited = []
    visited_list= []
    
    path, temp_wall, temp_visited = AStar(s_grid, g_grid, type_h, wall_list)
        #temp_grid = path

    wall_list.append( temp_wall )
    
    visited_list.extend(temp_visited)
    
    #print('extend once wall_list: ', temp_visited)
    #print(wall_list)
    
    #print('current wall list: ', wall_list)
    
    #print('first visited list: ', visited_list)
    
    #print('path: ', path)
    
    passed = 0
    
    #if first attempt is not compelted
    if path == []:
        
        
        if len(wall_list) == 0:
            
            path, temp_wall, temp_visited = AStar(visited_list[-1], g_grid, type_h, wall_list)
            
            for i in temp_visited:
                if (i in visited_list) == False:
                    visited_list.extend(temp_visited)

            #print('temp wall 1: ', temp_wall)

            if (temp_wall in wall_list) == False:

                #print('extend in while loop 1')
                wall_list.append( temp_wall )

            print('wall list next to start: ', wall_list)
            
            # goal cords not reached
        
            #print('checking if path reached goal')
    
            if wall_list == [[]]:
                print('Start surrounded by walls')
                runnable = False
                print('No path to Goal.')
                window2 = display_maze(maze_copy)
                window2.mainloop()
                passed = 1

                
        #wall_list.extend( temp_wall )
        if wall_list != [[]]:
            # path not empty but not at goal
            
            counter = 0
            #print('first last node: ', path[-1].getCord())
            
            while (visited_list[-1] != g_grid):
                
                #print('STARTING ASTAR LOOP FROM: ', visited_list[-1])
                
                #print('LOOPS WALL_LIST: ', wall_list)

                path, temp_wall, temp_visited  = AStar(visited_list[-1], g_grid, type_h, wall_list)
                
                for i in temp_visited:
                    #print('cord in temp_visited: ', i)
                    if (i in visited_list) == False:
                        visited_list.extend(temp_visited)
                    

                #print('temp wall 2: ', temp_wall)

               

                #print('extend in while loop 2')
                if (temp_wall in wall_list) == False:
                    wall_list.append( temp_wall )
                    
                print('wall_list: ', wall_list)
                
                counter = counter + 1
                
                if counter >= 999:
                    runnable= False
                    break
                
                
            if runnable == False:
                passed = 0
                #print('No path to Goal.')
                
            else:
                final_path = visited_list

                #print('final_path length: ', len(final_path))
                #print('final_path: ', final_path)
                print("\n")

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

                window2 = display_maze(maze_copy)
                window2.mainloop()
                print('Path to Goal found. Grids traveled: ')
                print(len(final_path))

                runnable = False
                passed = 1

    elif path and runnable == True:
        # path completed
        
        #start from goal grid
        up = path[len(path) - 1]
        final_path = [up.getCord()]

        while up.getCord() != s_grid:
            up = up.getParent()
            final_path.append(up.getCord())
        
        #reverse the path
        final_path = final_path[::-1]
        
        #print('final_path length: ', len(final_path))
        #print('final_path: ', final_path)
        #print("\n")
        
        
        for i in range(len(final_path)):
            curr_location = final_path[i]
            #print('curr_location: ', curr_location)
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

        window2 = display_maze(maze_copy)
        window2.mainloop()
        print('Path to Goal found. Grids traveled: ')
        print(len(final_path))
        runnable = False
        passed=1
        
    if runnable == False and passed == 0:
        #runnable = False
        print('No path to Goal.')
        print('visited_list: ', visited_list)
        final_path = visited_list
            
        #print('final_path length: ', len(final_path))
        #print('final_path: ', final_path)
        print("\n")

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

        window2 = display_maze(maze_copy)
        window2.mainloop()
        print('Path to Goal found. Grids traveled: ')
        print(len(final_path))


    


#--------------------
#run function end

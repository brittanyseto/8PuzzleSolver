#!/usr/bin/python
import math
import heapq

MAX_NODES = 5000000 

#Store board and info into nodes 
class puzzle(object):

    #initializer
    def __init__(self, state = None):
        self.state = state #current state of board
        self.length = 3 #num tiles in each row
        self.total_tiles = 9 #total tiles on board
        self.hs = None
        self.last_move = []
       
        #initial state
        if state is not None:     
            self.state = list(state)
        else:
            #generate goal state if state is null 
            self.state = [(x + 1) % 9 for x in range(self.total_tiles)]

    def __hash__(self):
        if self.hs is None:
            self.hs = hash(tuple(self.state))
        return self.hs

    #check if equal states
    def __eq__(self, other):
        return self.state == other.state
    
#Find the shortest path from START to goal.
def solve(start, goal, heuristic):
    pq = [] #heap to push into heapq
    h_values = [] #values generated by heuristics
    link = {} # parent node link
    h = {} # store heuristic in map
    g = {} #minimal path to goal state
    depth = 0 #increment by 1 each time a node is expanded 
    x = 0 # bool to see if "ucs"
    g[start] = 0 #initialize goal state to 0 
    q_size = 0; 
    q_max = 0
    
    #create heap (aka priority queue) to store nodes
    heapq.heappush(pq, (0, 0, start))
    q_size += 1

    #general search algorithm
    for i in range(MAX_NODES):
        
        #pop off first node 
        temp1, temp2, current = heapq.heappop(pq)
        q_size -= 1

        #check current state is goal state
        if current.state == goal.state:
            print_board(current.state)
            print "GOAL!"
            print "Max queue size= ", q_max
            return 

        print_board(current.state) 
        print "\nBest state to expand with a g(n) =", g[current]+1, "and",
        moves = possible_moves(current)
        depth = g[current]

        #look for min h in the possible moves 
        for j in moves:
            if j not in g or g[j] > depth + 1:
                g[j] = depth + 1
                if j not in h:
                    h[j] = heuristic(j, goal)
                    h_values.append(h[j])
                    if(heuristic == "ucs"):
                        x = 1
                link[j] = current
                heapq.heappush(pq, (g[j] + h[j], i, j))
                q_size += 1
        print "h(n) = ", min_h(h_values, x), "(expanded:", i, ")"
        h_values[:] = []
        if(q_size > q_max):
            q_max = q_size
        

def print_board(list_nodes): 
    temp = [] 
    j = 0
    for i in list_nodes: 
        if j > 2:
            print "\n",
            j = 0
        print i, 
        j += 1
    print "\n",

def min_h(h_list, x): 
    h_list.sort()
    for i in h_list:
        if i != 0 and x != 1:
            return i

def possible_moves(curr_state):
    temp = curr_state.state.index(0)

    #check left
    if temp % curr_state.length > 0:
        j = temp
        tmp = list(curr_state.state)
        last_move = tmp[temp-1]
        tmp[temp-1], tmp[j] = tmp[j], tmp[temp-1]
        result = puzzle(tmp)
        result.last_move = last_move
        yield result
    #check right
    if temp % curr_state.length < curr_state.length-1:
        j = temp
        tmp = list(curr_state.state)
        last_move = tmp[temp+1]
        tmp[temp+1], tmp[j] = tmp[j], tmp[temp+1]
        result = puzzle(tmp)
        result.last_move = last_move
        yield result
    #check up
    if temp - curr_state.length >= 0:
        j = temp
        tmp = list(curr_state.state)
        last_move = tmp[temp-curr_state.length]
        tmp[temp-curr_state.length], tmp[j] = tmp[j], tmp[temp-curr_state.length]
        result = puzzle(tmp)
        result.last_move = last_move
        yield result
    #check down
    if temp + curr_state.length < curr_state.total_tiles:
        j = temp
        tmp = list(curr_state.state)
        last_move = tmp[temp+curr_state.length]
        tmp[temp+curr_state.length], tmp[j] = tmp[j], tmp[temp+curr_state.length]
        result = puzzle(tmp)
        result.last_move = last_move
        yield result



# Uniform cost search
def ucs(curr_state, goal):
    return 0

# Returns the number of tiles misplaced.
def misplaced_tiles(curr_state, goal):    
    h = 0
    for i in range(curr_state.total_tiles):
        #check if tiles are in the right spot 
        if curr_state.state[i] != goal.state[i]:
            h += 1
    return h


# Returns manhattan distance
def manhattan_distance(curr_state, goal):
    h = 0
    f = 0
    s = [[0]*3 for i in range(3)]
    g = [[0]*3 for i in range(3)]

    s = make_matrix(curr_state)
    g = make_matrix(goal)

    #loop through to get indexes of misplaced tiles 
    for i in range(3): 
        for j in range(3):
            if s[i][j] != g[i][j]:
                x = get_index(s[i][j], g, "i")
                y = get_index(s[i][j], g, "j")
                h += abs(x - i) + abs(y - j)/2
    return h

def make_matrix(state):
    matrix = [[0]*3 for i in range(3)]
    cnt = 0

    for i in range(3):
        for j in range(3):
            matrix[i][j] = state.state[cnt]
            cnt += 1

    return matrix

def get_index(value, goal, x):
    for i in range(3): 
        for j in range(3): 
            if value == goal[i][j]:
                if x == "i":
                    return i
                if x == "j":
                    return j


###################### main ###########################

print "Welcome to Brittany's 8 puzzle solver!"
user_input1 = raw_input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle: ")

default = [1, 2, 3, 4, 0, 6, 7, 5, 8]
goal  = [1, 2, 3, 4, 5, 6, 7, 8, 0]
#temp = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']


if user_input1 == "1":
    board = puzzle(default);
elif user_input1 == "2":
    temp2 = []
    print "Enter values for \nA B C\nD E F\nG H I "
    user_input = input("Enter value for A: ")
    temp2.append(user_input)
    user_input = input("Enter value for B: ")
    temp2.append(user_input)
    user_input = input("Enter value for C: ")
    temp2.append(user_input)
    user_input = input("Enter value for D: ")
    temp2.append(user_input)
    user_input = input("Enter value for E: ")
    temp2.append(user_input)
    user_input = input("Enter value for F: ")
    temp2.append(user_input)
    user_input = input("Enter value for G: ")
    temp2.append(user_input)
    user_input = input("Enter value for H: ")
    temp2.append(user_input)
    user_input = input("Enter value for I: ")
    temp2.append(user_input)

    board = puzzle(temp2)

print "\n1. Uniform Cost Search"
print "2. A* with the Misplaced Tile Heuristic"
print "3. A* with the Manhattan distance heuristic \n"
user_input2 = raw_input("Enter your choice of algorithm: ")

if user_input2 == "1":
    print "Uniform Cost Search\n", 
    solve(board, puzzle(), ucs)
elif user_input2 == "2":
    print "A* with the Misplaced Tile Heuristic\n", 
    solve(board, puzzle(), misplaced_tiles)
elif user_input2 == "3":
    print "A* with the Manhattan distance heuristic\n", 
    solve(board, puzzle(), manhattan_distance)



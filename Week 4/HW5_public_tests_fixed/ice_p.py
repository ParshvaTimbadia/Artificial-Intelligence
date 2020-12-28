# "MDPs on Ice - Assignment 5"
# Ported from Java

import random
import numpy as np
import copy
import sys

GOLD_REWARD = 100.0
PIT_REWARD = -150.0
DISCOUNT_FACTOR = 0.5
EXPLORE_PROB = 0.2 # for Q-learning
LEARNING_RATE = 0.1
ITERATIONS = 10000
MAX_MOVES = 1000
ACTIONS = 4
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
MOVES = ['U','R','D','L']

# Fixed random number generator seed for result reproducibility --
# don't use a random number generator besides this to match sol
random.seed(5100)

# Problem class:  represents the physical space, transition probabilities, reward locations,
# and approach to use (MDP or Q) - in short, the info in the text file
class Problem:
    # Fields:
    # approach - string, "MDP" or "Q"
    # move_probs - list of doubles, probability of going 1,2,3 spaces
    # map - list of list of strings: "-" (safe, empty space), "G" (gold), "P" (pit)

    # Format looks like
    # MDP    [approach to be used]
    # 0.7 0.2 0.1   [probability of going 1, 2, 3 spaces]
    # - - - - - - P - - - -   [space-delimited map rows]
    # - - G - - - - - P - -   [G is gold, P is pit]
    #
    # You can assume the maps are rectangular, although this isn't enforced
    # by this constructor.

    # __init__ consumes stdin; don't call it after stdin is consumed or outside that context
    def __init__(self):
        self.approach = input('Reading mode...')
        print(self.approach)
        probs_string = input("Reading transition probabilities...\n")
        self.move_probs = [float(s) for s in probs_string.split()]
        self.map = []
        for line in sys.stdin:
            self.map.append(line.split())

    def solve(self, iterations):            
        if self.approach == "MDP":
            return mdp_solve(self, iterations)
        elif self.approach == "Q":
            return q_solve(self, iterations)
        return None
        
# Policy: Abstraction on the best action to perform in each state - just a 2D string list-of-lists
class Policy:
    def __init__(self, problem): # problem is a Problem
        # Signal 'no policy' by just displaying the map there
        self.best_actions = copy.deepcopy(problem.map)

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.best_actions])

# roll_steps:  helper for try_policy and q_solve -- "rolls the dice" for the ice and returns
# the new location (r,c), taking map bounds into account
# note that move is expecting a string, not an integer constant
def roll_steps(move_probs, row, col, move, rows, cols):
    displacement = 1
    total_prob = 0
    move_sample = random.random()
    for p, prob in enumerate(problem.move_probs):
        total_prob += prob
        if move_sample <= total_prob:
            displacement = p+1
            break
    # Handle "slipping" into edge of map
    new_row = row
    new_col = col
    if not isinstance(move,str):
        print("Warning: roll_steps wants str for move, got a different type")
    if move == "U":
        new_row -= displacement
        if new_row < 0:
            new_row = 0
    elif move == "R":
        new_col += displacement
        if new_col >= cols:
            new_col = cols-1
    elif move == "D":
        new_row += displacement
        if new_row >= rows:
            new_row = rows-1
    elif move == "L":
        new_col -= displacement
        if new_col < 0:
            new_col = 0
    return new_row, new_col


# try_policy:  returns avg utility per move of the policy, as measured by "iterations"
# random drops of an agent onto empty spaces, running until gold, pit, or time limit 
# MAX_MOVES is reached
def try_policy(policy, problem, iterations):
    total_utility = 0
    total_moves = 0
    for i in range(iterations):
        # Resample until we have an empty starting square
        while True:
            row = random.randrange(0,len(problem.map))
            col = random.randrange(0,len(problem.map[0]))
            if problem.map[row][col] == "-":
                break
        for moves in range(MAX_MOVES):
            total_moves += 1
            policy_rec = policy.best_actions[row][col]
            # Take the move - roll to see how far we go, bump into map edges as necessary
            row, col = roll_steps(problem.move_probs, row, col, policy_rec, len(problem.map), len(problem.map[0]))
            if problem.map[row][col] == "G":
                total_utility += GOLD_REWARD
                break
            if problem.map[row][col] == "P":
                total_utility += PIT_REWARD
                break
    return total_utility / total_moves



def ispossibletomove(rows,cols):
    list= []
   
    if (cols+1) < len(problem.map[0]):
        list.append("R")
    if (rows+1) < len(problem.map):
        list.append("D")
    if (cols-1) >= 0:
        list.append("L")    
    if (rows-1) >= 0:
        list.append("U")
    return list

def rewardMatrix():
    
    rewards = [[0 for j in range(len(problem.map[0]))] for i in range(len(problem.map))]
    
    i=0
    
    while i != len(problem.map):
        j=0       
        while j !=len(problem.map[0]):
            if problem.map[i][j]=='G':
                rewards[i][j]=GOLD_REWARD
            elif problem.map[i][j]=='P':
                rewards[i][j]=PIT_REWARD
            j+=1
        i+=1     
            
    return rewards

def lookuptable(i):
    
    dict={0:'U', 1:'R', 2:'D', 3:'L'}
    
    return dict[i]
    

# mdp_solve:  use [iterations] iterations of the Bellman equations over the whole map in [problem]
# and return the policy of what action to take in each square
def mdp_solve(problem, iterations):
    
    
  
   
    
    grid = copy.deepcopy(problem.map)
    reward=rewardMatrix() 
    print(reward)
    
    
    
            
        
   
    temp_utility= copy.deepcopy(V)
    
    
  
    gamma = problem.move_probs
    
    for iteration in range(ITERATIONS):
        
        
        for i in range(rows):
            for j in range(colums):
                
                if grid[i][j]=='P' or grid[i][j]=='G':
                    continue
                
            
                #We need to update the utility value in the utility grid, ie. V
                
                #We need to find the best action move max[a] from state s and update its 
                #action in the gird and its utility value in V.
                
                #For that we will iterate through all possible actions.
                S={}
                for m in MOVES:
                    
                    if m=='U':
                        
                    
                        S['U']=0
                        for slip,prob in enumerate(slip_probs):
                            current_i=i-(slip+1)
                            
                            if current_i<0:
                                current_i=0
                                
                              
                            S['U']+= DISCOUNT_FACTOR*(prob*temp_utility[current_i][j])
                            
                        
                    if m=='D':
                        
                     
                        
                        S['D']=0
                        for slip,prob in enumerate(slip_probs):
                            current_i=i+(slip+1)
                            
                            if current_i>=rows:
                                current_i=rows-1
                                
                           
                            S['D']+= DISCOUNT_FACTOR*(prob*temp_utility[current_i][j])
                            
                        
                        
                    if m=='R':
                        
                        
                        
                        S['R']=0
                        for slip,prob in enumerate(slip_probs):
                            current_j=j+(slip+1)
                            
                            if current_j>=colums-1:
                                current_j = colums - 1
                                
                           
                            S['R']+= DISCOUNT_FACTOR*(prob*temp_utility[i][current_j])
                            
                
                    if m=='L':
                        
                        
                        
                        S['L']=0
                        for slip,prob in enumerate(slip_probs):
                            current_j=j-(slip+1)
                            
                            if current_j <0:
                                current_j = 0
                            
                            
                            S['L']+= DISCOUNT_FACTOR*(prob*temp_utility[i][current_j])
                        
                # print("This S", S)       
                OPTIMAL= max(S, key = lambda x:S[x])
                val=S[OPTIMAL]
                temp_utility[i][j]=val
                grid[i][j]=OPTIMAL
        
        
                
    print("GRID after",iterations,"iterations:")
    print(grid) 
    problem.map = grid
    policy = Policy(problem)
    problem.map=copys
    return policy    
    
    '''

def q_solve(problem, iterations):
    policy = Policy(problem)
    # TODO
    return policy

# Main:  read the problem from stdin, print the policy and the utility over a test run
if __name__ == "__main__":
    problem = Problem()
    policy = problem.solve(ITERATIONS)
    print(policy)
    print("Calculating average utility...")
    print("Average utility per move: {utility:.2f}".format(utility = try_policy(policy, problem,ITERATIONS)))
        

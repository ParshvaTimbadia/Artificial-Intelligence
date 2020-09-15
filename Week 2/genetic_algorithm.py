# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 09:52:13 2020

@author: HP
"""


#Implement genetic algorithm in Python for creating a list of N numbers that 
#equal X when s squared and summed together.


#Steps involved in the Genetic Algorithm. 
'''
1. Creating an Individial
2. Creating the population
3. Creating Function for Calculating the Fitness Value
4. Select the parents 
5. Perform Crossover
6. Perform mutation only on Parents.


'''

#Importing libraries.
from random import random, randint
from operator import add
import functools 
from time import time




#First we will create an individual often in the GA it is referred as Chromosomes

def chromosomes(length, min_val, max_val):
    '''
    
    Parameters
    ----------
    size : This provides the size of each individual.
    min_val : The minimumm value a cell in the chromosome should have.
    max_val : The maximum value a cell in the chromosome should have.

    Returns: a list of chromosome. 
    
    The values of the each cell is selected randomly.
   
    '''
    
    list=[]
    for i in range(length):
        list.append(randint(min_val, max_val))
        
    return list

#Now its time to create function for the populaiton. 
#Population is nothing but multiple chromosomes together.

def population(size, length, min_val, max_val):
    '''
    
    size : This is the size of the population   
    length : The length of each chromosomes
    min_val :The minimum value of chromosomes
    max_val : The maximum value of chromosomes

    Returns
        population : 
        
            This function return the list of different chromosomes.

    '''
    
    population=[]
    for i in range(size):
        population.append(chromosomes(length, min_val, max_val))
    
    
    return population


#Now we need to assign the fitness of each population 
#For our problem we will determine fitness by ditance between squared sum of individual 
# and the the final target X.
    
def fitness(individual, target):
    '''
    This returns the fitness value for each chromosomes.

    '''
    squared_individual = [number ** 2 for number in individual]
    sum = functools.reduce(add, squared_individual)
    return abs(target-sum)


    

#Now its time to evlove that is to mutate and crossover. 
def eval(popu, target,lower_bound, upper_bound, random_select=0.05 ):
    
    '''
    This function privodes the best possible chromosome.
    '''
    
    iteration=0
    '''This time function is for the reason that program should terminate after 30 seconds
    The reason for this is that sometimes answer get stuck on the local optima and might 
    get into an infinite loop. For instance, take the target value as 105, it is not possible for 
    the chromosome of size 5 and values reanging from (0,5) to provide the exact result.
    It will get stuck on 104 in that case. [5,5,5,5,2] would be the best possible result at 
    that time. So we are running the program for 30 Seconds.
    '''
    end= time() + 30
    new_selection = float('inf')
    
    '''
    Now we will keep on running the while loop until we achieve the result desired.
    '''
    while True and time() < end:
        
        iteration+=1
        
        #Now take the value from the population and arrange them according to the
        #fitness value. 
        selection = [(fitness(x, target), x) for x in popu]
        
    
        
        #Sorting accoring to cost function 
        selection = sorted(selection, key= lambda i: i[0])
        
        
        
        if selection[0][0]==0: #This means that we have achieved the goal.
            best_val = list(selection[0][1])
            break 
        elif new_selection > selection[0][0]:
            best_val = list(selection[0][1])
            new_selection = selection[0][0]
            
        
        
          #Now we will select the retain_length, that is the length to select the number of
        #parents from the total population 
        retain_length = int(len(selection)*0.2)
        
   
        parents = selection[:retain_length]
        
       
        #Now we will also consider other individuals randomly for better results. 
    
        for individual in selection[retain_length:]:
        #the random function helps to generate the random value from 0.0 to 1.0 
            if random_select > random():
                parents.append(individual)
        
       
        
        final_parents=[]
        for i in parents:
            final_parents.append(i[1])
        
        #  print(final_parents)
        # break   
            
        parents_length= len(final_parents)
        desired_length= len(popu)-parents_length
       
            
        '''
        CrossOver
        '''
        children=[]
        while len(children)< desired_length:
            parent_1_index = randint(0, parents_length-1)
            parent_2_index = randint(0, parents_length-1)
        
            if parent_1_index != parent_2_index:
                parent_1= final_parents[parent_1_index]
                
                parent_2= final_parents[parent_2_index]
              
                
                half= int (len(parent_1)/2)
                child= parent_1[:half]+ parent_2[half:]
                
                
                
                children.append(child)
    
        '''
        
        Now we will mutate the parents here. 
        
        '''
    
        for individual in final_parents:
           
                position_to_change= randint(0, len(individual)-1)
                
                #Need to change this mutation into a better one
                
                individual[position_to_change] = randint(lower_bound, upper_bound)
                
      
        final_parents.extend(children)
        
        
        popu=final_parents        
    
    
    print()
    print("The optimal chromosome which we got", best_val,"after",iteration, "Iterations") 
    
    


s= int(input("Enter the size of population you want: "))

l= int(input("Enter the length of Each Chromosome that you want: "))

mi= int(input("Enter the minimum value that you want in the Chromosomes: "))

ma= int(input("Enter the maximum value that you want in the Chromosomes: "))

print()
print("Please wait 30 seconds incase the answer is not provided instantly....")

p = population(s, l, mi, ma)
target= int(input("Enter the Target Value that you want to achieve: "))
eval(p, target, mi, ma)



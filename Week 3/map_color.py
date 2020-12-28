# R is a set of restrictions
# this function colors the given province with the given color
# returns false if not possible, returns the set of new restrictions if possible
def addColor(R, province, color):
    ans = []
    for rr in R:
        res = checkRestriction(rr, province, color)
        if res == False:
            return False
        elif res == None:
            continue
        else:
            ans.append(res)
    return ans


# checks if the restrition rr allows the given province to have the given color
# returns false if not possible, otherwise returns the new restriction
def checkRestriction(rr, province, color):
    # finding the index of the province (saved to index)
    index = -1
    other = -1
    if rr[0] == province:
        index = 0
        other = 1
    elif rr[1] == province:
        index = 1
        other = 0
    else:
        return rr

    if isinstance(rr[other], int):
        # other component is a color
        if (color != rr[other]):
            return None
        else:
            return False
    else:
        return [rr[other], color]


# solving the CSP by variable elimination
# recursive structure: ci is the province index to be colored (0 = bc, 1 = ab, etc)
# n is the number of colors
# provinces is a list of provinces
# if coloring is possible returns the province-> color map, otherwise False
# for 3 colors outputs should be like {'ab': 1, 'bc': 2, 'mb': 1, 'nb': 1, 'ns': 2, 'nl': 1, 'nt': 3, 'nu': 2, 'on': 2, 'pe': 3, 'qc': 3, 'sk': 2, 'yt': 1}

"""
Declaring a global variable
"""
color_map={}

def solveCSP(provinces, n, R, ci):
    # no choice for the current province
     
    global color_map
    """
    IF you wnat to check whether the variables are actually getting eliminated or not 
    uncomment the line in the code. That line basically provides the new set of restrictions 
    and you will clearly able to see that the variables are getting eliminated. 
    
    
    Note: The result for the Number of nodes 3,4 and 5 are same. This is because 
    in the given map any state is connected to at the most 3 neighbour and hence there is no
    requirement for any additional colors to use. 
    
    Note: Also the number of colors should be atleast 2 else it would throw a message such as 
    Invalid. This is because almost any of the Grph coloring problem are actaully solvable by 4 
    colors in the worst case. Usually 3 works fine but 2 is just impossible. 
    
    
    Also, the while loop in the end was an infinte loop so I am adding additional line which will
    stop the code when you type -1. 
    
    """
    
    if n <3: 
        
        return "Please use numbers from 3 to 5  !!!"
    
    
    """
    Without Recursion
    """
    # for province in provinces:
        
    #     for color in range(1, n+1):
            
    #         new_res= addColor(R, province, color)
            
    #         if new_res ==False:
    #             continue
    #         else:
                
    #             R= new_res
    #             print("New Restiction:",R)
    #             color_map[province]=color
    #             break
    
    # return color_map
   
    
    """
    With Recursion 
    """
    
    
    
    for color in range(1, n+1):
        new_res = addColor(R, provinces[ci], color)
        
        if new_res==False:
            continue
        else:
            color_map[provinces[ci]]=color
            R= new_res
            # print("New Restiction:",R)
            break
        
    if ci<len(provinces)-1:
        solveCSP(provinces, n, new_res, ci+1)
    else:
        return color_map
            
    return color_map        
            
    
    

  

# main program starts
# ===================================================

n = 5  # int(input("Enter the number of color"))
colors = []
for i in range(1, n + 1):
    colors.append(i)
print(colors)

# creating map of canada
# cmap[x] gives the neighbors of the province x
cmap = {}
cmap["ab"] = ["bc", "nt", "sk"]
cmap["bc"] = ["yt", "nt", "ab"]
cmap["mb"] = ["sk", "nu", "on"]
cmap["nb"] = ["qc", "ns", "pe"]
cmap["ns"] = ["nb", "pe"]
cmap["nl"] = ["qc"]
cmap["nt"] = ["bc", "yt", "ab", "sk", "nu"]
cmap["nu"] = ["nt", "mb"]
cmap["on"] = ["mb", "qc"]
cmap["pe"] = ["nb", "ns"]
cmap["qc"] = ["on", "nb", "nl"]
cmap["sk"] = ["ab", "mb", "nt"]
cmap["yt"] = ["bc", "nt"]

# CSP restrictions
# each restriction is modeled as a pair [a,b] which means the province 5a's
# color is not equal to b, where b is either a color (a number 1 to n) or
# another province. Examples ['bc', 'ab'] means the color of bc should
# not be equal to ab -- ["bc",4] means the color of bc should not be 4
# R is the list of restrictions

R = []

# initiaitiong restrictions based on the province neighborhood

for x in cmap:
    for y in cmap[x]:
        R.append([x, y])



# initiating a list of provinces
provinces = []
for p in cmap:
    provinces.append(p)


while (1):
    num = int(input("Enter number of  colors? "))
    if num==-1: #Enter -1 to terminate the code.
        print("DONE")
        break
    print(solveCSP(provinces, num, R, 0))
    

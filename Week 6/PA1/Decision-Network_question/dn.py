from decimal import Decimal, ROUND_HALF_UP
import copy, random
from itertools import product

jointProbDict = dict()
query = []
nodesDict = dict()
nodesDict_Copy = None
utilityNode = None


def readFromFile(fname):
    inputArray = []
    with open(fname) as f:
        inputArray = f.readlines()
    return inputArray


def writeToFile(fname, outputArr):
    x = len(outputArr) - 1
    with open(fname, 'w+') as file:
        for i in range(0, x):
            file.write(outputArr[i] + '\n')
        file.write(outputArr[x])


class Node:

    def __init__(self, name, nodeType, parents, children, probMatrix):
        self.name = name  # name of the node
        self.nodeType = nodeType  # node type : decision node, chance node or utility node
        self.parents = parents  # list of parents of this node in sorted order
        self.children = children  # list of children of this node in sorted order
        self.probMatrix = probMatrix  # probability matrix of this node; design it as a dicitionary


def hiddenVariablesCalc(varDictList):
    global jointProbDict, nodesDict
    varDictList_Local = copy.deepcopy(varDictList)
    for i in varDictList_Local:
        parentsList = nodesDict[i].parents
        if parentsList == None or len(parentsList) == 0:
            continue
        for p in parentsList:
            if p not in varDictList_Local:
                varDictList_Local.append(p)
    varDictList_Local = sorted(varDictList_Local)
    if varDictList_Local == varDictList:
        return varDictList_Local
    else:
        return hiddenVariablesCalc(varDictList_Local)


def hiddenVariablesCalcLocal(varDictList):
    global jointProbDict, nodesDict_Copy
    varDictList_Local = copy.deepcopy(varDictList)
    for i in varDictList_Local:
        parentsList = nodesDict_Copy[i].parents
        if parentsList == None or len(parentsList) == 0:
            continue
        for p in parentsList:
            if p not in varDictList_Local:
                varDictList_Local.append(p)
    varDictList_Local = sorted(varDictList_Local)
    if varDictList_Local == varDictList:
        return varDictList_Local
    else:
        return hiddenVariablesCalcLocal(varDictList_Local)


varsLocal = []
pGlobal = []
cGlobal = []


def getLCA(var):
    global nodesDict, varsLocal, pGlobal, cGlobal
    if nodesDict[var].parents == None and nodesDict[var].nodeType == 'decision':
        return 1
    if nodesDict[var].parents == None and nodesDict[var].nodeType == 'chance':
        return 0
    parentsList = nodesDict[var].parents
    tmp = 0
    for j in range(len(parentsList)):
        if parentsList[j] in varsLocal: return 1
        pGlobal.append(parentsList[j])
        cGlobal.extend(nodesDict[parentsList[j]].children)
        if not set(cGlobal).issubset(set(pGlobal)): return 1
        tmp += getLCA(parentsList[j])
    if tmp == 0:
        return 0
    else:
        return 1


def jointProbabilityCalculator(varDict):
    global jointProbDict, nodesDict, nodesDict_Copy
    if nodesDict_Copy == None:
        nodesDict_Copy = copy.deepcopy(nodesDict)
    res = 1.0
    for key in sorted(varDict.iterkeys()):
        probMatrixDict = nodesDict_Copy[key].probMatrix
        if nodesDict_Copy[key].parents == None or nodesDict_Copy[key].parents == []:
            if not nodesDict_Copy[key].nodeType == 'decision':
                if varDict[key] == '+':
                    res *= probMatrixDict['s']
                else:
                    res *= (1 - probMatrixDict['s'])
        else:
            parentsList = nodesDict_Copy[key].parents
            signStr = ''
            for i in parentsList:
                signStr += varDict[i]
            if varDict[key] == '+':
                res *= probMatrixDict[signStr]
            else:
                res *= (1 - probMatrixDict[signStr])
    
    return res


def list_difference(a, b):
    b = set(b)
    return [x for x in a if x not in b]


def enumJointProbWithHV(varDict, hiddenVars):
    global nodesDict
    hiddenVars_Local = copy.deepcopy(hiddenVars)
    if len(hiddenVars_Local) == 0:
        return jointProbabilityCalculator(varDict)
    varDict_True = copy.deepcopy(varDict)
    varDict_False = copy.deepcopy(varDict)
    current = hiddenVars_Local.pop(0)
    varDict_True[current] = '+'
    varDict_False[current] = '-'
    return enumJointProbWithHV(varDict_True, hiddenVars_Local) + enumJointProbWithHV(varDict_False, hiddenVars_Local)


def jointProbabilityCalculatorWithHiddenVariables(varDict, hiddenVars=None):
    global nodesDict, nodesDict_Copy, varsLocal, pGlobal, cGlobal
    varsLocal = varDict.keys()
    var = varDict.keys()
    queue = []
    for i in range(len(var)):
        v = var[i]
        if nodesDict[v].parents == None:
            continue
        pGlobal = [v]
        cGlobal = []
        if getLCA(v) == 1:
            continue
        else:
            queue.append(v)
    for i in range(len(queue)):
        v = queue[i]
        hvLocal = list_difference(hiddenVariablesCalc(list(v)), list(v))
        nodesDict_Copy[v].probMatrix['s'] = enumJointProbWithHV({str(v): '+'}, hvLocal)
        nodesDict_Copy[v].parents = None
    hv = list_difference(hiddenVariablesCalcLocal(varDict.keys()), varDict.keys())
    return enumJointProbWithHV(varDict, hv)


s_add = 0

def calculator_EU(jp):
    # return jointProbabilityCalculatorWithHiddenVariables(jp)\
    #     / jointProbabilityCalculatorWithHiddenVariables(varDict)
    
    return jointProbabilityCalculatorWithHiddenVariables(jp)
    

def getListKeys(dict): 
    list = [] 
    for key in dict.keys(): 
        list.append(key) 
          
    return list


def getListValue(dict): 
    list = [] 
    for key in dict.values(): 
        list.append(key) 
          
    return list

def expectedUtility(parentDict, varDict, parentDictList):
    global jointProbDict, nodesDict, s_add, utilityNode
    parentDictList_Local = copy.deepcopy(parentDictList)
    # TODO section
    
    s_add= jointProbabilityCalculatorWithHiddenVariables(varDict)
    onlyuKeys = getListKeys(utilityNode.probMatrix) 
    onlyuval = getListValue(utilityNode.probMatrix)
    world_of_parent=[]
    ukeylist=[]
    
    #List of List
    for x in onlyuKeys:
        temp=[]
        for i in x:
            temp.append(i)
        ukeylist.append(temp)
    
    
    # print(parentDictList) #Which Position should we consider. 
    
    
    if len(parentDict)==len(parentDictList):
        c=0
        result=0 
        for j in ukeylist: 
            barca=0
            for i in parentDictList:
               parentDict[i]=j[barca]
               barca+=1
                # ++- 
                #Combine VarDict
            jp={}
            
            for key, val in varDict.items():
                jp[key]= val #This will take all the values from the varDict 
        
            #Now calculation for the parent. 
            for key,val in parentDict.items():
                jp[key]= val
        
            #Now calculating the probability 
            result+= jointProbabilityCalculatorWithHiddenVariables(jp)*onlyuval[c]
            c+=1
        
        
        
    else: #This is for the handling the case like input three

        result=0
        while len(parentDictList_Local)!=0:
            current = parentDictList_Local.pop(0) #[D, I]
            if current in varDict:
                newprobdict= copy.deepcopy(parentDictList)
                #Now storing the symbol and the index. 
                index_of_current = newprobdict.index(current)
                value_of_current_in_VD = varDict[newprobdict[index_of_current]]
                
                #Calculating the Utility. 
                result=0 
                for j in range(len(ukeylist)):
                    for i,key in enumerate(parentDict):
                        if ukeylist[j][index_of_current]==value_of_current_in_VD:
                             
                            parentDict[key]= ukeylist[j][i] 
                        
                        
                    if ukeylist[j][index_of_current]==value_of_current_in_VD:
                        jp={}
            
                        for key, val in varDict.items():
                            jp[key]= val #This will take all the values from the varDict 
            
                        #Now calculation for the parent. 
                        for key,val in parentDict.items():
                            jp[key]= val
                
                #Now calculating the probability
                        
                        result+= calculator_EU(jp)*onlyuval[j]
                
    
    return result  
                       
    
    
    '''
    #################################################################################################################
    '''
    
    # result=0
     
    # while True:
    # #So now first lets consider the parents node.
    #     #Storing the first value and then removing it off from the parentDict_local
    #     parent= parentDictList_Local[0]
    #     del parentDictList_Local[0]
        
    #     if parent in varDict:
    #         if not parentDictList_Local:
            
            
    #             if len(parentDictList_Local)==0:
    #                 sign_store="" #This is for ++ +- 
                    
    #                 #Iterating through the parent dict and calculating the probability. 
                    
    #                 for i in utilityNode.parents:
    #                     if i in parentDict:
    #                         sign_store+=parentDict[i] #Storing the positive signature.
                            
    #                     #If not present adding the value from vardict like EU(I=+)
    #                     elif i in varDict:
    #                         sign_store+=varDict[i]
                            
    #                 jp={}
        
    #                 for key, val in varDict.items():
    #                     jp[key]= val #This will take all the values from the varDict 
        
    #                 #Now calculation for the parent. 
    #                 for key,val in parentDict.items():
    #                     jp[key]= val
                    
    #                 without_utility = calculator_EU(jp,varDict)
                    
    #                 result+= without_utility*utilityNode.probMatrix[sign_store]
    #                 s_add+=without_utility
            
    #     #Now considering both positive value and negative value of the given parent 
    #     #ie D+ and D- 
    #     parents_pos, parents_neg = copy.deepcopy(parentDict), copy.deepcopy(parentDict)
    #     # Lets change the value of the variable as per formulae. 
    #     # So basically assigning negative sign for neg and so on and we will calculate prob based on that. 
    #     parents_pos[parent]='+'
    #     parents_neg[parent]='-'
        
    #     if not parentDictList_Local:
            
    #         if parents_pos:
    #             if len(parentDictList_Local)==0:
    #                 sign_store="" #This is for ++ +- 
                    
    #                 #Iterating through the parent dict and calculating the probability. 
                    
    #                 for i in utilityNode.parents:
    #                     if i in parents_pos:
    #                         sign_store+=parents_pos[i] #Storing the positive signature.
                            
    #                     #If not present adding the value from vardict like EU(I=+)
    #                     elif i in varDict:
    #                         sign_store+=varDict[i]
                            
    #                 jp={}
        
    #                 for key, val in varDict.items():
    #                     jp[key]= val #This will take all the values from the varDict 
        
    #                 #Now calculation for the parent. 
    #                 for key,val in parents_pos.items():
    #                     jp[key]= val
                    
    #                 without_utility = calculator_EU(jp,varDict)
                    
    #                 result+= without_utility*utilityNode.probMatrix[sign_store]
    #                 s_add+=without_utility
                
    #         if parents_neg:
    #             if len(parentDictList_Local)==0:
    #                 sign_store="" #This is for ++ +- 
                    
    #                 #Iterating through the parent dict and calculating the probability. 
                    
    #                 for i in utilityNode.parents:
    #                     if i in parents_neg:
    #                         sign_store+=parents_neg[i] #Storing the neg signature.
                            
    #                     #If not present adding the value from vardict like EU(I=+)
    #                     elif i in varDict:
    #                         sign_store+=varDict[i]
                            
    #                 jp={}
        
    #                 for key, val in varDict.items():
    #                     jp[key]= val #This will take all the values from the varDict 
        
    #                 #Now calculation for the parent. 
    #                 for key,val in parents_neg.items():
    #                     jp[key]= val
                    
    #                 without_utility = calculator_EU(jp,varDict)
                    
    #                 result+= without_utility*utilityNode.probMatrix[sign_store]
                    
    #                 s_add+=without_utility
                
          
    #     if len(parentDictList_Local)==0:
    #         return result
    
    
    '''
    #####################################################################################################
    '''
    # print(parentDict, varDict, parentDictList)
    
    # s_add= jointProbabilityCalculator(varDict)
    # jp={}
    
    # for key, val in varDict.items():
    #     jp[key]= val #This will take all the values from the varDict 
    
    # #Now calculation for the parent. 
    # for key,val in parentDict.items():
    #     jp[key]= val
    
    # #Calculation for probability now 
    
    # calc1 = jointProbabilityCalculatorWithHiddenVariables(jp)
    
    # #Considering other cases apart from the fixed one
    
    # for key in jp.iterkeys():
    #     if key in parentDict.iterkeys():
    #         if jp[key]=='+':
    #             jp[key]='-'
    #         else:
    #             jp[key]='+'
    
    # calc2 = jointProbabilityCalculatorWithHiddenVariables(jp)
    
    # result= utilityNode.probMatrix['+']*calc1 + utilityNode.probMatrix['-']*calc2
    
    # print(round(result/s_add))
    # return result
    
    
    
def permutations(size):
    return list(product(['+','-'],repeat =size))
  
            

expectedUtilityDict = dict()


def maximumExpectedUtility(qList, qDict):
    global jointProbDict, nodesDict, expectedUtilityDict, s_add, utilityNode
    qList_Local = copy.deepcopy(qList)
    
    # print(qDict)
    # print(qList)
    #First create all the possibilities for whatever it is in qDict. 
    # print(utilityNode.probMatrix)
    
    #Generating the size similar to the length for the possible permutations
    size= len(qDict)
    symbols= permutations(size)
    new_list=[]
    
    
    #Generating all the possible symbols 
    #That is it provides all the possible cases. 
    for i in symbols:
        x=0
        #Now creating a new dict to avoid updating of the value.
        d=copy.deepcopy(qDict)
        for key, val in d.items():
            #This is the new dict which will be assigned and stored in the new_list
            d[key]=i[x]
            x+=1
        new_list.append(d)
            
    for i in new_list:
         #Getting the symbol first from the generated possibilites 
        sym=''
        for key in i:
            sym+=i[key]
            
       
        parentDict={} 
        
        #Creaitng the parent dict which is not a constant and keep on changing 
        #This change will be reflected when EU is called.
        parentDictList= utilityNode.parents
        for parent_v in parentDictList:
            
            if parent_v not in i:
                #It doesnt matter here what we assign it is going to change anyways in the 
                #EU it is going to change
                parentDict.update({parent_v:'-'})
                
        result = expectedUtility(parentDict, i, parentDictList)
        
         
        
        #Now stroing the reuslt into the EUDict it will store all the possibilities. 
        #Maximum will be selected from the it 
        
        if sym not in expectedUtilityDict:
            expectedUtilityDict[sym]=result
        
        elif sym in expectedUtilityDict and result> expectedUtilityDict[sym]:
            expectedUtilityDict[sym]=result
    return


def maximumExpectedUtilityWithConditional(qDict, evDict, qList):
    global jointProbDict, nodesDict, expectedUtilityDict, s_add, utilityNode
    qList_Local = copy.deepcopy(qList)
    # TODO section
    
    #Generating the size similar to the length for the possible permutations
    size= len(qDict)
    symbols= permutations(size)
    new_list=[]
    
    
    #Generating all the possible symbols 
    #That is it provides all the possible cases. 
    for i in symbols:
        x=0
        #Now creating a new dict to avoid updating of the value.
        d=copy.deepcopy(qDict)
        for key, val in d.items():
            #This is the new dict which will be assigned and stored in the new_list
            d[key]=i[x]
            x+=1
        new_list.append(d)
            
    for i in new_list:
        
        #Getting the symbol first from the generated possibilites 
        sym=''
        for key in i:
            sym+=i[key]
        
        #Using the code from above used many times for updating the values in the dict.
        varDict={}
        
        for key, val in i.items():
            varDict[key]= val 
        
                   
        for key,val in evDict.items():
            varDict[key]= val
        
       
        parentDict={} 
        
        
        parentDictList= utilityNode.parents
        
        #Creaitng the parent dict which is not a constant and keep on changing 
        #This change will be reflected when EU is called.
        for parent_v in parentDictList:
            if parent_v not in varDict:
                parentDict.update({parent_v:'+'})
        
        s_add=0
        new_result = expectedUtility(parentDict, varDict, parentDictList)/s_add
        #The S_add value will get changed here when it is calling the EU
        
        #Now stroing the reuslt into the EUDict it will store all the possibilities. 
        #Maximum will be selected from the it 
        
        if sym not in expectedUtilityDict:
            expectedUtilityDict[sym]=new_result
        
        elif sym in expectedUtilityDict and new_result > expectedUtilityDict[sym]:
            expectedUtilityDict[sym]=new_result
    return
    

    #Trial
    # jointProbDict={}
    # qList_Local1 = copy.deepcopy(qList)
    # qList_Local2 = copy.deepcopy(qList)
    # QD_with_pos = copy.deepcopy(qDict)
    # QD_with_neg = copy.deepcopy(qDict)
    
    # #print(qList_Local) 
    # #print(qDict)    
    # parentDict={} #First value of the EU
    # #For positive calc 
    # while True:
    #     #Taking the first value
    #     s_add=0
    #     first= qList_Local1[0]
    #     del qList_Local1[0]
    #     #Making the val as positive.
    #     QD_with_pos[first]='+'
        
    #     symbol = ''
    #     for key in QD_with_pos:
    #         symbol+=QD_with_pos[key]
        
    #     varDict = {}
    #     varDict.update(QD_with_pos)
    #     varDict.update(evDict)
        
        
    #     for i in utilityNode.parents:
    #         if i not in varDict:
    #             parentDict.update({i:'+'})
        
        
    #     re= expectedUtility(parentDict, varDict , utilityNode.parents)/s_add
    #     expectedUtilityDict.update({symbol:re})
        
        
    #     if len(qList_Local1)==0:
    #         break
    
    # parentDict={}
    # #For negative calc 
    # while True:
    #     #Taking the first value
    #     s_add=0
    #     first= qList_Local2[0]
    #     del qList_Local2[0]
    #     #Making the val as positive.
    #     QD_with_neg[first]='-'
        
    #     symbol = ''
    #     for key in QD_with_neg:
    #         symbol+=QD_with_neg[key]
        
    #     varDict = {}
    #     varDict.update(QD_with_neg)
    #     varDict.update(evDict)
        
        
    #     for i in utilityNode.parents:
    #         if i not in varDict:
    #             parentDict.update({i:'+'})
        
    #     re= expectedUtility(parentDict, varDict, utilityNode.parents)/s_add
    #     expectedUtilityDict.update({symbol:re})
    #     print(expectedUtilityDict)
        
    #     if len(qList_Local2)==0:
    #         break
    
    # return
    
    


def main():
    inputArray = readFromFile('./Testcases/input09.txt')
    i = 0
    global query, nodesDict, utilityNode, s_add, expectedUtilityDict, nodesDict_Copy
    while i < len(inputArray):
        
        if '*' not in inputArray[i]:
            xx = inputArray.pop(i).split('\n')[0]
            query.append(xx) #-Parshva This is first part of the code before ****
        else:
            inputArray.pop(i)
            break
      
    # now we are left with the inputArray containing the node specification
    while len(inputArray) != 0:
        nodePlaceholder = []
        i = 0
        # translating one node into a bayesian network node
        while i < len(inputArray):
            if '*' not in inputArray[i]:
                nodePlaceholder.append(inputArray.pop(i))
            else:
                inputArray.pop(i)
                break
        # now we have reached a line containing a '*', thus we can move forward with creating a node for the obtained lines of data
        # we start with initializing the probMatrix dictionary
        # print(nodePlaceholder)
        probMatrix = dict()
        # finding out the name of this node & whether or not it has any parents
        firstLine = nodePlaceholder[0].split()
        if len(firstLine) == 1:
            name = firstLine[0]
            parents = []
            children = []
            # if the node is a decision node, it has no parents and no probMatrix
            if 'decision' in nodePlaceholder[1]:
                nodeType = 'decision'
                probMatrix = None
                parents = None
            # if the node is a chance node, it will have one line after the name which gives us the probability of this node when this node is True,
            # independent of any other node (as it doesn't have any parents). Thus we create a dictionary storing the probability value for when
            # the node is True and when it is False.
            else:
                nodeType = 'chance'
                prob = float(nodePlaceholder[1])
                probMatrix.update({'s': prob})
            # now we create the node for this node, and we add the newly created node in the dictionary nodesDict
            node = Node(name, nodeType, parents, children, probMatrix)
            nodesDict.update({name: node})
        # if the node had dependencies on other nodes, i.e., it has some parent nodes
        else:
            firstLine = nodePlaceholder[0].split()
            name = firstLine.pop(0)
            firstLine.pop(0)
            if name == 'utility':
                nodeType = 'utility'
                children = None
            else:
                nodeType = 'chance'
                children = []
            parents = sorted(firstLine)
            nodePlaceholder.pop(0)
            # loop to populate the probMatrix dicitionary
            for j in nodePlaceholder:
                current = j.split()
                val = float(current[0])  # probability value is stored here
                boolVals = [x for (y, x) in sorted(
                    zip(firstLine, current[1:]))]  # array containing the signs as per the sorted variables
                boolValsString = ''.join(boolVals)  # string containing the signs as per the sorted variables
                probMatrix.update({boolValsString: val})
            # now we have the probMatrix populated as per the sorted parents list
            # now we create the node for this node, and we add the newly created node in the dictionary nodesDict
            node = Node(name, nodeType, parents, children, probMatrix)
            # if it is a utility node, store it in the utilityNode variable
            if name == 'utility':
                utilityNode = node
            # else, if the node is not a utility node, we add the node to the dictionary nodesDict
            else:
                nodesDict.update({name: node})
            # now update the children list for the parents of this node
            for p in parents:
                nodesDict[p].children.append(name)
    
    # print(probMatrix) #- Parshva This basically provides the end utility value 
    outputArr = []
    for i in query:
        yy = i.split('(')
        zz = yy[1].split(')')  # removing the closing brace
        internalStr = zz[0]  # this is the internal string, i.e the string of variables inside the brace
        func = yy[0]
        if func == 'P':
            # probability
            if '|' in internalStr:
                # conditionality exists
                nodesDict_Copy = None
                nodesDict_Copy = copy.deepcopy(nodesDict)
                qDict = dict()
                evDict = dict()
                aa = internalStr.split('|')
                q = aa[0].split(',')
                e = aa[1].split(',')
                for z in q:
                    bb = z.split('=')
                    k = bb[0].strip()
                    v = bb[1].strip()
                    qDict.update({k: v})
                for z in e:
                    bb = z.split('=')
                    k = bb[0].strip()
                    v = bb[1].strip()
                    evDict.update({k: v})
                varDict = dict()
                varDict.update(qDict)
                varDict.update(evDict)
                num = jointProbabilityCalculatorWithHiddenVariables(varDict)
                hv = list_difference(hiddenVariablesCalcLocal(evDict.keys()), evDict.keys())
                den = enumJointProbWithHV(evDict, hv)
                tmp = Decimal(str(num / den))
                output = str(Decimal(tmp.quantize(Decimal('0.01'))))
                outputArr.append(output.ljust(4, '0'))
                nodesDict_Copy = None

            else:
                # conditionality doesn't exist
                nodesDict_Copy = None
                nodesDict_Copy = copy.deepcopy(nodesDict)
                lit = internalStr.split(', ')  # split the string str on ', ' to get the list of literals
                varDict = dict()
                for z in lit:
                    aa = z.split('=')
                    k = aa[0].strip()
                    v = aa[1].strip()
                    varDict.update({k: v})
                # if the number of variables here in the varDict is the same as the number of variables in the nodesDict, we simply
                # calculate the Joint Probability
                if len(varDict) == len(nodesDict):
                    tmp = Decimal(str(jointProbabilityCalculator(varDict)))
                    output = str(Decimal(tmp.quantize(Decimal('0.01'))))
                    outputArr.append(output.ljust(4, '0'))
                # otherwise, we will calculate the Joint Probability summed over the hidden variables
                else:
                    tmp = Decimal(str(jointProbabilityCalculatorWithHiddenVariables(varDict)))
                    output = str(Decimal(tmp.quantize(Decimal('0.01'))))
                    outputArr.append(output.ljust(4, '0'))

                nodesDict_Copy = None

        elif func == 'EU':
            # Expected Utility
            s_add = 0
            if '|' in internalStr:
                nodesDict_Copy = None
                nodesDict_Copy = copy.deepcopy(nodesDict)
                # conditionality exists
                qDict = dict()
                evDict = dict()
                aa = internalStr.split('|')
                q = aa[0].split(',')
                e = aa[1].split(',')
                for z in q:
                    bb = z.split('=')
                    k = bb[0].strip()
                    v = bb[1].strip()
                    qDict.update({k: v})
                for z in e:
                    bb = z.split('=')
                    k = bb[0].strip()
                    v = bb[1].strip()
                    evDict.update({k: v})
                parentsList = utilityNode.parents
                parentDict = dict()
                for i in parentsList:
                    if i not in evDict:
                        parentDict.update({i: '+'})
                varDict = dict()
                varDict.update(qDict)
                varDict.update(evDict)
                tmp = str(int(round(expectedUtility(parentDict, varDict, parentsList) / s_add, 0)))
                print(tmp)
                nodesDict_Copy = None

            else:
                # conditionality doesn't exist
                nodesDict_Copy = None
                nodesDict_Copy = copy.deepcopy(nodesDict)
                qDict = dict()
                evDict = dict()
                aa = internalStr.split(',')
                for z in aa:
                    bb = z.split('=')
                    k = bb[0].strip()
                    v = bb[1].strip()
                    evDict.update({k: v})
                parentsList = utilityNode.parents
                for i in parentsList:
                    if i not in evDict:
                        qDict.update({i: '+'})
                tmp = str(int(round(expectedUtility(qDict, evDict, parentsList), 0)))
                print(tmp)
                nodesDict_Copy = None

            outputArr.append(tmp)

        elif func == 'MEU':
            # Maximum Expected Utility
            expectedUtilityDict = dict()
            s_add = 0
            if '|' in internalStr:
                # conditionality exists
                nodesDict_Copy = None
                nodesDict_Copy = copy.deepcopy(nodesDict)
                qList = []
                evDict = dict()
                aa = internalStr.split('|')
                q = aa[0].split(',')
                e = aa[1].split(',')
                for z in q:
                    bb = z.strip()
                    qList.append(bb)
                for z in e:
                    bb = z.split('=')
                    k = bb[0].strip()
                    v = bb[1].strip()
                    evDict.update({k: v})
                qDict = dict()
                for i in qList:
                    qDict.update({i: '+'})
                maximumExpectedUtilityWithConditional(qDict, evDict, qList)
                tmp_val = max([expectedUtilityDict[_] for _ in expectedUtilityDict])
                for key in expectedUtilityDict:
                    if expectedUtilityDict[key] == tmp_val:
                        tmp_key = key
                tmp = ''
                for i in tmp_key:
                    tmp += i
                    tmp += ' '
                tmp += str(int(round(tmp_val, 0)))
                nodesDict_Copy = None

            else:
                nodesDict_Copy = None
                nodesDict_Copy = copy.deepcopy(nodesDict)
                qList = []
                aa = internalStr.split(',')
                for z in aa:
                    bb = z.strip()
                    qList.append(bb)
                qDict = dict()
                for i in qList:
                    qDict.update({i: '+'})
                maximumExpectedUtility(qList, qDict)
                tmp_val = max([expectedUtilityDict[_] for _ in expectedUtilityDict])
                for key in expectedUtilityDict:
                    if expectedUtilityDict[key] == tmp_val:
                        tmp_key = key
                tmp = ''
                for i in tmp_key:
                    tmp += i
                    tmp += ' '
                tmp += str(int(round(tmp_val, 0)))
                nodesDict_Copy = None

            outputArr.append(tmp)
    
   
    writeToFile('output.txt', outputArr)
    print(outputArr)
    print(' #### : ', expectedUtilityDict)


main()

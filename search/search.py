# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import Queue
from util import PriorityQueue


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    path = []          #lista goala care reprezinta calea pe care o urmeaza sa ajunga la starea curenta
    currState =  problem.getStartState()

    if problem.isGoalState(currState):     #verific daca starea initiala e si stare de luat in lista
        return path

    st = Stack()
    st.push( (currState, path) )     # inserez starea initiala ca sa ii fac pop prima data ei
    explored = set() #un set sa tin minte the explored states
    while not st.isEmpty():
        currState, path = st.pop()   #scot starea si path-ul corespunzator
        if problem.isGoalState(currState):
            return path
        explored.add(currState)
        for i in problem.getSuccessors(currState):
            if i[0] not in explored: #daca succesorul nu este deja explorat
                st.push( (i[0], path + [i[1]]) )  #il adug in stiva si actualizez path-ul 
                #s[1] acction ul cu care am ajuns in punctul ala (ex sud)   
    return []    #daca am ajuns aici nu am gasit solutia

   

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    path= []           
    currState =  problem.getStartState()    

    if problem.isGoalState(currState):    
        return path

    q = Queue()
    q.push( (currState, path)) 
    exp=set()   
    while not q.isEmpty():
        currState, path = q.pop()    
        if problem.isGoalState(currState): #vad daca o adaug la solutia finala
            return path
        exp.add(currState)

        qStates=[]
        for j in q.list:
            qStates.append(j[0]) #j[0] e primul element din tupla stocata in coada
            #si reprezenta a state of the node adicare currState
            #dupa for ul asta qState contine toate starile nodurilor prezente momentan in coada

        for i in problem.getSuccessors(currState):
            if i[0] not in exp and i[0] not in qStates: #o folosesc ca sa nu adaug duplicate
                q.push( (i[0], path + [i[1]]) )      
    return [] 


def uniformCostSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    path= []           
    currState =  problem.getStartState()    

    pq=PriorityQueue()
    pq.push((currState, path,0),0) 
    exp=set()   
    #pqStates=set()
    
    while not pq.isEmpty():
        currState, path,cost = pq.pop()    
        if problem.isGoalState(currState): #vad daca o adaug la solutia finala
            return path
        if(currState not in exp):
           exp.add(currState)
           pqStates=[]
           for j in pq.heap:
             pqStates.append(j[0]) #append la toata tupla cu currState,path si costul
           for i in problem.getSuccessors(currState):
             if i[0] not in exp and i[0] not in pqStates: #o folosesc ca sa nu adaug duplicate
                pq.push( (i[0], path + [i[1]],cost+i[2]),cost+i[2])  
             else:
                pq.update((i[0],path + [i[1]],cost+i[2]),cost+i[2])
    return []



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    path= []           
    currState =  problem.getStartState()    

    pq=PriorityQueue()
    pq.push((currState, path,0),0+heuristic(currState,problem)) 
    exp=set()   
    
    while not pq.isEmpty():
        currState, path,cost = pq.pop()    
        if problem.isGoalState(currState): #vad daca o adaug la solutia finala
            return path
        if(currState not in exp):
           exp.add(currState)
           pqStates=[]
           for j in pq.heap:
             pqStates.append(j[0]) #append la toata tupla cu currState,path si costul
           for i in problem.getSuccessors(currState):
             newCost=cost+i[2]
             priority=newCost+heuristic(i[0],problem)
             if i[0] not in exp and i[0] not in pqStates: #o folosesc ca sa nu adaug duplicate
                pq.push( (i[0], path + [i[1]],newCost),priority)  
             else:
                pq.update((i[0],path + [i[1]],newCost),priority)
    return []
   


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

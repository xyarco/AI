# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def graph_search(problem, fringe):
    """Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue.
    If two paths reach a state, only use the best one. [Fig. 3.18]"""
    closed = {}
    path = []
    parentMap = {}
    flipper = util.Stack()
    for element in problem.getSuccessors(problem.getStartState()):
        fringe.push(element)
        state, direction, cost = element
        parentMap[element] = problem.getStartState()
    while fringe:
        parent = fringe.pop()
        parent_state, direction, cost = parent

        #print("!!!", parent_state, direction, cost)

        if problem.isGoalState(parent_state):
            curr = parent
            previous = None
            while(curr in parentMap.keys()):
                flipper.push(curr)
                curr = parentMap[curr]
                previous = curr
            while not flipper.isEmpty():
                state, direction, cost = flipper.pop()
                path.append(direction)
            print("Final path: ", path)
            return path
        if parent not in closed:
            closed[parent] = True
            children = problem.getSuccessors(parent_state)
            for child in children:
                fringe.push(child)
                if child not in parentMap:
                    parentMap[child] = parent   
                    print child
    return None


def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
   
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  
  return graph_search(problem, util.Stack())

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  
  return graph_search(problem, util.Queue())
      
def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    closed = {}
    path = []
    parentMap = {}
    flipper = util.Stack()

    pq = util.PriorityQueue()
    costMap = {}

    #print("***", problem.getStartState())

    for element in problem.getSuccessors(problem.getStartState()):
        state, direction, cost = element
        costMap[state] = cost
        pq.push(element, cost)
        parentMap[element] = problem.getStartState()

    while pq:
        parent = pq.pop()
        parent_state, direction, cost = parent

        if problem.isGoalState(parent_state):
            curr = parent
            while (curr in parentMap.keys()):
                flipper.push(curr)
                curr = parentMap[curr]
            while not flipper.isEmpty():
                state, direction, cost = flipper.pop()
                path.append(direction)
            print("Final path: ", path)
            return path

        if parent not in closed:
            closed[parent] = True
            children = problem.getSuccessors(parent_state)
            for child in children:
                state, direction, cost = child
                tempCost = costMap[parent_state] + cost
                if state in costMap:
                    if tempCost >= costMap[state]:
                        continue
                costMap[state] = tempCost
                pq.push(child, costMap[state])
                if child not in parentMap:
                    parentMap[child] = parent
                    print child
    return None

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    closed = {}
    path = []
    parentMap = {}
    flipper = util.Stack()

    pq = util.PriorityQueue()
    costMap = {}

    for element in problem.getSuccessors(problem.getStartState()):
        state, direction, cost = element
        costMap[state] = heuristic(state, problem)
        pq.push(element, costMap[state] + cost)
        parentMap[element] = problem.getStartState()

    while pq:
        parent = pq.pop()
        parent_state, direction, cost = parent

        if problem.isGoalState(parent_state):
            curr = parent
            while (curr in parentMap.keys()):
                flipper.push(curr)
                curr = parentMap[curr]
            while not flipper.isEmpty():
                state, direction, cost = flipper.pop()
                path.append(direction)
            print("Final path: ", path)
            return path

        if parent not in closed:
            closed[parent] = True
            children = problem.getSuccessors(parent_state)
            for child in children:
                state, direction, cost = child
                tempCost = costMap[parent_state] + cost
                if state in costMap:
                    if tempCost >= costMap[state]:
                        continue
                costMap[state] = tempCost
                pq.push(child, costMap[state] + heuristic(state, problem))
                if child not in parentMap:
                    parentMap[child] = parent
                    print child
    return None




  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

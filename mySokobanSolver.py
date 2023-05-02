
'''

Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban

taboocells = []


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [[(11247282), 'Bismillah'], [10601171, 'Lucas', 'Ferreira']]

# - - - - - - - - - - - - - - - - AUXULLARY FUNCTIONS- - - - - - - - - - - - - - - - - - - - - - -


taboocells = []




def taboo_cells(warehouse: sokoban.Warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''

    global taboocells

    walls = warehouse.walls

    # get the maximum x and y coordinates of the warehouse, this will be the last warehouse wall 

    max_x, max_y = max(x for x, y in walls), max(y for x, y in walls)

    # from (0, 0) get all the cells that are not walls

    non_walls = [(x, y) for x in range(max_x + 1) for y in range(max_y + 1) if (x, y) not in walls]

    outside_cells = set()

    # if any cell's coordinate is lower or greater than the minimum and maximum coodinate for each row, then that cell is an outside cell   
    # create dictionary with row numbers as keys and lists of x-coordinates as values

    rows = {y: [x for x, y_ in walls if y_ == y] for y in set(y for x, y in walls)}

    # create dictionary with column numbers as keys and lists of y-coordinates as values

    columns = {x: [y for x_, y in walls if x_ == x] for x in set(x for x, y in walls)}


    # get the minmum and maximum coordinate wall coordinates for each row and column

    for x, y in non_walls:
        if x > max(rows[y]) or x < min(rows[y]):
            outside_cells.add((x, y))

        if y > max(columns[x]) or y < min(columns[x]):
            outside_cells.add((x, y))

    # inside cells are cells that are not outside cells

    inside_cells = [cell for cell in non_walls if cell not in outside_cells]


    # corners are cells that are inside cells and have a wall on two sides
    # that is a wall on the left and right or a wall on the top and bottom
    # and are not target cells

    corners = []
    
    for (x, y) in inside_cells:
        if (x, y) not in warehouse.targets:
            if (x - 1, y) in walls and (x, y - 1) in walls:
                corners.append((x, y))
                taboocells.append((x, y))
            elif (x + 1, y) in walls and (x, y - 1) in walls:
                corners.append((x, y))
                taboocells.append((x, y))
            elif (x - 1, y) in walls and (x, y + 1) in walls:
                corners.append((x, y))
                taboocells.append((x, y))
            elif (x + 1, y) in walls and (x, y + 1) in walls:
                corners.append((x, y))
                taboocells.append((x, y))

    # two corners along a wall have taboo cells between them if none of the cells are target cells
    # and there is a wall on either side of the cells
    
    # for every ith corner, check the entire list if there is a corner with the same x-coordinate, which means they are on the same row
    
    for i in range(len(corners)):
        for j in range(len(corners)):
            if corners[i][0] == corners[j][0]:
                # if they are on the same row, check if there are any cells between them that are not target cells
                # and if there is a continuous wall on either side of the cell. If there is, then that cell is a taboo cell
                for y in range(corners[i][1] + 1, corners[j][1]):
                    if (corners[i][0], y) not in warehouse.targets and (corners[i][0], y) not in walls:
                        if all((corners[i][0] - 1 , y_) in walls for y_ in range(corners[i][1], corners[j][1])) or all((corners[i][0] + 1, y_) in walls for y_ in range(corners[i][1], corners[j][1])):
                            taboocells.append((corners[i][0], y))


            # if they are on the same column, check if there are any cells between them that are not target cells
            # and if there is continuous wall on either side of the cell. If there is, then that cell is a taboo cell
            elif corners[i][1] == corners[j][1]:
                for x in range(corners[i][0] + 1, corners[j][0]):
                    if (x, corners[i][1]) not in warehouse.targets and (x, corners[i][1]) not in walls:
                        if all((x_, corners[i][1] - 1) in walls for x_ in range(corners[i][0], corners[j][0])) or all((x_, corners[i][1] + 1) in walls for x_ in range(corners[i][0], corners[j][0])):
                            taboocells.append((x, corners[i][1]))

    # the the initial warehouse string and replace all the new line characters with empty strings

    warehouse_string = warehouse.__str__().replace('\n', '')

    # get the index of the taboocells and replace the cells with 'X' in the warehouse string

    for taboocell in taboocells:
        pos = taboocell[1] * warehouse.ncols + taboocell[0]
        warehouse_string = warehouse_string[:pos] + 'X' + warehouse_string[pos + 1:]

    # remove the worker, boxes and targets from the string
    warehouse_string = warehouse_string.replace('@', ' ').replace('$', ' ').replace('.', ' ').replace('*', ' ')

    # return the warehouse string
    return warehouse_string

 
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

################ auxuallary classes #########################


class extend_Node(search.Node):

    """
    An extended version of the Node class that keeps track of the weight of the boxes
    """
    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)

        # box : (weight, moved)
        self.box_weight = {}
    

    def set_box_weight(self, box_coordinates):
        """
        Given a list of box coordinates, of the form [(x1, y1), (x2, y2), ...], which corresponds to the coordinates of the boxes in the node.
        Set the box_weight dictionary of the node to be of the form {box_coordinate : (weight, moved), ...}

        (NOTE : I didn't want to implement the get box coordinate function directly into the node class because it copies it for every node, which is not efficient)
        """

        # if parent is None, then the node is the initial state, so all the boxes are not moved

        # otherwise
        if self.parent:
            # for every box in the current node boxes
            for box in box_coordinates:
                # if the box is in the parent, then the box is not moved
                if box in self.parent.box_weight:
                    self.box_weight[box] = (self.parent.box_weight[box][0], False) # weight = weight of the box in the parent, moved = False
                else:
                # if the box is not in the parent, then the box is moved
                    for parent_box in self.parent.box_weight:
                        if parent_box not in box_coordinates:
                            self.box_weight[box] = (self.parent.box_weight[parent_box][0], True) # weight = weight of the box in the parent, moved = True
                            break
    
    def get_moved_box_weight(self):
        if self.parent:
            print(self.parent.box_weight)
        
        print(self.box_weight)
        
        for box in self.box_weight:
            if self.box_weight[box][1]:
                return self.box_weight[box][0]
        
        return None
    

        


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''

    
    def __init__(self, warehouse: sokoban.Warehouse):
        '''
        The initial state is the initial text representation of the warehouse.
        
        The goal state is the text representation of the warehouse with all the target cells replaced with boxes.

        In the goal state, the position of the worker is irrelevant. As long as the boxes are in the right places,
        and the worker has achieved it through a sequence of legal moves, the puzzle is solved.
        '''

        self.warehouse = warehouse

        # make the warehouse into a single string, and remove the new line character

        str_warehouse = warehouse.__str__().replace('\n', '')
        initial = str_warehouse
        
        goal = initial.replace('$', ' ').replace('.', '*').replace('@', ' ')

        initial = extend_Node(initial)
        
        for weight, box in zip(warehouse.weights, warehouse.boxes):
            initial.box_weight[box]  = (weight, False)
        
        goal = extend_Node(goal)

        super().__init__(initial, goal)
        

    def get_box_coordinate(self, state: str):
        '''
        Return the x and y cordinates of the boxes in state 

        @param state: A valid string representation of a state

        @return
            A list of cordinates for the boxes (either on a target or not) in the given state

        '''
        box_coordinates = []
        for i in range(len(state)):
            if state[i] == '$' or state[i] == "*":
                y, x = divmod(i, self.warehouse.ncols)
                box_coordinates.append((x, y))
        return box_coordinates

    

    def actions(self, state: search.Node):
        
        '''
        Return the list of legal actions that can be executed in the given state. 

        @param state: A valid state

        @return
            Return a list of possible moves that do not result in the worker object being places in a wall
        '''
        
        # index of the @ symbol in the state string
        
        playerposition = state.state.index('@')
        
        L = []  # list of legal actions

        # returns the coordinate of the agent in the current state        
        y, x = divmod(playerposition, self.warehouse.ncols)

        previousPlayerPosition = (x, y)


        # generate a list of legal moves (it can go anywhere expect into the walls)

        # When the agent is inside the warehouse and there is no wall to its left, it can move left
        if (x - 1, y) not in self.warehouse.walls:
            L.append("Left")
        
        # Right
        if (x + 1, y) not in self.warehouse.walls:
            L.append("Right")

        # Up
        if (x, y - 1) not in self.warehouse.walls:
            L.append("Up")
        
        # Down
        if (x, y + 1) not in self.warehouse.walls:
            L.append("Down")
        
        return L


    def result(self, state: search.Node, action):

        '''

        Returns the state that corresponds to the inputted action (as long as it is valid), including moving a box. 

        @param node: A valid node

        @param action: An action which does not allow the player to be in a wall

        @return
            Return a new node to be searched that contains a string representation of the result of the action

        '''

        #Extract box positions
        boxes = []

        boxStateAnalysis = state.state
        
        boxes = self.get_box_coordinate(boxStateAnalysis)

        #Move the player based on the action

        #To move the player we need to get the players current position
        
        playerPreviousPositionStr = state.state.index('@')
        y, x = divmod(playerPreviousPositionStr, self.warehouse.ncols)
        playerPreviousCordinates = (x, y)

        #Check which action was called
        if action == "Left":
            #Update the players position
            playerCordinates = (playerPreviousCordinates[0] - 1, playerPreviousCordinates[1])
        elif action == "Right":
            playerCordinates = (playerPreviousCordinates[0] + 1, playerPreviousCordinates[1])
        elif action == "Up":
            playerCordinates = (playerPreviousCordinates[0], playerPreviousCordinates[1] - 1)
        elif action == "Down":
            playerCordinates = (playerPreviousCordinates[0], playerPreviousCordinates[1] + 1)


        #Check to see if a box will need to be moved
        if playerCordinates in boxes:
            #then a box was moved

            boxCordinates = playerCordinates
            newBoxCordinates = None

            if action == "Left":
                #we need to check if the box can be pushed to the left
                newBoxCordinates = (boxCordinates[0] - 1, boxCordinates[1])

            elif action == "Right":
                newBoxCordinates = (boxCordinates[0] + 1, boxCordinates[1]) 

            elif action == "Up":
                newBoxCordinates = (boxCordinates[0], boxCordinates[1] - 1)

            elif action == "Down":
                newBoxCordinates = (boxCordinates[0], boxCordinates[1] + 1)

                
            #check to see if the new boxes position is in a wall, in another box or in a taboo cell
            if newBoxCordinates not in self.warehouse.walls and newBoxCordinates not in boxes and newBoxCordinates not in taboocells:


                currentState = state.state
                nextState = None

                #Convert the cordinates into a string position so we can update the text reprsentation
                playerPositionStr = playerCordinates[1] * self.warehouse.ncols + playerCordinates[0]
                boxNewPositionStr = newBoxCordinates[1] * self.warehouse.ncols + newBoxCordinates[0]
                boxPreviousPositionStr = boxCordinates[1] * self.warehouse.ncols + boxCordinates[0]


               
                #update state to reflect next state
                nextState = currentState[:playerPreviousPositionStr] + ' ' + currentState[playerPreviousPositionStr + 1:]
                #Check if the move has uncovered a target or if player has stepped off a target
                if playerPreviousCordinates in self.warehouse.targets and playerCordinates != playerPreviousCordinates:
                    #if they have moved then we need to highkight the space is open again
                    nextState = nextState[:playerPreviousPositionStr] + '.' + nextState[playerPreviousPositionStr + 1:]


                nextState = nextState[:boxPreviousPositionStr] + ' ' + nextState[boxPreviousPositionStr + 1:]
                nextState = nextState[:playerPositionStr] + '@' + nextState[playerPositionStr + 1:]
                
                if newBoxCordinates in self.warehouse.targets:
                    nextState = nextState[:boxNewPositionStr] + '*' + nextState[boxNewPositionStr + 1:]
                else:
                    nextState = nextState[:boxNewPositionStr] + '$' + nextState[boxNewPositionStr + 1:]



            else:
                #if the new boxes position is valid we need to move it in the warehouse object and update the string representation

                #if it is we need to move it back
                newBoxCordinates = boxCordinates

                #we can then update the state and return it

                currentState = state.state
                nextState = currentState

        elif playerCordinates in self.warehouse.walls:  

                currentState = state.state
                nextState = currentState

        else:   
                currentState = state.state
                nextState = None

                #Convert the cordinates into a string position so we can update the text reprsentation
                playerPositionStr = playerCordinates[1] * self.warehouse.ncols + playerCordinates[0]

                #update state to reflect next state
                nextState = currentState[:playerPreviousPositionStr] + ' ' + currentState[playerPreviousPositionStr + 1:]
                if playerPreviousCordinates in self.warehouse.targets and playerCordinates != playerPreviousCordinates:
                    #if they have moved then we need to highkight the space is open again
                    nextState = nextState[:playerPreviousPositionStr] + '.' + nextState[playerPreviousPositionStr + 1:]

                nextState = nextState[:playerPositionStr] + '@' + nextState[playerPositionStr + 1:]
                

        
        newNode = extend_Node(nextState)
        newNode.parent = state
        newNode.action = action
        newNode.set_box_weight(self.get_box_coordinate(nextState))
        newNode.path_cost = self.path_cost(state.path_cost, state, action, newNode)
        return newNode 


    def goal_test(self, node: search.Node):
        '''
    
        Determines whether the current state is the goal state or not

        @param node: A valid node

        @return
            If the current node's string representation matches the goal state's string representation returns true, indicating the searching algorithm has found the goal
        '''

        teststate = node.state.replace('@', ' ')

        if teststate == self.goal.state:
            return True    


    def path_cost(self, c, state1: extend_Node, action, state2: extend_Node):

        '''
    
        Determines the cost of moving from one state to the next, including when pushing boxes.
            
        @param c: the previous node's cost

        @param state1: a valid state to move from (usually the current state)

        @param state2: a valid state to move to (usually the next state)
            
        @return
            Depending on the players actions, returns the cost of moving from state1 to state2. If the player has not moved the previous node's cost is returned.
            If the worker has moved but not pushed a box return the previous node's cost + 1. Finally if the worker has pushed a box, return the cost of the previous node + 1 
            (for walking) + the cost of moving the box (weight)
        '''


        # if the player hasn't moved

        if state1.state == state2.state:
            return c

        # if the player has moved but not pushed a box
        elif state1.get_moved_box_weight() == None:
            return c + 1
        
        # if the player has moved and pushed a box

        else:
            return c + 1 + state1.get_moved_box_weight()

            

    
    def h(self, n: extend_Node):
        '''
        create a heuristic function that estimates the cost of the cheapest path from the state at node n to a goal state.
        '''

        return 0



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse: sokoban.Warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''


    walls = warehouse.walls

    boxes = warehouse.boxes

    pz = SokobanPuzzle(warehouse)

    state = pz.initial

    #Inital state check
    playerposition = state.state.index("@")
    y, x = divmod(playerposition, warehouse.ncols)
    playerposition = (x, y)

    #check if player position is in a wall or box if the move is made

    if playerposition in walls or playerposition in boxes:
        return "Impossible"


    for move in action_seq:

        previousPlayerPosition = playerposition        
        #move to next state
        state = pz.result(state, move)

        #update boxes, incase any have been moved
        box_coordinates = []
        for i in range(len(state.state)):
            if state.state[i] == '$' or state.state[i] == "*":
                y, x = divmod(i, warehouse.ncols)
                box_coordinates.append((x, y))

        #extract the players cordinates for the move that has just occured

        playerposition = state.state.index("@")
        y, x = divmod(playerposition, warehouse.ncols)
        playerposition = (x, y)

        #check if player position is in a wall or box if the move is made

        if playerposition in walls or playerposition in box_coordinates or playerposition == previousPlayerPosition:
            return "Impossible"
        
    
    result = ""

    for i in range(0, len(state.state), warehouse.ncols):
        result += state.state[i:i + warehouse.ncols] + "\n"
    return result
                    



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse: sokoban.Warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''

    pz = SokobanPuzzle(warehouse)

    taboo_cells(warehouse)
    
    sol = search.astar_graph_search(pz)

 

    if sol:
        return sol.solution(), sol.path_cost
    else:
        return "Impossible"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def print_puzzle(state):
    '''
    A function that returns the state of the puzzle in string format

    @param
     state: a valid state object
    
    '''
    result = ""

    for i in range(0, len(state), wh.ncols):
        result += state[i:i + wh.ncols] + "\n"

    print(result)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# TESTING

if __name__ == "__main__":
    wh = sokoban.Warehouse()

    wh.load_warehouse("./warehouses/warehouse_5n.txt")


    pz = SokobanPuzzle(wh)

    print(solve_weighted_sokoban(wh))
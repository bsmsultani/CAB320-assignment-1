
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

################ auxuallary function #########################


class TrackWeight(object):

    '''
    Tracks the weight of the boxes in the warehouse as the worker moves the boxes around.

    The weight of the boxes is stored in a dictionary with the state of the warehouse as the key and the value is a list of tuples.

    Each tuple contains the coordinates of the box, the weight of the box and a boolean value that indicates whether the box has been moved or not
    to reach the state it is in.
    '''
    
    # the initial node is the initial state of the warehouse and the initial weight is the weight of the boxes in the initial state
    # the number of columns is the number of columns in the warehouse string which is used to calculate the coordinates of the boxes

    def __init__(self, initial_node: str, initial_weight: list, numberOfColumns: int):
        self.numberOfColumns = numberOfColumns
        self.track_weight = {}

        # get the coordinates of the boxes in the initial state and store them in a list of tuples with the weight of the boxes
        # and set moved to false since the boxes have not been moved yet

        initial_box_coordinates = self.__get_box_coordinates___(initial_node)
        initial_box_weight = []

        for idx, box in enumerate(initial_box_coordinates):
            weight = initial_weight[idx]
            initial_box_weight.append((box, weight, False))
        

        initial_node = initial_node.replace('@', ' ').replace('.', ' ')
        self.track_weight[initial_node] = initial_box_weight
    
    def get_weight(self, state: str) -> list:
        '''
        Given a state of the warehouse, return the weight of the boxes in the warehouse
        as a list of tuples (weight, box, moved)
        '''
        state = state.replace('@', ' ').replace('.', ' ')
        
        if state in self.track_weight:
            return self.track_weight[state]
        else:
            return None
        
        
    def get_moved_box_weight(self, state: str):
        '''
        Given a state of the warehouse, return the weight of the box that was moved to reach the state
        '''
        state = state.replace('@', ' ').replace('.', ' ')
        if state in self.track_weight:
            # return the weight of the moved box
            return [weight for (box, weight, moved) in self.track_weight[state] if moved][0]
        else:
            return None
        
    def set_weight(self, state1: str, state2: str, newBoxCordinates: tuple):

        """
        Given two states of the warehouse, update the weight of the boxes in the second state.
        Determine the weight of the boxes in the second state by comparing the boxes in the first state and the second state.
        """
        
        # get the box coordinates and the weights of the boxes in the state1
        box_coordinate = self.__get_box_coordinates___(state1)
        # get the weight of the boxes in the state1
        state_weights = self.get_weight(state1)

        # get the box coordinates in the state2
        
        next_state_box_coordinates = self.__get_box_coordinates___(state2)
        next_state_box_weights = []

        # for each box in the state1, check if the box is in the state2. If it is, then the weight of the box in the state2 is the 
        # same as the weight of the box in the state1

        for idx, box in enumerate(box_coordinate):
            weight = state_weights[idx][1]
            if box in next_state_box_coordinates:
                next_state_box_weights.append((box, weight, False))

            # if the box is not in the state2, then the box has been moved to a new location.
            else:
                next_state_box_weights.append((newBoxCordinates, weight, True))

        state2Str = state2.replace('@', ' ').replace('.', ' ')

        self.track_weight[state2Str] = next_state_box_weights


    
    def __get_box_coordinates___(self, state: str):
        """
        Allows the user to get the coordinates of the boxes given a state of the warehouse.
        """

        box_coordinates = []
        for i in range(len(state)):
            if state[i] == '$' or state[i] == "*":
                y, x = divmod(i, self.numberOfColumns)
                box_coordinates.append((x, y))
        return box_coordinates
    
    def __contains__(self, node: str ):

        """
        Returns true if the state of the warehouse is in the track_weight dictionary
        """
        return node.replace('@', ' ').replace('.', ' ') in self.track_weight

        
class extend_Node(search.Node):
    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)
        self.track_weight = {}
        


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
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

        super().__init__(search.Node(initial), search.Node(goal))

        self.weight_tracker = TrackWeight(initial, self.warehouse.weights, self.warehouse.ncols)
    

    def actions(self, state: search.Node):
        
        '''
        Return the list of legal actions that can be executed in the given state.
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

        Function description:

        Return the state that results from executing the given action in the given state.

        The state is altered by moving the agent in the given direction, if that direction is legal.

        The movement of the agent may also cause the agent to push a box. Therefore we need to check if the agent is pushing a box.

        Then we also need to update the cost of new state. THIS IS THE ONLY PART THAT IS NOT IMPLEMENTED YET.

        '''

        #Extract box positions
        boxes = []
        numOfUnsolvedBoxes = state.state.count('$')

        boxStateAnalysis = state.state

        for box in range(numOfUnsolvedBoxes):
            boxPositionStr = boxStateAnalysis.index('$')
            boxStateAnalysis = boxStateAnalysis[:boxPositionStr] + ' ' + boxStateAnalysis[boxPositionStr + 1:]
            y, x = divmod(boxPositionStr, self.warehouse.ncols)
            boxPositionCordinates = (x, y)
            boxes.append(boxPositionCordinates)


        numOfSolvedBoxes = state.state.count('*')

        for box in range(numOfSolvedBoxes):
            boxPositionStr = boxStateAnalysis.index('*')
            boxStateAnalysis = boxStateAnalysis[:boxPositionStr] + ' ' + boxStateAnalysis[boxPositionStr + 1:]
            y, x = divmod(boxPositionStr, self.warehouse.ncols)
            boxPositionCordinates = (x, y)
            boxes.append(boxPositionCordinates)

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


                # if the current state's weight is not in the weight tracker then we can calculate the weight of the new state
                if state.state in self.weight_tracker:
                    self.weight_tracker.set_weight(state.state, nextState, newBoxCordinates)

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
                

        
        newNode = search.Node(nextState)
        newNode.parent = state
        newNode.action = action
        newNode.path_cost = self.path_cost(state.path_cost, state, action, newNode)
        return newNode 


    def goal_test(self, node: search.Node):
        '''
        Return True if the state is a goal state or False, otherwise.
        '''

        teststate = node.state

        teststate = teststate.replace('@', ' ')

        if teststate == self.goal.state:
            return True    


    def path_cost(self, c, state1: search.Node, action, state2: search.Node):
    
        '''
        Return the cost of a solution path that arrives at state2 from state1 via action, assuming cost c to get up to state1.

        The cost of an action is 1 + weight of the box pushed, if any.
        '''

        # get state2 weight from the weight tracker

        # if the player hasn't moved

        if state1.state == state2.state:
            return c

        # if the player has moved but not pushed a box
        elif state1.state.replace('@', ' ').replace('.', ' ') == state2.state.replace('@', ' ').replace('.', ' '):
            return c + 1
        
        # if the player has pushed a box
        else:
            return c + 1 + self.weight_tracker.get_moved_box_weight(state2.state)

            

    
    def h(self, n):
        '''
        create a heuristic function that estimates the cost of the cheapest path from the state at node n to a goal state.
        '''

        state = n.state.state
        targets = self.warehouse.targets.copy()
        # get the coordinates of the boxes as well as their weights
        box_weights = [(coordinate, weight) for (coordinate, weight, moved) in self.weight_tracker.get_weight(state)]

        # sort box in ascending order of weight
        box_weights.sort(key=lambda x: x[1], reverse=True)

        def manhattan_distance(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        # iterate through the boxes and find the closest target for each box and add it to the list 
        # as a tuple of (box, closest target)

        closest_box_target = []

        for box in box_weights:
            box_coordinate = box[0]

            # find the closest target for the box
            closest_target = None
            closest_target_distance = float('inf')

            for target in targets:
                target_distance = manhattan_distance(box_coordinate, target)

                if target_distance < closest_target_distance:
                    closest_target = target
                    closest_target_distance = target_distance

            # add box : target

            closest_box_target.append((box, closest_target))


            # remove the target from the list of targets

            targets.remove(closest_target)

        
        total_weight_to_solve = 0

        # iterate through the list of closest box : target tuples and calculate the total distance from the box to the target and multiply it by the weight of the box
        # to get the total weight to solve
        # also add a penalty for any other box that is closer to the target than the current box
        # this is to prevent the agent from pushing a box to the closest target
        # that is not the target for that box

        for i in range(len(closest_box_target)):
            box = closest_box_target[i][0][0]
            weight = closest_box_target[i][0][1]
            target = closest_box_target[i][1]

            # add the distance from the box to the target to the total distance

            total_weight_to_solve += manhattan_distance(box, target) * weight

            # if any other box is closer to the target than the current box, add a penalty to the total distance

            for j in range(0, len(closest_box_target)):
                other_box = closest_box_target[j][0][0]
                other_weight = closest_box_target[j][0][1]
                other_target = closest_box_target[j][1]

                if manhattan_distance(other_box, target) < manhattan_distance(box, target) and other_box != box:
                    total_weight_to_solve += manhattan_distance(other_box, target) * weight


        return total_weight_to_solve
            
            



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


    ## Situations which are illegal: Box in wall, pushing 2 boxes, player in wall, player in a box

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

        #update boxes, incase any have been moved
        boxes = warehouse.boxes
        
        #move to next state
        state = pz.result(state, move)

        #extract the players cordinates for the move that has just occured

        playerposition = state.state.index("@")
        y, x = divmod(playerposition, warehouse.ncols)
        playerposition = (x, y)

        #check if player position is in a wall or box if the move is made

        if playerposition in walls or playerposition in boxes:
            return "Impossible"
                    



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

    # if the weights are the same, use breadth first search
    
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

    # CHANGE THIS TO TEST DIFFERENT WAREHOUSES, FOR EXAMPLE:

    # time how long it takes to solve a warehouse

    wh.load_warehouse("./warehouses/warehouse_31.txt")

    pz = SokobanPuzzle(wh)

    print(solve_weighted_sokoban(wh))

    print_puzzle(pz.initial.state)

    print_puzzle(taboo_cells(wh))
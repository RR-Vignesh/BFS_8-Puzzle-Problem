# Importing the required packages
import numpy as np
import copy

## initializing the variable types
optimal_path = []
visited_nodes_list = []
node_path = {}
nodes_list = []
initial_state = []
goal_state = []

# File handle to access the files for creating .. Opened in write mode
file_nodepath = open('nodePath.txt', 'w')
file_nodes = open('Nodes.txt' , 'w')
file_nodeinfo = open('NodesInfo.txt','w')

## This function returns the node info (Node index, Parent index and the corresponding matrix/state) which is later written to the text file
def nodes_info(visited_nodes, node_path_values, init_state):
    nodes_info = []
    for i in visited_nodes:
        if i == init_state:
            continue
        else:
            child_node_index = visited_nodes.index(i)
            goal_val = tuple([tuple(x) for x in i])
            key_val = node_path_values.get(goal_val)
            key_val = visited_nodes.index(list([list(x) for x in key_val]))
            nodes_info.append([child_node_index, key_val, i])
    return nodes_info

# Function to initialize the matrix
def init_matrix(rows, columns):                                   
    mat = np.empty((3,3), dtype=int)
    for i in range(0,rows):
        for j in range(0,columns):
            mat[i][j] = int(input())

    return mat.tolist()

optimal_path = []
# Function for backtracking from Goal state to initial state
def back_tracking(path, initial_state, current_node):
    initial_state = tuple([tuple(x) for x in initial_state])
    current_node = tuple([tuple(x) for x in current_node])
    optimal_path.append(current_node)
    parent_path = tuple([tuple(i) for i in current_node])
    optimal_path.append(parent_path)
    while parent_path != initial_state:  
        parent_path = path[parent_path]
        optimal_path.append(parent_path)
    
    optimal_path.reverse()
    return optimal_path, len(optimal_path)

# Function to move the blank tile along left side
def ActionMoveLeft(mat,x,y):
    modified_state = copy.deepcopy(mat)
    dummy = modified_state[x][y-1]
    modified_state[x][y-1] = modified_state[x][y]
    modified_state[x][y] = dummy
    
    if modified_state not in visited_nodes_list:
        visited_nodes_list.append(modified_state)
        nodes_list.append(modified_state)
        prev_node = tuple([tuple(i) for i in mat])
        curr_node = tuple([tuple(j) for j in modified_state])
        node_path[curr_node] = prev_node
    
    if modified_state != goal_state:
        return False
    else:
        return True

# Function to move the blank tile along right side
def ActionMoveRight(mat,x,y):
    modified_state = copy.deepcopy(mat)
    dummy = modified_state[x][y+1]
    modified_state[x][y+1] = modified_state[x][y]
    modified_state[x][y] = dummy
    if modified_state not in visited_nodes_list:
        visited_nodes_list.append(modified_state)
        nodes_list.append(modified_state)
        prev_node = tuple([tuple(i) for i in mat])
        curr_node = tuple([tuple(j) for j in modified_state])
        node_path[curr_node] = prev_node
    
    if modified_state != goal_state:
        return False
    else:
        return True

# Function to move the blank tile upward
def ActionMoveUp(mat,x,y):
    modified_state = copy.deepcopy(mat)
    dummy = modified_state[x-1][y]
    modified_state[x-1][y] = modified_state[x][y]
    modified_state[x][y] = dummy
    if modified_state not in visited_nodes_list:
        visited_nodes_list.append(modified_state)
        nodes_list.append(modified_state)
        prev_node = tuple([tuple(i) for i in mat])
        curr_node = tuple([tuple(j) for j in modified_state])
        node_path[curr_node] = prev_node
    
    if modified_state != goal_state:
        return False
    else:
        return True

# Function to move the blank tile downward
def ActionMoveDown(mat,x,y):
    modified_state = copy.deepcopy(mat)
    dummy = modified_state[x+1][y]
    modified_state[x+1][y] = modified_state[x][y]
    modified_state[x][y] = dummy
    if modified_state not in visited_nodes_list:
        visited_nodes_list.append(modified_state)
        nodes_list.append(modified_state)
        prev_node = tuple([tuple(i) for i in mat])
        curr_node = tuple([tuple(j) for j in modified_state])
        node_path[curr_node] = prev_node
    
    if modified_state != goal_state:
        return False
    else:
        return True

# Function to find the blank tile in the matrix
def findBlankTile(matrix):                                
    for i in range(0,3):
        for j in range(0,3):
            if matrix[i][j]==0:
                return i,j

r = int(input("Enter the number of rows:"))
c = int(input("Enter the number of columns:"))

print("Enter the initial state in column wise")
initial_state = init_matrix(r,c)
print("The initial state matrix is : ")
print(initial_state)


print("Enter the goal state in column wise")
goal_state = init_matrix(r,c)
print("The goal state matrix is : ")
print(goal_state)  

## Appending the initial state
nodes_list.append(initial_state)

# appending the initial state to visited node since it is the first parent root node.
visited_nodes_list.append(initial_state)

status = False
while True: 
    transition_node = nodes_list.pop(0)
    zero_x, zero_y = findBlankTile(transition_node)
    if transition_node != goal_state:
        if status != True:
            if zero_x+1 < 3:
                status = ActionMoveDown(transition_node, zero_x, zero_y)
        if status != True:
            if zero_x-1 >= 0:
                status = ActionMoveUp(transition_node, zero_x, zero_y)
        if status != True:
            if zero_y+1 < 3:
                status = ActionMoveRight(transition_node, zero_x, zero_y)
        if status != True:
            if zero_y-1 >= 0:
                status = ActionMoveLeft(transition_node, zero_x, zero_y)

    else:
        ## Goal reached here. So going to check the backtracking data from goal node back to parent root node
        backtracking_data, length = back_tracking(node_path, initial_state, transition_node)
        print("The path of backtracking is as follows :")
        print(type(backtracking_data))
        
        # Capturing the node path and writing to corresponding file
        for path_val in backtracking_data:
            temp_1 = list(map(list, path_val))
            temp_2 = list(np.concatenate(temp_1))
            temp_3 = ' '.join(str(i) for i in temp_2)
            file_nodepath.write(temp_3)
            file_nodepath.write('\n')

        print(type(visited_nodes_list)) 
        ## Capturing the nodes and writing to nodes.txt file
        for i in visited_nodes_list:
            temp_a = list(map(list, i))
            temp_b = list(np.concatenate(temp_a))
            temp_c = ' '.join(str(i) for i in temp_b)
            print(temp_c)
            file_nodes.write(str(temp_c))
            file_nodes.write("\n")
        
        print("The number of nodes while backtracking is :")
        print(length)
        print("Final Goal Reached: ", transition_node)
        print("The number of nodes visited are :")
        print(len(visited_nodes_list))
        print("The node path is :")
        print(node_path)

        node_info_data = nodes_info(visited_nodes_list, node_path, initial_state)
        node_info_value =[]
        for i in node_info_data:
            visited_nodes_val = list(map(list, i[2]))
            nodes_concatenated = np.concatenate(visited_nodes_val)
            node_joined = " ".join(str(i) for i in nodes_concatenated)
            index = str(i[0])
            parent_index = str(i[1])
            node_info_final = index +"     "+parent_index+"     "+node_joined
            node_info_value.append(node_info_final)
        
        file_nodeinfo.write('\n'.join('%s' % a for a in node_info_value))

        file_nodeinfo.close()
        break



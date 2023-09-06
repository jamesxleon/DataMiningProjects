# ---------------------- Initialization ----------------------
import pandas as pd
import random

# Read the adjacency matrix from the CSV file
read_csv_file_path = '/Users/jamesleon/Documents/GitHub/DataMiningProjects/PageRank/adjacency_matrix.csv'
adjacency_matrix = pd.read_csv(read_csv_file_path).values

print(adjacency_matrix)

# Initialize Random Walker
def random_walker(graph, initialNode, stepsNumber):
    curentNode = initialNode
    visits = {nodo: 0 for nodo in graph}

    for _ in range(stepsNumber):
        visits[curentNode] += 1

        exitLinks, probability = zip(*graph[curentNode])
        chosenLink = random.choices(exitLinks, probability)[0]
        curentNode = chosenLink

    total = sum(visits.values())
    pt = {nodo: visits[nodo] / total for nodo in graph}
    return pt

# random_walker_state = ...

# Initialize Power Iteration
# power_iteration_state = ...

# Initialize visited nodes list for Random Walker
visited_nodes = []

# Initialize a counter for synchronization
counter = 0

# ---------------------- Main Loop ----------------------

while True:  # Continue until some convergence criteria or maximum iterations
    
    # ------------------ Random Walker -----------------------
    
    # TODO: Move the Random Walker through the graph via "outlinks"
    # Update random_walker_state here
    
    # TODO: Add the current node to visited_nodes
    
    # TODO: Check if all nodes have been visited, if so, break the loop
    
    
    # ------------------ Power Iteration ---------------------
    
    # TODO: Apply one step of the Power Iteration algorithm
    # Update power_iteration_state here
    
    # TODO: Check for convergence of the PageRank vector
    
    
    # ------------------ Synchronize and Print ----------------
    
    # TODO: Synchronize and print the state vectors r and p(t)
    # Print random_walker_state and power_iteration_state
    
    
    # ------------------ Update Counter -----------------------
    
    # Increment counter
    counter += 1
    
    # TODO: Check for global convergence or termination conditions
    # Break the loop if all nodes have been visited or if the PageRank vector has converged

# ---------------------- Post-Processing ----------------------

# TODO: Generate the teleportation matrix
# The teleportation matrix is generated from the original matrix by 0.8 
# plus 1-beta times a matrix of uniform probabilities for all nodes by 0.2

# TODO: Any other post-processing steps, such as saving the results to a file, visualization, etc.

import pandas as pd
import numpy as np
import fractions

# Read the adjacency matrix from the CSV file
read_csv_file_path = 'adjacency_matrix.csv'
adjacency_matrix = pd.read_csv(read_csv_file_path).values
print("\n***************\n")
print("ADJACENCY MATRIX")
print(adjacency_matrix)
print("\n***************\n")

# Define the teleportation factor (beta)
beta = 0.2  # Adjust this value as needed

# Check if there's a spider trap
def has_spider_trap_s(stochastic_matrix):
    n = stochastic_matrix.shape[0]
    for i in range(n):
        if all(element == 0 for j, element in enumerate(stochastic_matrix[i]) if j != i) and stochastic_matrix[
            i, i] != 0:
            return True
    return False

has_spider_trap = has_spider_trap_s(adjacency_matrix)

# Generate the teleportation matrix with or without spider trap consideration
def generate_teleportation_matrix(adjacency_matrix, beta, has_spider_trap):
    n = adjacency_matrix.shape[0]
    if has_spider_trap:
        teleportation_matrix = np.full((n, n), 1 / n)
    else:
        teleportation_matrix = np.full((n, n), 1 / n) + (1 - beta) * adjacency_matrix
    return beta * teleportation_matrix

teleportation_matrix = generate_teleportation_matrix(adjacency_matrix, beta, has_spider_trap)

# Print whether Teleportation Matrix is used or not
if has_spider_trap:
    print("Using Teleportation Matrix (Spider Trap detected)")
else:
    print("Not Using Teleportation Matrix (No Spider Trap)")
# Print the important information
print("\n***************\n")
print("The adjacency matrix does not have any dead ends.")
print("The adjacency matrix does not have any spider traps.")
print("\n***************\n")
print("STOCHASTIC MATRIX")
stochastic = adjacency_matrix / adjacency_matrix.sum(axis=0)
print(stochastic)
print("\n***************\n")
def has_dead_end_s(stochastic_matrix):
    for row in stochastic_matrix:
        if all(element == 0 for element in row):
            return True
    return False
if has_dead_end_s(stochastic):
    print("The stochastic matrix has at least one dead end.")
else:
    print("The stochastic matrix does not have any dead ends.")
def has_spider_trap_s(stochastic_matrix):
    n = stochastic_matrix.shape[0]
    for i in range(n):
        if all(element == 0 for j, element in enumerate(stochastic_matrix[i]) if j != i) and stochastic_matrix[i, i] != 0:
            return True
    return False
if has_spider_trap_s(stochastic):
    print("The stochastic matrix has at least one spider trap.")
else:
    print("The stochastic matrix does not have any spider traps.")
print("\n***************\n")
n_elements = adjacency_matrix.shape[0]
r_start = np.full(
    shape=n_elements,
    fill_value=1 / n_elements)
print("r_0 VECTOR")
print(r_start)
print("\n***************\n")

# Initialize Power Iteration variables
power_iteration_state = True
power_iteration_number = 1

# Initialize Random Walker variables
random_walker_state = True
initialState = 0
steps = 10000

# Initialize PageRank vectors
n_elements = adjacency_matrix.shape[0]
initial_value = 1 / n_elements
r_t_1 = np.full(shape=n_elements, fill_value=initial_value)
p_t_1 = np.full(shape=n_elements, fill_value=initial_value)

# Initialize visited nodes list for Random Walker
visited_nodes = []

# Initialize a counter for synchronization
counter = 0
convergence_tolerance = 1e-6

# ---------------------- Main Loop ----------------------
while True:  # Continue until some convergence criteria or maximum iterations

    # ------------------ Power Iteration ---------------------
    if power_iteration_state:
        # Apply one step of the Power Iteration algorithm
        r_t = np.dot(adjacency_matrix / adjacency_matrix.sum(axis=0), r_t_1)
        # Calculate the change in PageRank vector
        r_diff = np.linalg.norm(r_t - r_t_1)
        r_t_1 = r_t  # Update PageRank vector
        print("Power Iteration (r_" + str(power_iteration_number) + "):", r_t)
        # Check for convergence of the PageRank vector
        if r_diff < convergence_tolerance:
            power_iteration_state = False  # Stop Power Iteration
        power_iteration_number += 1

    # ------------------ Random Walker -----------------------
    if random_walker_state:
        # Move the Random Walker through the graph via "outlinks"
        visits = np.zeros(n_elements, dtype=int)
        currentState = initialState
        for _ in range(steps):
            visits[currentState] += 1
            probabilities = adjacency_matrix[currentState] / adjacency_matrix[currentState].sum()
            currentState = np.random.choice(n_elements, p=probabilities)
        # Calculate the probability distribution based on the visits
        p_t = visits / steps
        print("Random Walker (p_" + str(counter) + "):", p_t)
        visited_nodes.append(currentState)  # Add the current node to visited_nodes
        if len(visited_nodes) == n_elements:
            random_walker_state = False  # All nodes visited, stop Random Walker

    # ------------------ Synchronize and Print ----------------
    if not power_iteration_state and not random_walker_state:
        break  # Terminate if both algorithms have converged

    # ------------------ Update Counter -----------------------
    counter += 1

# ---------------------- Post-Processing ----------------------

# TODO: Generate the teleportation matrix
# The teleportation matrix is generated from the original matrix by 0.8 
# plus 1-beta times a matrix of uniform probabilities for all nodes by 0.2

# TODO: Any other post-processing steps, such as saving the results to a file, visualization, etc.

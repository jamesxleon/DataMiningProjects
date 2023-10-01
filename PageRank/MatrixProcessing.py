# ---------------------- Initialization ----------------------
import pandas as pd
import numpy as np
import json
import random 

# Read the adjacency matrix from the CSV file
read_csv_file_path = "/Users/jamesleon/Documents/GitHub/DataMiningProjects/PageRank/final_matrix.csv"

adjacency_matrix = pd.read_csv(read_csv_file_path).values

# Visualize the graph
#visualize_adjacency_matrix(adjacency_matrix) in Matrix.py

N = len(adjacency_matrix)

# Initialize variables for both Random Walker and Power Iteration
initial_state = random.randint(0, N-1)
current_state = initial_state
visited_nodes = []

r_start = np.full(shape=N, fill_value=1 / N)

# Run the Power Iteration with simulated user input for teleportation
r_t_1 = r_start

# Initialize convergence variables
CONVERGENCE_THRESHOLD = 0.01
CONVERGENCE_TOLERANCE = 1e-6
STATE_PROB_DIFF = 1
R_DIFF = 1

# Initialize lists to keep track of state probabilities and r vectors at each time step
state_probabilities = []
r_values = []

# Initialize teleportation probability
TELEPORT_PROB = 0

# Initialize a list to keep track of teleport decisions
teleport_decisions = []

# Initialize COUNTER for synchronization
COUNTER = 0

# ---------------------- Pre-Processing ---------------------- 
# Function to generate the stochastic matrix from the adjacency matrix
def generate_stochastic_matrix(adjacency_matrix):

    outlink_sums_local = adjacency_matrix.sum(axis=1)
    
    # Handle the case where the sum of outlinks is zero (dead ends)
    # Replace zero sums with 1 to avoid division by zero
    outlink_sums_local[outlink_sums_local == 0] = 1
    
    stochastic_matrix_local = adjacency_matrix / outlink_sums_local[:, np.newaxis]
    
    return stochastic_matrix_local, outlink_sums_local

stochastic_matrix, outlink_sums = generate_stochastic_matrix(adjacency_matrix)

print("Stochastic Matrix: \n{}\nOutlink Sums: \n{}\n".format(stochastic_matrix, outlink_sums))

# Function to move the Random Walker to the next state based on transition matrix and current state
def move_random_walker(matrix, current_state, TELEPORT_PROB):
    outlinks = np.nonzero(matrix[:, current_state])[0]
    if random.random() < TELEPORT_PROB or len(outlinks) == 0:
        next_state = random.randint(0, N-1)
    else:
        next_state = random.choice(outlinks)
    return next_state

# ---------------------- Main Loop --------------------------------
# Run both Random Walker and Power Iteration in the same loop until both converge

# Crear un diccionario para guardar la trazabilidad
trace_dict = {}

# Ejecutamos el algoritmo nuevamente, esta vez guardando la trazabilidad en el diccionario
while STATE_PROB_DIFF > CONVERGENCE_THRESHOLD or R_DIFF > CONVERGENCE_TOLERANCE:
    
    # --------------------------- Random Walker ---------------------------
    next_state = move_random_walker(stochastic_matrix, current_state, TELEPORT_PROB)
    visited_nodes.append(next_state)
    new_state_prob = np.array([visited_nodes.count(i)/len(visited_nodes) for i in range(N)])
    
    if len(state_probabilities) > 0:
        STATE_PROB_DIFF = np.sum(np.abs(new_state_prob - state_probabilities[-1]))
        
    state_probabilities.append(new_state_prob.tolist())
    current_state = next_state


    # --------------------------- Power Iteration ---------------------------
    if COUNTER % 10 == 0 and COUNTER != 0 and COUNTER % 20 != 0:
        print(f"\n=== Iteración {COUNTER} ===")
        
        user_input = ""

        while user_input not in ['Y', 'N']:
            user_input = input("Do you wish to teleport? (Y/N): ").strip().upper()
            if user_input == 'Y':
                do_teleport = True
                print("Teleporting...")
                print(f"Do teleport: {do_teleport}")
                print(f"Norma de la diferencia del vector r: {R_DIFF}")
                print(f"Diferencia en probabilidades de estado: {STATE_PROB_DIFF}")
                teleport_decisions.append(do_teleport)
                
                teleport_vector = np.full(shape=N, fill_value=1 / N)
                r_t = (1 - TELEPORT_PROB) * np.dot(stochastic_matrix, r_start) + TELEPORT_PROB * teleport_vector
                                
            elif user_input == 'N':
                do_teleport = False
                print("Teleportion cancelled")
                r_t = np.dot(stochastic_matrix, r_start)
                print(f"Do teleport: {do_teleport}")
                print(f"Norma de la diferencia del vector r: {R_DIFF}")
                print(f"Diferencia en probabilidades de estado: {STATE_PROB_DIFF}")
            else:
                print("Invalid input. Please enter Y or N.")



    else: 
        do_teleport = random.choice([True, False])
        teleport_decisions.append(do_teleport)
        
        if do_teleport or any(outlink_sum == 0 for outlink_sum in outlink_sums):
            teleport_vector = np.full(shape=N, fill_value=1 / N)
            r_t = (1 - TELEPORT_PROB) * np.dot(stochastic_matrix, r_start) + TELEPORT_PROB * teleport_vector
        else:
            r_t = np.dot(stochastic_matrix, r_start)
        
    R_DIFF = np.linalg.norm(r_t - r_start)
    r_start = r_t
    r_values.append(r_t.tolist())


    # Incrementar CONTADOR
    COUNTER += 1

    # Guardar trazabilidad en el diccionario
    trace_dict[COUNTER] = {
        'do_teleport': do_teleport,
        'current_state_probabilities': new_state_prob.tolist(),
        'current_r_vector': r_t.tolist()
    }

    # Imprimir algunos datos representativos en el terminal
    if COUNTER % 500 == 0 or COUNTER == 1:
        print(f"\n=== Iteración {COUNTER} ===")
        print(f"Do teleport: {do_teleport}")
        print(f"Norma de la diferencia del vector r: {R_DIFF}")
        print(f"Diferencia en probabilidades de estado: {STATE_PROB_DIFF}")

    # Guardar valores del vector para ver la convergencia
    csv_file_path = "/Users/jamesleon/Documents/GitHub/DataMiningProjects/PageRank/convergence.csv"

    with open(csv_file_path, 'w') as f:
        pd.DataFrame(r_values).to_csv(csv_file_path, index=False)

# Guardar la trazabilidad en un archivo JSON
trace_file_path = "/Users/jamesleon/Documents/GitHub/DataMiningProjects/PageRank/trace.json"

with open(trace_file_path, 'w') as f:
    json.dump(trace_dict, f, indent=4)

# Imprimir las probabilidades de estado finales y el vector PageRank final
print("\n=== Resultados Finales ===")
print(f"Probabilidades de Estado Finales: \n{new_state_prob}")
print(f"Vector PageRank Final: \n{r_t}")
print(f"Total de Iteraciones: {COUNTER}")
print(f"La trazabilidad completa ha sido guardada en {trace_file_path}")

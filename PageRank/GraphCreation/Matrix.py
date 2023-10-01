# Import required libraries 
import random
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

# Function to add dead ends
def add_dead_ends(matrix, num_dead_ends):
    dead_ends = random.sample(range(N), num_dead_ends)
    for i in dead_ends:
        matrix[i, :] = 0
    return dead_ends

# Function to add complex spider traps
def add_complex_spider_traps(matrix, num_spider_traps, dead_ends):
    spider_trap_sets = []
    for _ in range(num_spider_traps):
        available_nodes = [i for i in range(N) if i not in dead_ends and all(i not in trap_set for trap_set in spider_trap_sets)]
        trap_size = random.randint(3, min(5, len(available_nodes)))
        trap_nodes = random.sample(available_nodes, trap_size)
        for i in range(trap_size):
            matrix[trap_nodes[i], trap_nodes[(i + 1) % trap_size]] = 1
        spider_trap_sets.append(trap_nodes)
    return spider_trap_sets

# Function to fill remaining cells randomly
def fill_remaining(matrix, dead_ends, spider_traps):
    for i in range(N):
        if i not in dead_ends and i not in spider_traps:
            outlinks = random.sample(range(N), random.randint(1, N))
            matrix[i, outlinks] = 1

# Function to visualize adjacency matrix as a graph
def visualize_adjacency_matrix(adjacency_matrix):
    G = nx.DiGraph()
    num_nodes = adjacency_matrix.shape[0]
    G.add_nodes_from(range(num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adjacency_matrix[i, j] > 0:
                G.add_edge(i, j)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', font_size=18, node_size=700, font_color='black')
    plt.show()

# Initialize graph parameters
N = 15
#adjacency_matrix = np.zeros((N, N), dtype=int)

# Generate the adjacency matrix
#dead_ends = add_dead_ends(adjacency_matrix, 2)
#spider_traps = add_complex_spider_traps(adjacency_matrix, 1, dead_ends)
#fill_remaining(adjacency_matrix, dead_ends, [node for trap_set in spider_traps for node in trap_set])

# Visualize the graph
#visualize_adjacency_matrix(adjacency_matrix)

#print(adjacency_matrix, "\n", dead_ends, "\n",spider_traps)

# Write the adjacency matrix to a CSV file

#csv_file_path = '/Users/jamesleon/Documents/GitHub/DataMiningProjects/PageRank/final_matrix.csv'
#with open(csv_file_path, 'w') as f:
#    pd.DataFrame(adjacency_matrix).to_csv(csv_file_path, index=False)
 
# Read the adjacency matrix from the CSV file and visualize it
read_csv_file_path = '/Users/jamesleon/Documents/GitHub/DataMiningProjects/PageRank/final_matrix.csv'
adjacency_matrix = pd.read_csv(read_csv_file_path).values
visualize_adjacency_matrix(adjacency_matrix)

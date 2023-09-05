import numpy as np
import random
import pandas as pd

# Initialize N and create an N x N matrix filled with zeros
N = 10
adjacency_matrix = np.zeros((N, N), dtype=int)

# Function to add dead ends
def add_dead_ends(matrix, num_dead_ends):
    dead_ends = random.sample(range(N), num_dead_ends)
    for i in dead_ends:
        matrix[i, :] = 0
    return dead_ends

# Function to add spider traps
def add_spider_traps(matrix, num_spider_traps):
    spider_traps = random.sample([i for i in range(N) if i not in dead_ends], num_spider_traps)
    for i in spider_traps:
        matrix[i, :] = 0
        matrix[i, i] = 1
    return spider_traps

# Function to fill remaining cells randomly
def fill_remaining(matrix):
    for i in range(N):
        if i not in dead_ends and i not in spider_traps:
            outlinks = random.sample(range(N), random.randint(1, N))
            matrix[i, outlinks] = 1

# Add 3 dead ends
dead_ends = add_dead_ends(adjacency_matrix, 3)

# Add 3 spider traps
spider_traps = add_spider_traps(adjacency_matrix, 3)

# Fill the remaining cells
fill_remaining(adjacency_matrix)

print(adjacency_matrix, "\n", dead_ends, "\n",spider_traps)

# Write the adjacency matrix to a CSV file
csv_file_path = '/Users/jamesleon/Documents/GitHub/DataMiningProjects/PageRank/adjacency_matrix.csv'
with open(csv_file_path, 'w') as f:
    pd.DataFrame(adjacency_matrix).to_csv(csv_file_path, index=False)

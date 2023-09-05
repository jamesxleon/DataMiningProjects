# Proyecto 1: Word counting using Python

## Parallelism and Distributed computing

### Notes:

`PageRank` is the active project.

### GraphCreation Folder

**This is a code to generate a random NxN adjacency matrix (now set to N=10) with a given number of dead ends and spider traps (now set to 6)**

## Outcoming Work

### Power Iteration (Sebastián & Nicole)

- You'll be creating the ranking r vector representing the convergency of the importance for a given i web page given the M matrix read from a CSV

### Random Walker (Nicolás & Daniel)

- You'll be creating the p(t) vector representing the out probability from each page
- This should lead to a stationary probability

### Synchronization (James)

- Once both algorithms are up and running, I'll make them work side-by-side

### Check Global convergence or termination conditions (Sebastián & Nicole)

- You'll be suggesting the termination conditions for the rank and implementing it

### Post processing (Nicolás & Daniel)

- Do the teleportation matrix and save the results

# A Guidance on how to advance within each step is provided in the MatrixProcessing.py file
**Here's how I'd do each step of the process, btw**  
**Random Walker**
The idea of a Random Walker is to simulate a random walk through the graph. At each node i, the walker will move to one of its neighbors randomly, as specified by the adjacency matrix.

Here's a guide to implementing this:

Move Through Graph: Given the current node, identify its outlinks from the adjacency matrix. Move to one of these outlinked nodes randomly.
Update State: Update the state vector to reflect the current position of the random walker.
Visited Nodes: Keep a list of visited nodes. This will help you track where the walker has been and will be useful for the termination condition.

**Power Iteration**
Power Iteration is used to find the dominant eigenvector of the adjacency matrix, which, in this context, represents the PageRank score.

Normalize Columns: Before applying power iteration, make sure to normalize the columns of the adjacency matrix so that they sum to 1. This creates a stochastic matrix.
Iterate: Apply the power iteration update rule: P_new=Matrix × P_old
Normalize: Normalize the new P so it sums to 1.(You can choose wheter to use L1 norm or L2 norm here, but make sure to have some reason to support your decision)

**Synchronization**
Once you have both algorithms working independently, you can synchronize them within the main loop. The idea is to run one step of each algorithm per iteration of the loop, printing or storing the states at each step.

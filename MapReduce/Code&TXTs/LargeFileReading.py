from queue import Queue
import threading
from collections import Counter
import re
import os
import random
import json

# Function to simulate random node failure
def simulate_failure(probability=0.1):
    return random.random() < probability


# Function to split a large file into smaller chunks
def split_file_into_chunks(file_path, chunk_size=20*1024*1024):  # Default chunk size is 20MB
    
    file_size = os.path.getsize(file_path)
    num_chunks = file_size // chunk_size + bool(file_size % chunk_size)
    
    chunks = []
    
    with open(file_path, 'r') as f:
        for i in range(num_chunks):
            chunk_file_path = f"{file_path}_chunk_{i+1}.txt"
            with open(chunk_file_path, 'w') as chunk_file:
                chunk_data = f.read(chunk_size)
                chunk_file.write(chunk_data)
            chunks.append(chunk_file_path)
    
    return chunks

# Function to clean and tokenize text (Map function)
def map_function(chunk_file):
    with open(chunk_file, "r") as f:
        #replace non-alphanumeric characters with spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', f.read())
        #replace newlines with spaces
        text = re.sub(r'\n', ' ', text)
        #replace tabs with spaces
        text = re.sub(r'\t', ' ', text)
        #replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        words = text.lower().split()
    word_count = Counter(words)
    return word_count

# Function to reduce word counts (Reduce function)
def reduce_function(word_counts):
    total_count = Counter()
    for wc in word_counts:
        total_count += wc
    return total_count

# Coordinator Node
class Coordinator:
    def __init__(self, chunk_files, num_map_nodes=4, num_reduce_nodes=2):
        self.chunk_files = chunk_files
        self.num_map_nodes = num_map_nodes
        self.num_reduce_nodes = num_reduce_nodes
        self.map_output_queue = Queue()
        self.reduce_output_queue = Queue()
        self.map_nodes = []
        self.reduce_nodes = []
        
    def assign_map_tasks(self):
        for i, chunk_file in enumerate(self.chunk_files):
            t = threading.Thread(target=self.map_task, args=(chunk_file, i+1,))
            self.map_nodes.append(t)
            t.start()
            
    def map_task(self, chunk_file, task_id):
        print(f"Map Task {task_id} processing {chunk_file}")
        result = map_function(chunk_file)
        self.map_output_queue.put(result)
        print(f"Map Task {task_id} completed")
            
    def assign_reduce_tasks(self):
        map_results = [self.map_output_queue.get() for _ in range(self.num_map_nodes)]
        for i in range(self.num_reduce_nodes):
            # Splitting map_results into parts for each reduce node
            start_idx = i * len(map_results) // self.num_reduce_nodes
            end_idx = (i + 1) * len(map_results) // self.num_reduce_nodes
            part_map_results = map_results[start_idx:end_idx]
            
            t = threading.Thread(target=self.reduce_task, args=(part_map_results, i+1,))
            self.reduce_nodes.append(t)
            t.start()
            
    def reduce_task(self, part_map_results, task_id):
        print(f"Reduce Task {task_id} started")
        result = reduce_function(part_map_results)
        self.reduce_output_queue.put(result)
        print(f"Reduce Task {task_id} completed")
    
    def execute(self):
        print("Coordinator: Starting Map phase")
        self.assign_map_tasks()
        for t in self.map_nodes:
            t.join()
        
        print("Coordinator: Starting Reduce phase")
        self.assign_reduce_tasks()
        for t in self.reduce_nodes:
            t.join()
            
        print("Coordinator: Aggregating final results")
        final_results = reduce_function([self.reduce_output_queue.get() for _ in range(self.num_reduce_nodes)])
        return final_results

# Improved Coordinator Node with fault tolerance and intermediate result storage
class ImprovedCoordinator(Coordinator):
    def map_task(self, chunk_file, task_id):
        if simulate_failure():
            print(f"Map Task {task_id} failed")
            return
        
        print(f"Map Task {task_id} processing {chunk_file}")
        result = map_function(chunk_file)
        
        # Save intermediate result to file
        with open(f"/mnt/data/map_output_task_{task_id}.json", "w") as f:
            json.dump(result, f)
            
        self.map_output_queue.put(result)
        print(f"Map Task {task_id} completed")
            
    def reduce_task(self, part_map_results, task_id):
        if simulate_failure():
            print(f"Reduce Task {task_id} failed")
            return
        
        print(f"Reduce Task {task_id} started")
        result = reduce_function(part_map_results)
        
        # Save intermediate result to file
        with open(f"/mnt/data/reduce_output_task_{task_id}.json", "w") as f:
            json.dump(result, f)
            
        self.reduce_output_queue.put(result)
        print(f"Reduce Task {task_id} completed")
            

# Test the function
if __name__ == "__main__":

    file_path = 'MapReduce/Code&TXTs/large_file.txt'
    small_file_path = 'MapReduce/Code&TXTs/small_file.txt'

    # Split the sample file into chunks
    chunk_files = split_file_into_chunks(file_path)  
    chunk_files

    # Initialize Improved Coordinator and execute
    improved_coordinator = ImprovedCoordinator(chunk_files=chunk_files, num_map_nodes=4, num_reduce_nodes=2)
    final_word_count = improved_coordinator.execute()
    final_word_count.most_common(10)  # Show top 10 most common words as example


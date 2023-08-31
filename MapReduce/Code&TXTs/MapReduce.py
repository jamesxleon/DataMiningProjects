import threading
from queue import Queue
from functools import reduce
import pandas as pd
import re
import os


def clean_text(file):
    
    with open(file, "r") as f:
        #replace non-alphanumeric characters with spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', f.read())
        #replace newlines with spaces
        text = re.sub(r'\n', ' ', text)
        #replace tabs with spaces
        text = re.sub(r'\t', ' ', text)
        #replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)

    #save cleaned text to clean_text.txt
    with open("clean_text.txt", "w") as f:
        f.write(text)


# Master Node
def map_reduce(file_name, chunk_size, num_map_nodes, num_reduce_nodes):
    # Read the file
    with open(file_name, "r") as f:
        file_content = f.read()

    # Split the file content into chunks
    chunks = [file_content[i:i+chunk_size] for i in range(0, len(file_content), chunk_size)]
    
   

    # Create queues for mappers and reducers
    map_input_queue = Queue()
    map_output_queue = Queue()
    reduce_output_queue = Queue()

    # Populate map input queue
    for i, chunk in enumerate(chunks):
        map_input_queue.put((i, chunk))

    # Create and start mapper threads
    map_threads = []
    for i in range(num_map_nodes):
        t = threading.Thread(target=map_node, args=(map_input_queue, map_output_queue, chunk_size))
        map_threads.append(t)
        t.start()

    # Wait for mappers to finish
    for t in map_threads:
        t.join()

    # Collect mapper results
    map_results = []
    while not map_output_queue.empty():
        map_results.append(map_output_queue.get())

    # Create and start reducer threads
    reduce_threads = []
    for i in range(num_reduce_nodes):
        t = threading.Thread(target=reduce_node, args=(map_results, reduce_output_queue))
        reduce_threads.append(t)
        t.start()

    # Wait for reducers to finish
    for t in reduce_threads:
        t.join()

    # Collect reducer results
    reduced_results = []
    while not reduce_output_queue.empty():
        reduced_results.append(reduce_output_queue.get())

    # Combine results from all reducers
    final_result = reduce(chunk_word_combining, reduced_results)
    

    return final_result

# Mapper Node
def map_node(map_input_queue, map_output_queue,chunk_size):
    while not map_input_queue.empty():
        i, chunk = map_input_queue.get()
        map_output_queue.put(chunk_word_counting(chunk))
        #Obtain the size of each chunk in mb
        chunk_size_inbytes = len(chunk.encode('utf-8'))*8
        chunk_size_tomb = chunk_size_inbytes / (1024 * 1024)
        
        print("Mapping chunk", i, "Size:", chunk_size_tomb, "mb")
        
        
        

# Reducer Node
def reduce_node(map_results, reduce_output_queue):
    # Do something to pick appropriate chunks to reduce together
    # For now, just combine all results using the chunk_word_combining function
    reduced_result = reduce(chunk_word_combining, map_results)
    reduce_output_queue.put(reduced_result)

# Count words in a chunk
def chunk_word_counting(chunk):
    words = chunk.split()
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

# Combine word counts from multiple chunks
def chunk_word_combining(count1, count2):
    for word, count in count2.items():
        if word in count1:
            count1[word] += count
        else:
            count1[word] = count
    return count1

# Test the function
if __name__ == "__main__":
    clean_text("asyoulik.txt")
               
    file_name = "clean_text.txt" # Replace with your actual file name

    chunk_size = 1024  # Size of each chunk in bytes
    num_map_nodes = 5  # Number of map nodes
    num_reduce_nodes = 2  # Number of reduce nodes

    result = map_reduce(file_name, chunk_size, num_map_nodes, num_reduce_nodes)
    
    resultDataframe = pd.DataFrame(result.items(), columns=['Word', 'Count'])

    print(resultDataframe.head(40))

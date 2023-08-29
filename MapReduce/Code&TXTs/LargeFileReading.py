#Divide a file in chunks and count the repetitions of each word in the file as a sum of every chunk
def word_counting_map_reduce(file_name, chunk_size):
    # Open the file
    file = open(file_name, "r")
    # Read the file
    file_content = file.read()
    # Close the file
    file.close()
    # Split the file content in chunks
    chunks = [file_content[i:i+chunk_size] for i in range(0, len(file_content), chunk_size)]
    # Map the chunks
    mapped_chunks = map(chunk_word_counting, chunks)
    # Reduce the chunks
    reduced_chunks = reduce(chunk_word_counting, mapped_chunks)
    # Return the result
    return reduced_chunks

# Path: LargeFileReading.py
# Count the repetitions of each word in a chunk
def chunk_word_counting(chunk):
    # Split the chunk in words
    words = chunk.split()
    # Count the repetitions of each word in the chunk
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    # Return the result
    return word_count

# Path: LargeFileReading.py
# Reduce the chunks
def reduce(chunk1, chunk2):
    # Count the repetitions of each word in the chunks
    word_count = {}
    for word in chunk1:
        if word in word_count:
            word_count[word] += chunk1[word]
        else:
            word_count[word] = chunk1[word]
    for word in chunk2:
        if word in word_count:
            word_count[word] += chunk2[word]
        else:
            word_count[word] = chunk2[word]
    # Return the result
    return word_count

# Path: LargeFileReading.py
# Main function
def main():
    # Get the file name
    file_name = input("Enter the file name: ")
    # Get the chunk size
    chunk_size = int(input("Enter the chunk size: "))
    # Count the repetitions of each word in the file
    word_count = word_counting_map_reduce(file_name, chunk_size)
    # Print the result
    print(word_count)

# Path: LargeFileReading.py
# Call the main function
main()
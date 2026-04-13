# Define input file and chunk size
input_file = "batches copy.js"
chunk_size = 60000  # Number of characters per chunk

def split_file_by_characters(input_path, chunk_size):
    try:
        # Read the entire content of the file as a single string
        with open(input_path, "r") as f:
            content = f.read()

        # Get the total length of the file
        total_length = len(content)
        print(f"Total characters in file: {total_length}")

        # Divide into chunks of specified size
        for i in range(0, total_length, chunk_size):
            chunk_file_name = f"chunk_{i // chunk_size}.js"
            with open(chunk_file_name, "w") as chunk_file:
                chunk_file.write(content[i:i + chunk_size])

            print(f"Created: {chunk_file_name} with characters {i} to {min(i + chunk_size, total_length) - 1}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
split_file_by_characters(input_file, chunk_size)



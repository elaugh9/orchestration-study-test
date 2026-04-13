import json

# Define input file and chunk size
input_file = "mmlu_llm_gens_copy.json"
chunk_size = 60000  # Number of characters per chunk

def split_json_file_by_characters(input_path, chunk_size):
    try:
        # Read and parse the JSON file
        with open(input_path, "r") as f:
            data = json.load(f)

        # Convert the JSON object to a string for character-based splitting
        json_string = json.dumps(data, indent=2)
        total_length = len(json_string)
        print(f"Total characters in file: {total_length}")

        # Split into chunks of specified size
        for i in range(0, total_length, chunk_size):
            chunk_file_name = f"chunk_{i // chunk_size}.json"
            chunk_content = json_string[i:i + chunk_size]
            
            # To maintain valid JSON structure, handle edge cases here if needed
            if i + chunk_size < total_length:
                print("Warning: Ensure split does not truncate JSON structure!")

            # Write the chunk to a new file
            with open(chunk_file_name, "w") as chunk_file:
                chunk_file.write(chunk_content)

            print(f"Created: {chunk_file_name} with characters {i} to {min(i + chunk_size, total_length) - 1}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
split_json_file_by_characters(input_file, chunk_size)

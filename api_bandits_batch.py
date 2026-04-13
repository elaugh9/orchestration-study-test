import json
import requests

# Input and output file names
input_file = "Final_maths_generated_batches.json"
output_file = "Final_maths_response_outcomes.json"

# Base URL and variant
base_url = "http://localhost:80"
variant = "algLinUCB_0.9"

# Load the batch data
with open(input_file, "r") as f:
    batches = json.load(f)

# Dictionary to store responses
responses = {}

# Process each batch
for batch in batches:
    user_id = batch["user_id"]
    batch_index = batch["batch_index"]

    for question in batch["questions"]:
        question_index = question["question_index"]
        answer = question["answer"]
        previous_human_response = question.get("previous_human_response", "null")
        
        # Construct the query
        query = f"{user_id}*{question_index}*{answer}*{previous_human_response}*{batch_index}*{variant}"
        url = f"{base_url}/{query}"
        
        print(f"Sending request to: {url}")

        # Send the HTTP GET request
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes (e.g., 4xx, 5xx)

            # Parse the response
            response_data = response.text.strip()  # Use `.text` to capture raw response
            print(f"Response for {query}: {response_data}")

            # Save the response along with the variant
            key = f"batch_{batch_index}_question_{question_index}"
            responses[key] = {
                "response": response_data,
                "variant": variant
            }

        except requests.RequestException as e:
            print(f"Error making request for batch {batch_index}, question {question_index}: {e}")
            key = f"batch_{batch_index}_question_{question_index}"
            responses[key] = {
                "error": str(e),
                "variant": variant
            }

# Save the responses to a file
with open(output_file, "w") as f:
    json.dump(responses, f, indent=4)

print(f"Responses saved to {output_file}")

import json
import re
import random

# Load the responses.json file
with open("Final_maths_responses.json", "r") as file:
    responses = json.load(file)

# Initialize a list to store the extracted answers
llm_answers = []

# Function to extract the answer choice
def extract_answer(response):
    # 1. Check for "Answer: (A)", "Answer: A", etc.
    match = re.search(r"\bAnswer:\s*\(?([A-D])\)?", response, re.IGNORECASE)
    if match:
        return match.group(1)

    # 2. Check for standalone "(A)", "(B)", "(C)", "(D)" in uppercase
    match = re.search(r"\(([A-D])\)", response)
    if match:
        return match.group(1)

    # 3. Check for standalone "A", "B", "C", "D" in uppercase
    match = re.search(r"\b([A-D])\b", response)
    if match:
        return match.group(1)

    # 4. If no match, assign a random answer
    return random.choice(["A", "B", "C", "D"])

# Process each response and extract the final answer
for item in responses:
    answer = extract_answer(item["response"])
    llm_answers.append(answer)

# Save the results into a JSON file
output_data = {"llm_answers": llm_answers}

with open("Final_maths_llm_answers.json", "w") as output_file:
    json.dump(output_data, output_file, indent=2)

print("Extracted answers saved to 'llm_answers.json'.")


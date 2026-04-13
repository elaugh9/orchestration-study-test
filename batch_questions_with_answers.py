import json
import random
import csv

# Load the server data file
with open("server_data_final_maths.json", "r") as server_file:
    server_data = json.load(server_file)

# Load the combined_updated.csv file
questions_data = []
with open("Final_Maths_questions_cleaned.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        questions_data.append(row)

# Load the llm_answers.json file
with open("Final_maths_llm_answers.json", "r") as llm_file:
    llm_answers = json.load(llm_file)["llm_answers"]

# Create a map of question indexes to their corresponding answers
question_index_to_answer = {}
for index, question in enumerate(questions_data):
    question_index_to_answer[index] = question["answer"]

# Generate the new JSON structure
batches = []
for batch_index, question_indexes in enumerate(server_data["examples_per_batch"]):
    batch = {
        "batch_index": batch_index,
        "user_id": f"user{random.randint(100, 999)}",
        "questions": []
    }
    
    # Process each question in the batch
    for i, q_index in enumerate(question_indexes):
        question = {
            "question_index": q_index,
            "answer": question_index_to_answer[q_index],
            "previous_human_response": None if i == 0 else llm_answers[question_indexes[i - 1]]
        }
        batch["questions"].append(question)
    
    batches.append(batch)

# Save the result to a new JSON file
with open("Final_maths_generated_batches.json", "w") as output_file:
    json.dump(batches, output_file, indent=4)

print("JSON file created: generated_batches.json")

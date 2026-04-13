import json
import csv
###### Discard this code############
# File paths
final_prompts_path = "Final_maths_final_prompts.json"
combined_updated_path = "Final_Maths_questions_cleaned.csv"
llm_answers_path = "Final_maths_llm_answers.json"
generated_batches_path = "Final_maths_generated_batches.json"
response_outcomes_path = "Final_maths_response_outcomes.json"
server_data_math_path = "server_data_final_maths.json"
questions_embeddings_path = "Final_question_embeddings.json"

# Load JSON files
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Load CSV files
def load_csv(file_path):
    with open(file_path, "r") as f:
        return list(csv.DictReader(f))

# Load all required data
final_prompts = load_json(final_prompts_path)
combined_updated = load_csv(combined_updated_path)
llm_answers = load_json(llm_answers_path)
generated_batches = load_json(generated_batches_path)
response_outcomes = load_json(response_outcomes_path)
server_data_math = load_json(server_data_math_path)
questions_embeddings = load_json(questions_embeddings_path)

# Create mappings for efficient lookup
combined_updated_mapping = {
    row["question"]: row for row in combined_updated
}
server_data_mapping = {
    str(idx): data for idx, data in server_data_math["emb_data"].items()
}

# Initialize the base structure
variant_batches = {"diff-topics": {}}

# Generate final output
for batch in generated_batches:
    batch_index = batch["batch_index"]
    variant_batches["diff-topics"][str(batch_index)] = []

    for question in batch.get("questions", []):
        question_idx = question["question_index"]
        
        # Retrieve question data
        try:
            question_data = questions_embeddings[question_idx]
        except IndexError:
            continue  # Skip if index is out of range

        question_text = question_data["question"]
        embedding_data = question_data.get("embedding", [])

        # Extract data from various sources
        prompt_data = next((p["prompt"] for p in final_prompts if question_text in p["prompt"]), None)
        combined_data = combined_updated_mapping.get(question_text, {})
        llm_answer = llm_answers.get("llm_answers", [])[question_idx] if question_idx < len(llm_answers.get("llm_answers", [])) else None
        response_data = response_outcomes.get(f"batch_{batch_index}_question_{question_idx}", {})
        server_data = server_data_mapping.get(str(question_idx), {})

        # Clean up action field by removing the trailing asterisk if present
        action_value = response_data.get("response", "")
        if action_value and action_value.endswith("*"):
            action_value = action_value[:-1]

        # Construct question entry
        entry = {
            "prompt": prompt_data,
            "label": combined_data.get("answer"),
            "example_idx": str(question_idx),
            "embedding": embedding_data,
            "llm_answer": llm_answer,
            "topic": combined_data.get("subject"),
            "question": question_text,
            "options": combined_data.get("choices"),
            "display_topic": combined_data.get("subject"),
            "z_t": server_data.get("z_t"),
            "orig_example_idx": str(question_idx),
            "action": action_value,
            "variant": response_data.get("variant"),
        }
        variant_batches["diff-topics"][str(batch_index)].append(entry)

# Save the result to a JavaScript file
output_path = "Final_maths_variant_batches.js"
with open(output_path, "w") as f:
    f.write("var variant_batches = ")
    json.dump(variant_batches, f, indent=4)

print(f"Filtered question data has been saved to {output_path}")

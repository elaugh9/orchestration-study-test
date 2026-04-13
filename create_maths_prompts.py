import csv
import json
import re

# The fixed prompt
fixed_prompt = '''The following are multiple choice questions about high_school_mathematics.
Colton and his dad bought a gallon of paint that cost $13. They also bought 2 brushes that cost $9 each. What was the total cost, not including tax, of the brushes and the paint they bought?
(A) $22, (B) $24, (C) $31, (D) $35
Answer: C
Solve for y. y – 2 + 3y = 10
(A) 2, (B) 3, (C) 4, (D) 5
Answer: B
Solve 3 over 2 * w = 66.
(A) 33, (B) 44, (C) 88, (D) 99
Answer: B
Write 5.875 as a mixed number or fraction in simplest form.
(A) 5 and 8 over 9, (B) 5 and 7 over 8, (C) 7 over 8, (D) 5 and 87 over 105
Answer: B
Solve the equation 124 = m + 34.
(A) 158, (B) 90, (C) 88, (D) 4,216
Answer: B
Zelma buys p pounds of bananas for 40 cents per pound. She pays the clerk with a twenty-dollar bill. The clerk subtracts the total cost of the bananas from the twenty-dollar bill to determine the amount of change to give Zelma. Which expression represents the amount of change Zelma should receive?
(A) p - 20, (B) 20 - 40p, (C) 20 - 0.40p, (D) 0.40p - 20
Answer: C
Please answer the following question with just the correct option (A, B, C, or D) without any explanation or additional text.
'''

def process_question(question, choices):
    """
    Formats the question and choices for inclusion in the final prompt.
    Preserves the exact formatting of the choices.
    """
    # Ensure the choices are correctly separated
    if isinstance(choices, str):
        # Extract choices, preserving formatting including parentheses and special characters
        choices = re.findall(r"\(.*?\)|'[^']+'", choices)
    
    # Format the choices as (A), (B), (C), (D)
    choices_str = ', '.join([f"({chr(65 + i)}) {choice}" for i, choice in enumerate(choices)])
    
    # Format the question
    return f"{question}\n{choices_str}\nAnswer:"

# Read the CSV file and process each question
prompts = []
with open('Final_Maths_questions_cleaned.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        question = row['question']
        try:
            # Parse choices from the CSV
            choices = row['choices']
            
            # Process the question and choices
            new_prompt = fixed_prompt + process_question(question, choices)
            prompts.append({"prompt": new_prompt})

        except Exception as e:
            print(f"Error processing question: {question}\n{e}")
            continue

# Save the result to a JSON file
with open('Final_maths_final_prompts.json', 'w') as jsonfile:
    json.dump(prompts, jsonfile, indent=2)

print(f"Processing complete. {len(prompts)} prompts have been saved to 'Final_maths_final_prompts.json'.")


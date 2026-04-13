import pandas as pd

# Read the CSV file while properly handling embedded lists and parsing
df = pd.read_csv('Final_Maths_questions.csv', quotechar='"', skipinitialspace=True)

# Create a mapping dictionary for numerical answers
answer_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

# Function to map numerical answers while leaving string answers unchanged
def map_answers(answer):
    try:
        # Attempt to convert the answer to an integer and map it
        num_answer = int(answer)
        return answer_map.get(num_answer, answer)
    except ValueError:
        # If it's not a number, return it as-is
        return answer

# Apply the mapping function to the 'answer' column
df['answer'] = df['answer'].apply(map_answers)

# Save the updated DataFrame back to CSV
df.to_csv('Final_Maths_questions_updated.csv', index=False)

print("Conversion complete. Updated file saved as 'inter_questions_updated.csv'.")

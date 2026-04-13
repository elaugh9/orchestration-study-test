import pandas as pd
import re

# Function to process LaTeX in the questions and choices
def process_latex(latex_string):
    # Loop until no more changes are made
    previous_string = ""
    
    while latex_string != previous_string:
        previous_string = latex_string
        
        # Remove all dollar signs globally
        latex_string = latex_string.replace('$', '')
        
        # Remove all backslashes globally (e.g., \frac, \alpha, \sqrt)
        latex_string = latex_string.replace('\\', '')
        
        # Replace fractions like \frac{1}{2} with 1/2
        latex_string = re.sub(r'frac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', latex_string)
    
    return latex_string

# Load the CSV file
df = pd.read_csv("Final_Maths_questions_updated.csv")

# Process the 'question' column
df['question'] = df['question'].apply(process_latex)

# Process the 'choices' column (which contains LaTeX)
df['choices'] = df['choices'].apply(lambda x: process_latex(x))

# Save the cleaned data to a new CSV file
df.to_csv("Final_Maths_questions_cleaned.csv", index=False)

print("Conversion completed. Cleaned file saved as 'Final_Maths_questions_cleaned.csv'.")



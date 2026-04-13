import csv
import re

# Function to clean LaTeX symbols from text
def clean_latex(text):
    if not isinstance(text, str):
        return text
    # Remove LaTeX-related symbols but retain necessary math symbols
    cleaned_text = re.sub(r"\\[a-zA-Z]+|[\{\}\$\^\_]|\\", "", text)
    return cleaned_text.strip()

# Input and output file paths
input_file = "combined_updated.csv"
output_file = "combined_updated_cleaned.csv"

# Read and process the CSV
with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    for row in reader:
        # Clean the question column
        row["question"] = clean_latex(row["question"])
        
        # Clean and correctly format the choices column
        if row.get("choices"):
            # Split the space-separated list and clean each choice
            raw_choices = row["choices"].strip("[]").split("' '")  # Split by "' '"
            cleaned_choices = [clean_latex(choice.strip("'")) for choice in raw_choices if choice.strip()]
            # Properly format as a list of strings with single quotes around each choice
            formatted_choices = "['" + "' '".join(cleaned_choices) + "']"
            row["choices"] = formatted_choices
        
        # Write the cleaned row
        writer.writerow(row)

print(f"Cleaned CSV saved to {output_file}")

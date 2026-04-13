import os
import pandas as pd

# Path to the extracted folder
extracted_folder = 'extracted'
# Path to the folder where the scores will be saved
scores_folder = 'scores_extracted'

# Create the 'scores_extracted' folder if it doesn't exist
if not os.path.exists(scores_folder):
    os.makedirs(scores_folder)

# Iterate through each CSV file in the 'extracted' folder
for filename in os.listdir(extracted_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(extracted_folder, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Initialize a dictionary to store the counts for each category
        category_counts = {
            'category': [],
            'correct': [],
            'total': []
        }
        
        # Group by category (topic)
        for category, group in df.groupby('topic'):
            correct_count = (group['label'] == group['response']).sum()  # Count of correct responses
            total_count = len(group)  # Total number of responses
            
            # Append the counts to the dictionary
            category_counts['category'].append(category)
            category_counts['correct'].append(correct_count)
            category_counts['total'].append(total_count)
        
        # Create a DataFrame from the category counts
        score_df = pd.DataFrame(category_counts)
        
        # Save the new DataFrame to a CSV file in the 'scores_extracted' folder
        score_file_path = os.path.join(scores_folder, filename)
        score_df.to_csv(score_file_path, index=False)

        print(f"Processed file: {filename} -> Saved to: {score_file_path}")

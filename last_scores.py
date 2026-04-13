import pandas as pd
import os

# Define the folder containing the score CSV files
scores_folder = 'scores/'

# List all CSV files in the scores folder
score_files = [f for f in os.listdir(scores_folder) if f.endswith('.csv')]

# List to store the last score values
last_scores = []

# Process each score file
for file in score_files:
    # Define the file path
    file_path = os.path.join(scores_folder, file)
    
    # Read the score CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Check if the 'score' column exists
    if 'score' in df.columns:
        # Get the last value in the 'score' column
        last_score = df['score'].iloc[-1]
        
        # Append the last score to the list
        last_scores.append(last_score)
        print(f"Last score from {file}: {last_score}")
    else:
        print(f"No 'score' column found in {file}.")

# Calculate the average of the last scores
if last_scores:
    average_score = sum(last_scores) / len(last_scores)
    print(f"\nAverage of last scores from all files: {average_score}")
    
    # Save the last scores as a DataFrame
    last_scores_df = pd.DataFrame(last_scores, columns=['Last_Score'])
    
    # Define the file path to save the last scores CSV
    output_file_path = 'scores/last_scores.csv'
    
    # Save the last scores to the CSV file
    last_scores_df.to_csv(output_file_path, index=False)
    print(f"\nLast scores saved to {output_file_path}")
else:
    print("No scores found to calculate the average.")

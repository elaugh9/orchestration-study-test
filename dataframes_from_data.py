import pandas as pd
import os

# Define the source and destination folders
data_folder = 'data/'
scores_folder = 'scores/'

# Create the scores folder if it doesn't exist
if not os.path.exists(scores_folder):
    os.makedirs(scores_folder)

# List all files in the 'data' folder
files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Process each file in the data folder
for file in files:
    # Define the file path
    file_path = os.path.join(data_folder, file)
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Check if the first column has NaN values and get the corresponding 'score' values
    nan_rows = df[df.iloc[:, 0].isna()]
    
    # Check if 'score' column exists
    if 'score' in nan_rows.columns:
        # Define the output file path for the score CSV
        output_file_path = os.path.join(scores_folder, f"scores_{file}")
        
        # Save the 'score' values where the first column is NaN to the new CSV
        nan_rows[['score']].to_csv(output_file_path, index=False)
        print(f"Scores for {file} have been saved to {output_file_path}.")
    else:
        print(f"No 'score' column found in {file}.")



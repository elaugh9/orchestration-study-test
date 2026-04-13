import os
import pandas as pd

# Path to the folder containing the processed CSV files
scores_folder = 'nli_pool_performance'

# List to hold the rows for the final table
final_data = []

# Iterate through each CSV file in the 'scores_extracted' folder
for index, filename in enumerate(os.listdir(scores_folder), start=1):
    if filename.endswith('.csv'):
        file_path = os.path.join(scores_folder, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Extract correct answers count for each category
        elementary_correct = df[df['category'] == 'elementary_mathematics']['correct'].sum() / 20
        high_school_correct = df[df['category'] == 'high_school_mathematics']['correct'].sum() / 20
        college_correct = df[df['category'] == 'college_mathematics']['correct'].sum() / 20
        
        # Append the values as a row for the final table
        final_data.append([f'user {index}', elementary_correct, high_school_correct, college_correct])

# Create a DataFrame from the final data
final_df = pd.DataFrame(final_data, columns=['user', 'elementary mathematics', 'high school mathematics', 'college mathematics'])

# Save the final DataFrame to a CSV file
final_table_path = 'final_nli_scores_table.csv'
final_df.to_csv(final_table_path, index=False)

print(f"Final table saved to: {final_table_path}")


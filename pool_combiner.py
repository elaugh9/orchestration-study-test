import pandas as pd
import os

# Define the directory containing the result CSVs
pool_dir = "nli_pool"

# Initialize an empty list to hold the data from all CSVs
all_data = []

# Loop through all CSV files in the pool folder
for filename in os.listdir(pool_dir):
    if filename.endswith(".csv"):  # Process only CSV files
        csv_path = os.path.join(pool_dir, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Append the DataFrame to the list
        all_data.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(all_data, ignore_index=True)

# Define the path for the combined CSV
combined_csv_path = os.path.join(pool_dir, "combined_results.csv")

# Save the combined DataFrame to a new CSV file
combined_df.to_csv(combined_csv_path, index=False)

print(f"All CSVs have been combined into: {combined_csv_path}")

import pandas as pd

# List of CSV files to combine
csv_files = ["combined_updated.csv", "elementary_data.csv", "college_data.csv"]

# Read all CSV files into DataFrames
dataframes = [pd.read_csv(file) for file in csv_files]

# Determine the number of rows to interleave and the total limit
chunk_size = 20  # Number of rows to take from each file in each round
max_questions = 300  # Total number of questions required

# Initialize an empty DataFrame for the combined output
combined_df = pd.DataFrame()

# Interleave rows from each DataFrame
while any(not df.empty for df in dataframes) and len(combined_df) < max_questions:
    for i, df in enumerate(dataframes):
        if not df.empty:
            # Take the first `chunk_size` rows
            chunk = df.iloc[:chunk_size]
            combined_df = pd.concat([combined_df, chunk], ignore_index=True)
            # Remove the rows that were just added
            dataframes[i] = df.iloc[chunk_size:]
            
            # Break if we reach the total question limit
            if len(combined_df) >= max_questions:
                break

# Save the interleaved DataFrame to a new CSV file
combined_df.to_csv("Final_Maths_questions.csv", index=False)

print(f"CSV files interleaved successfully into 'questions.csv' with {len(combined_df)} questions.")


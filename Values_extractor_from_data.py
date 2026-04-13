import pandas as pd
import json
import os

# Define input and output directories
input_dir = "data"
output_dir = "extracted"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get all CSV files in the data folder
csv_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]

for file in csv_files:
    input_csv_path = os.path.join(input_dir, file)
    output_csv_path = os.path.join(output_dir, f"extracted_{file}")  # Save with prefix
    
    # Load the CSV file into a dataframe
    df = pd.read_csv(input_csv_path)
    
    # Check if the dataframe has more than 280 rows
    if len(df) <= 280:
        print(f"Skipping {file} - Only {len(df)} rows (needs more than 280).")
        continue  # Skip processing this file

    # Find the column names dynamically
    topic_col = df.columns[df.columns.str.lower() == "topic"][0]  # Find "topic"
    label_col = df.columns[df.columns.str.lower() == "label"][0]  # Find "label"
    response_col = df.columns[df.columns.str.lower() == "response"][0]  # Find "response"

    # Initialize an empty list to store the extracted data
    new_data = []

    # Iterate through the dataframe row by row
    for i in range(len(df) - 1):  # Avoid index error on last row
        if df.iloc[i, 0] == "call-function":  # Check if the first column contains "call-function"
            topic = df.at[i, topic_col]  # Fetch the topic value dynamically

            # Check the next row for "survey-html-form"
            if df.iloc[i + 1, 0] == "survey-html-form":
                label = df.at[i + 1, label_col]  # Fetch label dynamically
                response_raw = df.at[i + 1, response_col]  # Fetch response dynamically

                # Extract only the answer (A, B, C, or D)
                try:
                    response_json = json.loads(response_raw)  # Convert string to dictionary
                    response = response_json.get("mcAnswer", "")  # Get the answer if it exists
                except (json.JSONDecodeError, AttributeError):  # Handle cases where it's not JSON
                    response = response_raw  # Keep original if parsing fails

                # Append extracted values to new_data list
                new_data.append([topic, label, response])

    # Create a new dataframe for the extracted data
    new_df = pd.DataFrame(new_data, columns=["topic", "label", "response"])

    # Save the new dataframe as a CSV file
    new_df.to_csv(output_csv_path, index=False)

    print(f"Extracted data saved to: {output_csv_path}")

print("Processing complete for all valid CSV files!")

import pandas as pd
import ast
import os

# Define the directories for input and output
input_dir = "data"
output_dir = "pool_new"

# Ensure the output directory exists (creates it if it doesn't)
os.makedirs(output_dir, exist_ok=True)

# Loop through all CSV files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):  # Process only CSV files
        csv_path = os.path.join(input_dir, filename)
        
        # Read the CSV into a DataFrame
        df = pd.read_csv(csv_path)

        # Check if the CSV has less than 280 rows
        if len(df) < 280:
            print(f"Skipping {filename}: File has less than 280 rows.")
            continue  # Skip processing this file if it has fewer than 280 rows

        # Initialize an empty list to store extracted rows
        extracted_data = []

        # Find the start index by searching for the first occurrence of "call-function" in the first column
        start_index = None
        for i in range(len(df)):
            if df.iloc[i, 0] == "call-function":  # Check the first column for "call-function"
                start_index = i
                break

        if start_index is None:
            print(f"Skipping {filename}: 'call-function' not found in the first column.")
            continue  # Skip this file if "call-function" is not found

        # Loop through rows starting from the found start index
        while start_index < len(df):
            try:
                # Make sure we don't go out of bounds
                if start_index + 1 < len(df):
                    topic = df.loc[start_index, "topic"]
                    response_data = df.loc[start_index + 1, "response"]
                    llm_answer = df.loc[start_index+1, "llm_answer"]
                    population_answer = df.loc[start_index+1, "population_answer"]
                
                    # Extract the mcAnswer value
                    response_dict = ast.literal_eval(response_data)  # Convert string to dictionary
                    response = response_dict.get("mcAnswer", "")  # Extract "mcAnswer" value

                    label = df.loc[start_index + 1, "label"]
                    llm_support_used = df.loc[start_index + 3, "llm_support_used"]
                    human_support_used = df.loc[start_index + 3, "human_support_used"]
                    
                    # Extract recommendation and recommendation_lists
                    recommendation = df.loc[start_index + 3, "recommendation"]
                    recommendation_lists = df.loc[start_index + 3, "recommendation_lists"]

                    # Check if any essential data is missing
                    if not topic or not response or not label:
                        print(f"Skipping row {start_index} in {filename}: Missing essential data.")
                        start_index += 5
                        continue

                    # Append all relevant data including the new columns
                    extracted_data.append([topic, llm_answer, population_answer, response, label, llm_support_used, human_support_used, recommendation, recommendation_lists])

                    start_index += 5  # Move to the next set of rows
                else:
                    break  # If there's no more data to process

            except (KeyError, SyntaxError, ValueError) as e:
                print(f"Error processing row {start_index} in {filename}: {e}")
                break  # Stop if columns are missing or response data is invalid
            except IndexError as e:
                print(f"IndexError at row {start_index} in {filename}: {e}")
                break  # Stop if index exceeds DataFrame length

        # Check if extracted data is empty (no valid rows processed)
        if not extracted_data:
            print(f"Warning: {filename} has no valid extracted data.")

        # Create a new DataFrame with extracted data
        if extracted_data:
            result_df = pd.DataFrame(extracted_data, columns=["topic", "llm_answer", "population_answer", "response", "label", "llm_support_used", "human_support_used", "recommendation", "recommendation_lists"])

            # Save the resultant CSV into the 'pool' folder
            output_path = os.path.join(output_dir, f"result_{filename}")
            result_df.to_csv(output_path, index=False)

            print(f"Processed and saved: {output_path}")
        else:
            print(f"Skipped {filename}: No valid data extracted.")

print("Extraction complete. Resultant CSVs saved in the 'pool' folder.")

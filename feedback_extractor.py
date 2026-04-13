import pandas as pd
import os

# Define the directories for input and output
input_dir = "data"  # Folder containing the CSV files
output_file = "consolidated_feedback.csv"  # Output file for consolidated feedback

# Initialize a list to store feedback data
feedback_data = []

# Loop through all CSV files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):  # Process only CSV files
        csv_path = os.path.join(input_dir, filename)
        
        # Read the CSV into a DataFrame
        df = pd.read_csv(csv_path)

        # Check if the CSV has at least one row
        if len(df) > 0:
            # Get the last row of the DataFrame
            last_row = df.iloc[-1]

            # Check if the last row contains feedback data (survey-text trial_type)
            if last_row["trial_type"] == "survey-text":
                # Extract the feedback answers
                feedback_answers = last_row["response"]

                # Parse the feedback answers (assuming it's a JSON-like string)
                try:
                    feedback_dict = eval(feedback_answers)  # Convert string to dictionary
                except:
                    feedback_dict = {}  # If parsing fails, use an empty dictionary

                # Add user information and feedback to the list
                user_data = {
                    "filename": filename,
                    "prolific_id": last_row.get("prolific_id", ""),
                    "subject": last_row.get("subject", ""),
                    **feedback_dict  # Unpack feedback answers into the dictionary
                }
                feedback_data.append(user_data)

# Create a DataFrame from the feedback data
if feedback_data:
    feedback_df = pd.DataFrame(feedback_data)

    # Save the consolidated feedback to a CSV file
    feedback_df.to_csv(output_file, index=False)
    print(f"Consolidated feedback saved to: {output_file}")
else:
    print("No feedback data found in the CSV files.")
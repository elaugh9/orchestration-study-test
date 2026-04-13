import pandas as pd
import pyarrow
import fastparquet
# Load the Parquet file
# Load the Parquet file using pyarrow explicitly
df = pd.read_parquet("test-00000-of-00001.parquet", engine="pyarrow")

# Save to CSV
df.to_csv("college_data.csv", index=False)

print("Parquet file converted to CSV!")

# List of CSV files to combine
#csv_files = ["combined_updated.csv", "elementary_data.csv"]

# Initialize an empty DataFrame
#combined_df = pd.DataFrame()

# Loop through each file and append its data to the combined DataFrame
#for file in csv_files:
#    df = pd.read_csv(file)  # Read the current CSV file
#    combined_df = pd.concat([combined_df, df], ignore_index=True)  # Append the data

# Save the combined DataFrame to a new CSV file
#combined_df.to_csv("questions.csv", index=False)

#print("CSV files combined successfully into 'combined.csv'.")


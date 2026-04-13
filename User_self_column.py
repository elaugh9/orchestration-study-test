import pandas as pd

# Load the combined_results.csv file
df = pd.read_csv('nli_pool/combined_results.csv')

# Add a new column 'user_self'
# True if both llm_support_used and human_support_used are False, otherwise False
df['user_self'] = ~(df['llm_support_used'] | df['human_support_used'])

# Save the updated DataFrame back to the original CSV (or a new file if preferred)
df.to_csv('combined_results_with_user_self.csv', index=False)

print("New column 'user_self' added successfully!")
import pandas as pd

# Load the CSV file
df = pd.read_csv("nli_pool/combined_results.csv")

# Group by topic and count occurrences of each type of support
support_counts = df.groupby("topic").agg(
    llm_support_used=("llm_support_used", "sum"),
    human_support_used=("human_support_used", "sum"),
    self_support_used=("llm_support_used", lambda x: (x == False).sum())  # Since llm_support_used and human_support_used are both False for self-support
)

# Adjust self-support calculation to ensure both supports are False
support_counts["self_support_used"] = df.groupby("topic").apply(
    lambda x: ((x["llm_support_used"] == False) & (x["human_support_used"] == False)).sum()
)

# Print results
print(support_counts)

import pandas as pd

# Path to your CSV file
csv_file_path = 'pool_new/combined_results.csv'  # Replace with the actual path

# Load the CSV data into a DataFrame
df = pd.read_csv(csv_file_path)

# Define categories and initialize counters
categories = ['elementary_mathematics', 'high_school_mathematics', 'college_mathematics']
results = {
    'overridden_and_correct': {category: 0 for category in categories},
    'followed_and_wrong': {category: 0 for category in categories},
    'overridden_and_wrong': {category: 0 for category in categories},
    'followed_and_correct': {category: 0 for category in categories},
    'would_have_helped': {category: 0 for category in categories},  # Cases where following the recommendation would have helped
    'would_have_hurt': {category: 0 for category in categories}  # Cases where following the recommendation would have hurt
}

# Function to determine if the recommendation was followed
def is_recommendation_followed(recommendation, llm_support_used, human_support_used):
    """
    Determine if the recommendation was followed based on llm_support_used and human_support_used.
    This function considers only the first three recommendations.
    """
    recommendation = recommendation.lower()

    if "attempt this problem by yourself" in recommendation:
        return not llm_support_used and not human_support_used
    elif "outsource this problem to the ai agent" in recommendation:
        return llm_support_used
    elif "outsource this problem to a human agent" in recommendation:
        return human_support_used

    return False  # Default to False for any other recommendation


# Get total unique recommendations
unique_recommendations = df['recommendation'].unique()
print("Total unique recommendations in data:")
for rec in unique_recommendations:
    print(f"- {rec}")

# Process each row in the DataFrame
for _, row in df.iterrows():
    topic = row['topic']
    response = row['response']
    label = row['label']
    recommendation = row['recommendation']
    llm_support_used = row['llm_support_used']
    human_support_used = row['human_support_used']
    llm_answer = row['llm_answer']
    population_answer = row['population_answer']
    
    # Ensure the topic is one of the valid categories
    if topic not in categories:
        continue  

    # Determine if the user's response is correct
    is_correct = (response == label)

    # Determine if the recommendation was followed
    recommendation_followed = is_recommendation_followed(recommendation, llm_support_used, human_support_used)

    # Update counters based on whether the recommendation was followed or overridden
    if not recommendation_followed and is_correct:
        results['overridden_and_correct'][topic] += 1
    elif recommendation_followed and not is_correct:
        results['followed_and_wrong'][topic] += 1
    elif not recommendation_followed and not is_correct:
        results['overridden_and_wrong'][topic] += 1
    elif recommendation_followed and is_correct:
        results['followed_and_correct'][topic] += 1

    # Check if following the recommendation would have helped
    if not recommendation_followed and not is_correct:
        if "ai agent" in recommendation.lower() and llm_answer == label:
            results['would_have_helped'][topic] += 1
        elif "human agent" in recommendation.lower() and population_answer == label:
            results['would_have_helped'][topic] += 1

    # Check if following the recommendation would have hurt
    if not recommendation_followed and is_correct:
        if "ai agent" in recommendation.lower() and llm_answer != label:
            results['would_have_hurt'][topic] += 1
        elif "human agent" in recommendation.lower() and population_answer != label:
            results['would_have_hurt'][topic] += 1

# Print the results
print("\nResults:")
for metric, counts in results.items():
    print(f"{metric}:")
    for category, count in counts.items():
        print(f"  {category}: {count}")

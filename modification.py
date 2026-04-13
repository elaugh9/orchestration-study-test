import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import run_tsne

# Load the MMLU math dataset
df = pd.read_csv('inter_questions.csv')

# Filter for high school mathematics questions
math_df = df[df['subject'] == 'high_school_mathematics']

# Create TF-IDF vectors
tfidf = TfidfVectorizer()
tfidf_vectors = tfidf.fit_transform(math_df['question'])

# Convert sparse matrix to dense array
embeddings = tfidf_vectors.toarray()

# Run t-SNE and save results
category_ids = ['high_school_mathematics'] * len(math_df)
tsne_results = run_tsne(embeddings, category_ids, output_path="mmlu_tsne_math.csv")

# Create server_data.json
server_data = {
    "emb_data": {},
    "examples_per_batch": []
}

for i, (_, row) in enumerate(math_df.iterrows()):
    server_data["emb_data"][str(i)] = {
        "z_t": tsne_results[i].tolist(),
        "y_t": row['answer']
    }

# Create 10 random batches of 60 examples each
num_questions = len(math_df)
for _ in range(10):
    batch = np.random.choice(num_questions, size=60, replace=False).tolist()
    server_data["examples_per_batch"].append(batch)

# Save server_data_math.json
with open('server_data_math.json', 'w') as f:
    json.dump(server_data, f)

print("Files generated successfully!")

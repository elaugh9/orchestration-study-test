import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import json

# Load the MMLU math dataset
#df = pd.read_csv('combined_updated.csv')
df = pd.read_csv('inter_questions_updated.csv')

# Filter for high school mathematics questions
math_df = df[df['subject'] == 'high_school_mathematics']

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to get BERT embeddings
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy().flatten()

# Generate embeddings and structure them in JSON format
questions_with_embeddings = []

for question in math_df['question']:
    embedding = get_bert_embedding(question)
    questions_with_embeddings.append({
        "question": question,
        "embedding": embedding.tolist()  # Convert to list for JSON compatibility
    })

# Save embeddings to a JSON file
with open('All_question_embeddings.json', 'w') as json_file:
    json.dump(questions_with_embeddings, json_file, indent=2)

print("Embeddings generated and saved to 'question_embeddings.json' successfully!")

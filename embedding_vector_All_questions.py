import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import json

# Load the dataset
df = pd.read_csv('Final_Maths_questions_cleaned.csv')

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

# Initialize a list to store questions and embeddings
questions_with_embeddings = []

# Process each question in the original order from the dataset
for _, row in df.iterrows():
    subject = row['subject']
    question = row['question']

    print(f"Processing question: {question[:50]}... (Subject: {subject})")

    # Generate BERT embedding for the question
    embedding = get_bert_embedding(question)
    questions_with_embeddings.append({
        "subject": subject,
        "question": question,
        "embedding": embedding.tolist()  # Convert to list for JSON compatibility
    })

# Save embeddings for all questions to a single JSON file
with open('Final_question_embeddings.json', 'w') as json_file:
    json.dump(questions_with_embeddings, json_file, indent=2)

print("Embeddings generated and saved to 'All_question_embeddings.json' successfully!")


from together import Together
import time
import os
import json

# Set your API key
API_KEY = "cfbd5902d2d7c78c2be0ba2d8ecec581e3e9deb5cde9ddbc334861516277ec1f"  # Replace with your actual API key
os.environ["TOGETHER_API_KEY"] = API_KEY

def send_prompt(prompt):
    client = Together()

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        messages=messages,
        max_tokens=512,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>", "<|eom_id|>"],
        stream=True
    )

    full_response = ""
    for token in response:
        if hasattr(token, 'choices'):
            content = token.choices[0].delta.content
            print(content, end='', flush=True)
            full_response += content

    print("\n\nFull response:")
    print(full_response)
    return full_response

# Load prompts from final_prompts.json
with open("Final_maths_final_prompts.json", "r") as file:
    prompts_data = json.load(file)

# Store responses
responses = []

# Process each prompt and get the response
for item in prompts_data:
    prompt = item["prompt"]
    print(f"\nSending prompt:\n{prompt}")
    try:
        response = send_prompt(prompt)
        responses.append({"prompt": prompt, "response": response})
    except Exception as e:
        print(f"Error processing prompt:\n{prompt}\nError: {e}")
    time.sleep(5)  # Wait 5 seconds between requests

# Save responses to a JSON file
with open("Final_maths_responses.json", "w") as response_file:
    json.dump(responses, response_file, indent=2)

print(f"\nProcessing complete. Responses saved to 'responses.json'.")

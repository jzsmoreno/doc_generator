from openai import OpenAI

from doc_generator.main import process_notebooks

# Example API call setup (replace with your actual API URL and key if needed)
api_url = "http://127.0.0.1:1234/v1"
client = OpenAI(base_url=api_url, api_key="lm-studio")
model = "granite-3.1-8b-instruct"

# Running the program
process_notebooks(client, model, "notebooks")

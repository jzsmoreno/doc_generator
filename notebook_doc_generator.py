from openai import OpenAI

from doc_generator.main import process_notebooks
from doc_generator.utils import md_to_pdf

# Example API call setup (replace with your actual API URL and key if needed)
api_url = "http://127.0.0.1:1234/v1"
client = OpenAI(base_url=api_url, api_key="lm-studio")
model = "gemma-3-4b-it"

# Running the program
markdown_file, output_pdf = process_notebooks(client, model, "notebooks")
md_to_pdf(markdown_file, output_pdf)

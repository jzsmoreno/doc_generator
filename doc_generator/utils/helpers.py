import os
import re

import nbformat
from nbconvert import MarkdownExporter

from doc_generator.prompts import prompt_for_add_comments, system_prompt


def format_text(input_string):
    cleaned_string = re.sub(r"\s+", "_", input_string.strip())
    return cleaned_string


def clean_completion_text(completion):
    response_text = completion.choices[0].message.content.strip()
    cleaned_response = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)
    # Eliminar líneas vacías o con solo espacios
    cleaned_response = re.sub(r"\n\s*\n", "\n", cleaned_response)

    # Eliminar espacios al principio y al final de cada línea
    cleaned_response = re.sub(r"^\s+|\s+$", "", cleaned_response, flags=re.MULTILINE)
    return cleaned_response


# Step 1: Load all notebooks from the 'notebooks' folder
def load_notebooks(directory="notebooks"):
    notebooks = []
    for filename in os.listdir(directory):
        if filename.endswith(".ipynb"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                notebook = nbformat.read(file, as_version=4)
                notebooks.append(notebook)
    return notebooks


# Step 2: Extract markdown and code cells from the notebook
def extract_cells(client, model, notebook):
    markdown_cells = []
    code_cells = []

    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            markdown_cells.append(cell.source)
        else:
            prompt = prompt_for_add_comments(cell.source)

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            )
            clean_response = clean_completion_text(completion)
            code_cells.append(clean_response)

    return markdown_cells, code_cells


# Step 4: Convert Jupyter Notebook to Markdown format
def convert_notebook_to_markdown(notebook):
    exporter = MarkdownExporter()
    markdown, _ = exporter.from_notebook_node(notebook)
    return markdown

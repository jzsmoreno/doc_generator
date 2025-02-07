import os

import nbformat
from nbconvert import MarkdownExporter
from openai import OpenAI
import re


# Example API call setup (replace with your actual API URL and key if needed)
api_url = "http://127.0.0.1:1234/v1"
client = OpenAI(base_url=api_url, api_key="lm-studio")
model = "deepseek-r1-distill-qwen-1.5b"


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
def extract_cells(notebook):
    markdown_cells = []
    code_cells = []

    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            markdown_cells.append(cell.source)
        else:
            code_cells.append(cell.source)

    return markdown_cells, code_cells


# Step 3: Send content (markdown + code) to an API for documentation generation
def generate_documentation_from_api(markdown_content, code_content, model=model):
    """Processes extracted content with OpenAI API."""
    combined_content = (
        "\n\n# Markdown Cells\n\n" + markdown_content + "\n\n# Code Cells\n\n" + code_content
    )
    prompt = f"""
    **Instructions**: Below is the content of a Jupyter Notebook in markdown and code format. Your task is to generate a brief and clear documentation on the general purpose of the notebook, the main steps followed, the analysis performed, and the results obtained, if any. Organize the documentation into the following sections:

    1. **Introduction**: A brief description of the main goal of the notebook.
    2. **Methodology**: Explanation of the key steps or processes followed in the notebook.
    3. **Analysis and Results**: A summary of the analysis performed and the results obtained.
    4. **Conclusions**: A brief conclusion, if applicable.

    **Considerations**:
    - Make sure to use clear and simple language.
    - Do not include excessive details about the code; focus on describing the actions and the reasoning behind them.
    - If the notebook includes graphs or visualizations, mention their purpose and what insights they provide.
    - If specific tools or libraries are used (such as Pandas, Matplotlib, etc.), briefly mention their role in the analysis.
    - The output must be properly structured in **Markdown** format. Use headings, lists, and bold text appropriately to improve readability and organization.

    **Input**: Below is the markdown and code content of the Jupyter Notebook:

    {combined_content}

    **Expected output**: The output should be a structured text in **Markdown** format that explains the notebook concisely yet comprehensively, covering the mentioned sections, and following the given considerations.
    """

    completion = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    response_text = completion.choices[0].message.content.strip()
    cleaned_response = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)
    # Eliminar líneas vacías o con solo espacios
    cleaned_response = re.sub(r"\n\s*\n", "\n", cleaned_response)

    # Eliminar espacios al principio y al final de cada línea
    cleaned_response = re.sub(r"^\s+|\s+$", "", cleaned_response, flags=re.MULTILINE)
    return cleaned_response


# Step 4: Convert Jupyter Notebook to Markdown format
def convert_notebook_to_markdown(notebook):
    exporter = MarkdownExporter()
    markdown, _ = exporter.from_notebook_node(notebook)
    return markdown


# Step 5: Process all notebooks and generate documentation
def process_notebooks(directory="notebooks"):
    notebooks = load_notebooks(directory)
    for notebook in notebooks:
        # Extract markdown and code content
        markdown_cells, code_cells = extract_cells(notebook)

        # Join the markdown and code content into a single string
        markdown_content = "\n\n".join(markdown_cells)
        code_content = "\n\n".join(code_cells)

        # Send combined content (markdown + code) to the API for documentation generation
        documentation = generate_documentation_from_api(markdown_content, code_content)

        # Convert the whole notebook to markdown
        notebook_markdown = convert_notebook_to_markdown(notebook)

        # Save the markdown and generated documentation to a file
        output_filename = os.path.join(
            "output", f'{notebook["metadata"].get("name", "unnamed")}_documentation.md'
        )
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("# Documentation\n\n")
            f.write(documentation)
            # f.write("\n\n# Original Notebook\n\n")
            # f.write(notebook_markdown)

        print(f"Documentation saved for {notebook['metadata'].get('name', 'unnamed notebook')}")


# Running the program
process_notebooks("notebooks")

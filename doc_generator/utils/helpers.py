import os
import re

# import pypandoc
import subprocess

import black
import markdown
import nbformat
from nbconvert import MarkdownExporter

from doc_generator.prompts import prompt_for_add_comments, system_prompt

# from weasyprint import HTML


def md_to_pdf(markdown_file, output_pdf):
    """
    Converts a Markdown file (.md) to a PDF file.

    Parameters
    ----------
    markdown_file : str
        Path to the input .md file.
    output_pdf : str
        Path to save the generated .pdf file.
    """
    if not os.path.exists(markdown_file):
        print(f"Error: Input file '{markdown_file}' does not exist.")
        return

    try:
        css_file = "style.css"  # Optional: Path to your CSS file for styling

        # Build the pandoc command
        command = ["pandoc", markdown_file, "--css", css_file, "-o", output_pdf]
        subprocess.run(command, check=True)
        # Convert Markdown to HTML using markdown library
        # html = markdown.markdown(open(markdown_file, "r", encoding="utf-8").read())

        # Use WeasyPrint to convert HTML to PDF
        # HTML(string=html).write_pdf(output_pdf)

        # pypandoc.convert_file(markdown_file, "pdf", outputfile=output_pdf)

        print(f"Successfully converted '{markdown_file}' to '{output_pdf}'")

    except Exception as e:
        print(f"Error converting '{markdown_file}': {e}")


def format_text(input_string):
    cleaned_string = re.sub(r"\s+", "_", input_string.strip())
    return cleaned_string


def clean_completion_text(completion, clean_spaces=True):
    response_text = completion.choices[0].message.content.strip()
    cleaned_response = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)

    if clean_spaces:
        # Eliminar líneas vacías o con solo espacios
        cleaned_response = re.sub(r"\n\s*\n", "\n", cleaned_response)
        # Eliminar espacios al principio y al final de cada línea
        cleaned_response = re.sub(r"^\s+|\s+$", "", cleaned_response, flags=re.MULTILINE)

    cleaned_response = cleaned_response.strip("```markdown\n").strip("```")

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
def format_code_with_black(content):
    try:
        formatted_content = black.format_str(
            content,
            mode=black.Mode(line_length=100),
        )
        return formatted_content
    except (black.NothingChanged, black.parsing.InvalidInput):
        return content


def format_markdown(content):
    formatted_content = re.sub(r"\n+", "\n", content.strip())
    formatted_content = re.sub(r"\s+", " ", formatted_content)
    return formatted_content


def extract_cells(client, model, notebook):
    markdown_cells = []
    code_cells = []

    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            # Format markdown content before adding to the list
            formatted_markdown = format_markdown(cell.source)
            markdown_cells.append(formatted_markdown)
        else:
            # Format code content with black before sending for comments
            formatted_code = format_code_with_black(cell.source)
            prompt = prompt_for_add_comments(formatted_code)

            # Create a chat completion request with the formatted code
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            )

            # Clean the response from the completion and add to code cells
            clean_response = clean_completion_text(completion)
            code_cells.append(clean_response)

    return markdown_cells, code_cells


# Step 4: Convert Jupyter Notebook to Markdown format
def convert_notebook_to_markdown(notebook):
    exporter = MarkdownExporter()
    markdown, _ = exporter.from_notebook_node(notebook)
    return markdown

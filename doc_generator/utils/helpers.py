import os
import re

import nbformat
from nbconvert import MarkdownExporter


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


# Step 4: Convert Jupyter Notebook to Markdown format
def convert_notebook_to_markdown(notebook):
    exporter = MarkdownExporter()
    markdown, _ = exporter.from_notebook_node(notebook)
    return markdown

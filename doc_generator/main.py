import os
import re

from doc_generator.prompts import prompt_for_documentation
from doc_generator.utils import convert_notebook_to_markdown, extract_cells, load_notebooks


# Step 3: Send content (markdown + code) to an API for documentation generation
def generate_documentation_from_api(client, markdown_content, code_content, model):
    """Processes extracted content with OpenAI API."""
    combined_content = (
        "\n\n# Markdown Cells\n\n" + markdown_content + "\n\n# Code Cells\n\n" + code_content
    )

    prompt = prompt_for_documentation(combined_content)

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


# Step 5: Process all notebooks and generate documentation
def process_notebooks(client, model, directory="notebooks"):
    notebooks = load_notebooks(directory)
    for notebook in notebooks:
        # Extract markdown and code content
        markdown_cells, code_cells = extract_cells(notebook)

        # Join the markdown and code content into a single string
        markdown_content = "\n\n".join(markdown_cells)
        code_content = "\n\n".join(code_cells)

        # Send combined content (markdown + code) to the API for documentation generation
        documentation = generate_documentation_from_api(
            client, markdown_content, code_content, model
        )

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

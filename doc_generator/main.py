import os

from IPython.display import clear_output

from doc_generator.prompts import (
    prompt_for_documentation,
    prompt_for_documentation_name,
    prompt_for_generation_resume,
    prompt_for_review_format,
    prompt_for_table_creation,
)
from doc_generator.utils import clean_completion_text, extract_cells, load_notebooks


# Step 3: Send content (markdown + code) to an API for documentation generation
def generate_documentation_from_api(client, markdown_content, code_content, model):
    """Processes extracted content with OpenAI API."""

    prompt = prompt_for_generation_resume(code_content)
    completion = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    context = clean_completion_text(completion)

    prompt = prompt_for_table_creation(code_content)
    completion = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    tables_info = clean_completion_text(completion)

    combined_content = (
        "\n\n**Markdown Cells**\n\n" + markdown_content + "\n\n**Code Cells**\n\n" + code_content
    )

    prompt = prompt_for_documentation(combined_content, context, tables_info)
    completion = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    cleaned_response = clean_completion_text(completion)

    return cleaned_response, context


# Step 5: Process all notebooks and generate documentation
def process_notebooks(client, model, directory="notebooks", language="english"):
    notebooks = load_notebooks(directory)
    num_notebooks = len(notebooks)
    print(f"Found {num_notebooks} notebooks in the directory: {directory}")
    for notebook in notebooks:
        print(f"Processing notebook number {notebooks.index(notebook) + 1} of {num_notebooks}...")
        print("Extracting markdown and code content...")
        # Extract markdown and code content
        markdown_cells, code_cells = extract_cells(client, model, notebook)
        print("Content extracted successfully.")

        # Join the markdown and code content into a single string
        markdown_content = "\n\n".join(markdown_cells)
        code_content = "\n\n".join(code_cells)

        # Send combined content (markdown + code) to the API for documentation generation
        print("Sending combined content to the API for documentation generation...")
        documentation, context = generate_documentation_from_api(
            client, markdown_content, code_content, model
        )
        print("Documentation generated successfully.")

        print("Generating review prompt for documentation...")
        prompt = prompt_for_review_format(documentation, language)
        completion = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        documentation = clean_completion_text(completion)
        print("Review prompt processed and documentation cleaned.")

        print("Generating name for the documentation...")
        prompt = prompt_for_documentation_name(context)
        completion = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        doc_name = clean_completion_text(completion)
        metadata_name = notebook["metadata"].get("name", "unnamed")
        doc_name = doc_name if metadata_name == "unnamed" else metadata_name
        output_filename = os.path.join("output", f"{doc_name}.md")
        print(f"Generated documentation name: {doc_name}")

        print(f"Saving documentation to file: {output_filename}")
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(documentation)

        print(f"Documentation saved in {output_filename}")
        clear_output(wait=True)

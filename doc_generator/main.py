import os
import re

from IPython.display import clear_output

from doc_generator.prompts import (
    prompt_for_documentation,
    prompt_for_documentation_name,
    prompt_for_generation_resume,
    prompt_for_review_format,
    prompt_for_table_creation,
    system_prompt,
)
from doc_generator.utils import clean_completion_text, extract_cells, format_text, load_notebooks


# Step 3: Send content (markdown + code) to an API for documentation generation
def generate_documentation_from_api(client, markdown_content, code_content, model):
    """Processes extracted content with OpenAI API."""

    print("Generating resume for code content...")
    prompt = prompt_for_generation_resume(code_content)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    context = clean_completion_text(completion)
    print("Resume generated successfully.")

    print("Generating tables for code content...")
    prompt = prompt_for_table_creation(code_content)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    response_text = completion.choices[0].message.content
    tables_info = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)
    tables_info += "\n"
    print("Tables generated successfully.")

    combined_content = (
        "\n\n**Markdown Cells**\n\n" + markdown_content + "\n\n**Code Cells**\n\n" + code_content
    )

    print("Generating documentation for combined content...")
    prompt = prompt_for_documentation(combined_content, context, tables_info)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    cleaned_response = clean_completion_text(completion, clean_spaces=False)

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
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        documentation = clean_completion_text(completion, clean_spaces=False)
        print("Review prompt processed and documentation cleaned.")

        print("Generating name for the documentation...")
        prompt = prompt_for_documentation_name(context)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        doc_name = clean_completion_text(completion)
        doc_name = format_text(doc_name)
        metadata_name = notebook["metadata"].get("name", "unnamed")
        doc_name = doc_name if metadata_name == "unnamed" else metadata_name
        doc_name = doc_name.replace(".", "") if doc_name.endswith(".") else doc_name
        doc_name = doc_name.replace(".md", "") if doc_name.endswith(".md") else doc_name
        output_filename = os.path.join("output", f"{doc_name}.md")
        print(f"Generated documentation name: {doc_name}")

        print(f"Saving documentation to file: {output_filename}")
        if len(output_filename) > 255:
            output_filename = os.path.join("output", "unnamed_documentation.md")
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(documentation)

        print(f"Documentation saved in {output_filename}")
        clear_output(wait=True)
        return output_filename, output_filename.replace("md", "pdf")

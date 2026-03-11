import os
import re
import threading

from IPython.display import clear_output

from core.prompts import (
    prompt_for_documentation,
    prompt_for_documentation_name,
    prompt_for_generation_resume,
    prompt_for_review_format,
    prompt_for_table_creation,
    system_prompt,
)
from core.utils import (
    clean_completion_text,
    extract_cells,
    format_text,
    load_notebooks,
    md_to_pdf,
)


# Global cancellation flag
_cancellation_requested = threading.Event()
_cancellation_lock = threading.Lock()


def is_cancelled():
    """Check if cancellation has been requested."""
    return _cancellation_requested.is_set()


def cancel_generation():
    """Request cancellation of the current generation process."""
    with _cancellation_lock:
        _cancellation_requested.set()
    print("\nCancellation requested. Finishing current task...")


def reset_cancellation():
    """Reset the cancellation flag for a new generation process."""
    _cancellation_requested.clear()


# Step 3: Send content (markdown + code) to an API for documentation generation
def generate_documentation_from_api(client, markdown_content, code_content, model):
    """Processes extracted content with OpenAI API."""
    if is_cancelled():
        return None, None

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
    # Check for cancellation after first API call
    if is_cancelled():
        return None, context

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
    # Check for cancellation after second API call
    if is_cancelled():
        return None, context

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
    # Reset cancellation flag at the start
    reset_cancellation()
    notebooks, names = load_notebooks(directory)
    num_notebooks = len(notebooks)
    print(f"Found {num_notebooks} notebooks in the directory: {directory}")
    for i, notebook in enumerate(notebooks):
        # Check for cancellation before processing each notebook
        if is_cancelled():
            print(f"\nCancellation accepted. Stopping after {i} notebook(s).")
            break
        print(f"Notebook name : {names[i]}")
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
        # Check for cancellation after documentation generation
        if is_cancelled() or documentation is None:
            print(f"\nStopping notebook processing. Documentation for this notebook was not saved.")
            break
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
        # Check for cancellation after review prompt
        if is_cancelled():
            print(f"\nStopping notebook processing. Documentation for this notebook was not saved.")
            break

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
        markdown_file, output_pdf = output_filename, output_filename.replace("md", "pdf")
        md_to_pdf(markdown_file, output_pdf)
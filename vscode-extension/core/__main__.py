"""
CLI Entry Point for Notebook Documentation Generator
This module allows running the tool via: python -m core [options]
"""

import argparse
import os
import signal
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.main import cancel_generation
from openai import OpenAI
from core.claude_client import create_claude_client


def signal_handler(signum, frame):
    """Handle Ctrl+C signal to gracefully cancel generation."""
    print("\n\nCtrl+C detected! Requesting cancellation...")
    cancel_generation()
    print("Please wait for current task to finish...")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate documentation from Jupyter notebooks using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m core                           Generate docs for all notebooks in 'notebooks' folder
  python -m core path/to/notebook.ipynb    Generate docs for a specific notebook
  python -m core path/to/folder           Generate docs for all notebooks in a folder
  python -m core --no-pdf                  Generate only markdown, skip PDF
  python -m core --language spanish       Generate docs in Spanish
  python -m core --model gpt-4            Specify AI model to use
        """,
    )

    parser.add_argument(
        "input_path",
        nargs="?",
        default="notebooks",
        help="Path to notebook file, folder, or notebooks directory (default: notebooks)",
    )

    parser.add_argument(
        "output_dir",
        nargs="?",
        default="output",
        help="Output directory for generated documentation (default: output)",
    )

    parser.add_argument(
        "--no-pdf", action="store_true", help="Skip PDF generation, generate only markdown"
    )

    parser.add_argument(
        "--language",
        default="english",
        help="Language for generated documentation (default: english)",
    )

    parser.add_argument(
        "--model", default="gpt-4", help="AI model to use for generation (default: gpt-4)"
    )

    parser.add_argument(
        "--api-key", help="OpenAI API key (or set OPENAI_API_KEY environment variable)"
    )

    parser.add_argument(
        "--provider",
        choices=["openai", "ollama", "lmstudio", "claude"],
        default="openai",
        help="LLM provider (openai, ollama/LMStudio local via api-base, claude/Anthropic)",
    )

    parser.add_argument(
        "--api-base",
        help="Custom API base URL for OpenAI-compatible (e.g., http://localhost:11434/v1)",
    )

    parser.add_argument("--list-models", action="store_true", help="List available models and exit")

    return parser.parse_args()


def get_llm_client(provider, args):
    """Initialize LLM client based on provider."""
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY", "")
    base_url = args.api_base or os.environ.get("API_BASE_URL", "")

    if provider in ["openai", "ollama", "lmstudio"]:
        # OpenAI-compatible (cloud or local)
        if not api_key and not base_url and provider == "openai":
            print(
                "Warning: No OpenAI API key for 'openai' provider. Set OPENAI_API_KEY or use --api-key."
            )

        if ("localhost" in (base_url or "") or "127.0.0.1" in (base_url or "")) and not api_key:
            api_key = "local-model"

        try:
            from openai import OpenAI

            client = OpenAI(base_url=base_url, api_key=api_key)
            print(f"{provider.upper()} client initialized (OpenAI-compatible)")
            print(f"  Model: {args.model}")
            print(f"  Base URL: {base_url or 'https://api.openai.com/v1'}")
            return client
        except Exception as e:
            print(f"Error initializing {provider} client: {e}")
            sys.exit(1)

    elif provider == "claude":
        # Claude/Anthropic
        try:
            from core.claude_client import ClaudeClient

            client = ClaudeClient(
                base_url=base_url or None,
                auth_token=api_key or None,
                model=args.model,
            )
            print(f"Claude client initialized")
            print(f"  Model: {client.model}")
            print(f"  Base URL: {client.base_url}")
            return client
        except Exception as e:
            print(f"Error initializing Claude client: {e}")
            print("Set ANTHROPIC_API_KEY env var or use --api-key")
            sys.exit(1)

    else:
        print(f"Unsupported provider: {provider}")
        sys.exit(1)


def setup_environment():
    """Ensure required directories exist."""
    # Create notebooks directory if it doesn't exist
    if not os.path.exists("notebooks"):
        os.makedirs("notebooks")
        print("Created 'notebooks' directory. Add your .ipynb files there.")

    # Create output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")
        print("Created 'output' directory.")


def process_single_notebook(
    client, model, notebook_path, output_dir, no_pdf=False, language="english"
):
    """Process a single notebook file."""
    import nbformat
    from core.main import (
        clean_completion_text,
        generate_documentation_from_api,
        prompt_for_review_format,
        system_prompt,
    )
    from core.utils.helpers import extract_cells, md_to_pdf

    print(f"\nProcessing notebook: {notebook_path}")

    # Load the notebook
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # Extract cells
    markdown_cells, code_cells = extract_cells(client, model, notebook)

    # Combine content
    markdown_content = "\n\n".join(markdown_cells)
    code_content = "\n\n".join(code_cells)

    # Generate documentation
    documentation, context = generate_documentation_from_api(
        client, markdown_content, code_content, model
    )

    prompt = prompt_for_review_format(documentation, language)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    documentation = clean_completion_text(completion, clean_spaces=False)

    # Get output filename
    basename = os.path.basename(notebook_path).replace(".ipynb", "")
    output_path = os.path.join(output_dir, f"{basename}.md")

    # Save markdown
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(documentation)

    print(f"Markdown saved to: {output_path}")

    # Convert to PDF if requested
    if not no_pdf:
        try:
            from core.main import md_to_pdf

            pdf_path = output_path.replace(".md", ".pdf")
            md_to_pdf(output_path, pdf_path)
            print(f"PDF saved to: {pdf_path}")
        except Exception as e:
            print(f"Warning: Could not generate PDF: {e}")

    return output_path


def main():
    """Main entry point for the CLI."""
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    args = parse_args()

    # Check if input path exists
    input_path = args.input_path
    output_dir = args.output_dir

    if not os.path.exists(input_path):
        print(f"Error: Input path does not exist: {input_path}")
        sys.exit(1)

    # Get provider and model
    provider = args.provider
    model = args.model

    # List models if requested (basic info)
    if args.list_models:
        print(f"Provider: {provider}")
        print(f"OpenAI-compatible models: gpt-4o, gpt-4, gpt-3.5-turbo, llama3, etc.")
        if provider == "anthropic":
            print("Anthropic models: claude-3-5-sonnet-20240620, claude-3-sonnet-20240229")
        sys.exit(0)

    # Initialize LLM client
    client = get_llm_client(provider, args)

    # Setup environment
    setup_environment()

    # Determine what to process
    if os.path.isfile(input_path):
        # Single notebook file
        if not input_path.endswith(".ipynb"):
            print(f"Error: {input_path} is not a Jupyter notebook (.ipynb)")
            sys.exit(1)

        process_single_notebook(client, model, input_path, output_dir, args.no_pdf, args.language)

    elif os.path.isdir(input_path):
        # Directory - process all notebooks
        notebook_files = [
            os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".ipynb")
        ]

        if not notebook_files:
            print(f"No notebooks found in: {input_path}")
            sys.exit(1)

        print(f"Found {len(notebook_files)} notebook(s) in: {input_path}")

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Process each notebook
        for notebook_file in notebook_files:
            try:
                process_single_notebook(
                    client, model, notebook_file, output_dir, args.no_pdf, args.language
                )
            except Exception as e:
                print(f"Error processing {notebook_file}: {e}")
                continue

        print(f"\nDocumentation generated in: {output_dir}")

    else:
        print(f"Error: Invalid input path: {input_path}")
        sys.exit(1)

    print("\nDone!")


if __name__ == "__main__":
    main()

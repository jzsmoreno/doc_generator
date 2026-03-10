import os
import sys
from openai import OpenAI
import nbformat

# Add the doc_generator directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from doc_generator.utils.helpers import extract_cells


def test_extract_cells():
    """Test the extract_cells function with a sample notebook."""

    # Create a simple test notebook programmatically
    notebook = nbformat.v4.new_notebook()

    # Add a markdown cell
    notebook.cells.append(
        nbformat.v4.new_markdown_cell("# Test Notebook\nThis is a test notebook.")
    )

    # Add a code cell with output
    code_cell = nbformat.v4.new_code_cell("print('Hello, World!')\n2 + 2")

    # Add output to the code cell
    code_cell.outputs = [{"output_type": "stream", "name": "stdout", "text": "Hello, World!\n4\n"}]

    # Add another code cell with rich output
    code_cell2 = nbformat.v4.new_code_cell("import matplotlib.pyplot as plt\nplt.plot([1, 2, 3])")
    code_cell2.outputs = [
        {
            "output_type": "display_data",
            "data": {
                "text/plain": "<matplotlib.figure.Figure at 0x123456789>",
                "image/png": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            },
        }
    ]

    notebook.cells.append(code_cell)
    notebook.cells.append(code_cell2)

    api_url = "http://127.0.0.1:1234/v1"
    client = OpenAI(base_url=api_url, api_key="lm-studio")
    model = "gemma-3-4b-it"

    # Test the extract_cells function
    try:
        markdown_cells, code_cells = extract_cells(client, model, notebook)

        print("Test Results:")
        print(f"Number of markdown cells extracted: {len(markdown_cells)}")
        print(f"Number of code cells extracted: {len(code_cells)}")

        # Check if outputs are included
        for i, code_cell in enumerate(code_cells):
            print(f"\nCode cell {i+1}:")
            print(f"Content length: {len(code_cell)}")
            if "Output:" in code_cell:
                print("✓ Outputs found in extracted content!")
            else:
                print("✗ No outputs found in extracted content")

        return True

    except Exception as e:
        print(f"Error during extraction: {e}")
        return False


if __name__ == "__main__":
    print("Testing extract_cells function...")
    success = test_extract_cells()
    if success:
        print("\n✓ Test completed successfully!")
    else:
        print("\n✗ Test failed!")

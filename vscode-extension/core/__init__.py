"""
Notebook Documentation Generator - Core Package
"""

from core.main import (
    cancel_generation,
    generate_documentation_from_api,
    is_cancelled,
    process_notebooks,
    reset_cancellation,
)
from core.utils.helpers import (
    clean_completion_text,
    convert_notebook_to_markdown,
    extract_cells,
    load_notebooks,
    md_to_pdf,
)

__version__ = "0.1.0"
__all__ = [
    "process_notebooks",
    "generate_documentation_from_api",
    "extract_cells",
    "md_to_pdf",
    "clean_completion_text",
    "load_notebooks",
    "convert_notebook_to_markdown",
    "is_cancelled",
    "cancel_generation",
    "reset_cancellation",
]

"""
Notebook Documentation Generator - Core Package
"""

from core.main import (
    process_notebooks,
    generate_documentation_from_api,
    is_cancelled,
    cancel_generation,
    reset_cancellation,
)
from core.utils.helpers import (
    extract_cells,
    md_to_pdf,
    clean_completion_text,
    load_notebooks,
    convert_notebook_to_markdown,
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

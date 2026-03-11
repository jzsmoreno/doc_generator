# Feature Summary

## Core Features

### 1. AI-Powered Documentation Generation
- Uses OpenAI GPT-4, GPT-3.5 Turbo, or local models
- Analyzes Jupyter notebook content (markdown + code)
- Generates comprehensive documentation with:
  - Introduction
  - Methodology
  - Analysis and Results
  - Conclusions

### 2. Code Commenting
- Automatically adds comments to code cells
- Uses AI to explain code functionality
- Preserves original code structure

### 3. Table Extraction
- Extracts tables from code outputs
- Includes tables in documentation exactly as they appear
- Supports pandas DataFrame displays

### 4. Multi-Format Output
- **Markdown**: Clean, readable documentation
- **PDF**: Professional formatted documents
- Custom output directory configuration

### 5. VS Code Integration
- Right-click context menu for notebooks
- Right-click context menu for folders
- Command Palette commands
- Progress notifications
- Output panel for debugging

## CLI Features

### Flexible Input Options
```bash
# Single notebook
python -m core notebook.ipynb

# All notebooks in folder
python -m core notebooks/

# Custom output directory
python -m core notebook.ipynb my_output/
```

### Configuration Options
- `--no-pdf`: Skip PDF generation
- `--language`: Set documentation language
- `--model`: Choose AI model
- `--api-key`: Specify API key
- `--api-base`: Custom API endpoint

### Supported Models
- OpenAI GPT-4
- OpenAI GPT-3.5 Turbo
- Ollama (llama2, codellama, etc.)
- LM Studio models
- Any OpenAI-compatible API

## Technical Features

### 1. Cell Extraction
- Markdown cell extraction
- Code cell extraction
- Output capture (text, images)
- Cell metadata preservation

### 2. Content Processing
- Code formatting with Black
- Markdown normalization
- Output text extraction
- Multi-format output handling

### 3. Error Handling
- Graceful degradation
- Detailed error messages
- Logging to output channel
- Recovery from partial failures

### 4. Progress Tracking
- Real-time progress notifications
- Step-by-step status updates
- Completion notifications

## Extension Features

### 1. Context Menu Integration
- Right-click on .ipynb files
- Right-click on folders
- Explorer and Editor context menus

### 2. Environment Checking
- Python availability detection
- Dependency verification
- System requirement checks

### 3. Configuration Management
- VS Code settings integration
- Per-workspace configuration
- API key management

### 4. Output Panel
- Real-time logging
- Error reporting
- Debug information

## Supported Languages

Documentation can be generated in:
- English (default)
- Spanish
- French
- German
- Chinese
- Japanese
- And many more...

## File Support

### Input Files
- `.ipynb` - Jupyter notebooks (version 4+)

### Output Files
- `.md` - Markdown documentation
- `.pdf` - PDF documents

## Platform Support

- **Windows**: Full support with GTK3 for PDF
- **macOS**: Full support with Homebrew dependencies
- **Linux**: Full support with system libraries

## Integration Capabilities

### External Tools
- OpenAI API
- Ollama
- LM Studio
- WeasyPrint
- Pandoc
- Black (code formatting)

### Workflow Integration
- Pre-commit hooks
- CI/CD pipelines
- Batch processing
- Single file processing


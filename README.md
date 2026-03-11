# Notebook Documentation Generator

A powerful tool that generates comprehensive documentation from Jupyter notebooks using AI. Includes a VS Code extension for seamless integration.

## Features

- **AI-Powered Documentation**: Generate detailed documentation using OpenAI or local models (Ollama, LM Studio)
- **Multiple Output Formats**: Generate both Markdown and PDF documentation
- **VS Code Integration**: Right-click context menus and Command Palette integration
- **Code Commenting**: Automatically adds comments to code cells
- **Table Extraction**: Extracts and includes data tables from notebook outputs
- **Multi-language Support**: Generate documentation in multiple languages
- **Flexible API Configuration**: Use OpenAI API or local models

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or with specific packages:

```bash
pip install openai nbconvert nbformat markdown weasyprint pypandoc black
```

### 2. Configure API Access

**Option A: OpenAI API**

```bash
# Set environment variable
export OPENAI_API_KEY=your-api-key-here

# Or use the API base URL for other models
export API_BASE_URL=https://api.openai.com/v1
```

**Option B: Local Models (Ollama, LM Studio)**

```bash
# For Ollama
export API_BASE_URL=http://localhost:11434/v1

# For LM Studio
export API_BASE_URL=http://127.0.0.1:1234/v1
```

### 3. Use the CLI

```bash
# Generate docs for all notebooks in 'notebooks' folder
python -m core

# Generate docs for a specific notebook
python -m core path/to/notebook.ipynb

# Generate docs for all notebooks in a folder
python -m core path/to/notebooks output

# Generate only markdown (skip PDF)
python -m core path/to/notebook.ipynb --no-pdf

# Use a specific model
python -m core path/to/notebook.ipynb --model gpt-4

# Generate in a different language
python -m core path/to/notebook.ipynb --language spanish
```

### 4. Install VS Code Extension

```bash
cd vscode-extension
npm install
npm run compile
```

Then open VS Code and install the extension from the `vscode-extension` folder.

## Project Structure

```
doc_generator/
├── core/                      # Core Python package
│   ├── __init__.py           # Package exports
│   ├── __main__.py           # CLI entry point
│   ├── main.py               # Main processing logic
│   ├── prompts/              # AI prompt templates
│   │   └── prompt_templates.py
│   └── utils/                # Utility functions
│       └── helpers.py
├── notebooks/                # Sample notebooks (add yours here)
├── output/                   # Generated documentation
├── vscode-extension/         # VS Code extension
│   ├── src/                  # TypeScript source
│   └── package.json          # Extension configuration
├── requirements.txt          # Python dependencies
├── package.json             # Root npm configuration
├── build.bat                # Windows build script
└── build.sh                 # Linux/Mac build script
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_path` | Path to notebook file or folder | `notebooks` |
| `output_dir` | Output directory for docs | `output` |
| `--no-pdf` | Skip PDF generation | False |
| `--language` | Documentation language | `english` |
| `--model` | AI model to use | `gpt-4` |
| `--api-key` | OpenAI API key | From env |
| `--api-base` | Custom API base URL | From env |

## Supported AI Models

- OpenAI GPT-4
- OpenAI GPT-3.5 Turbo
- Ollama models (llama2, codellama, etc.)
- LM Studio models
- Any OpenAI-compatible API

## Configuration

### VS Code Settings

```json
{
  "notebookDocGenerator.openaiApiKey": "your-api-key",
  "notebookDocGenerator.model": "gpt-4",
  "notebookDocGenerator.language": "english",
  "notebookDocGenerator.generatePdf": true,
  "notebookDocGenerator.pythonPath": "",
  "notebookDocGenerator.apiBaseUrl": ""
}
```

### Environment Variables

```bash
OPENAI_API_KEY=your-api-key
API_BASE_URL=http://localhost:11434/v1
```

## Documentation Files

- [INSTALLATION.md](INSTALLATION.md) - Detailed installation guide
- [TESTING.md](TESTING.md) - Testing procedures
- [FEATURE_SUMMARY.md](FEATURE_SUMMARY.md) - Complete feature list

## Building

### Windows

```bash
build.bat
```

### Linux/Mac

```bash
chmod +x build.sh
./build.sh
```

## Troubleshooting

### Python not found

Ensure Python 3.7+ is installed and in your PATH. Check with:

```bash
python --version
```

### Module not found

Make sure you're running from the project root directory.

### PDF generation fails

Install system dependencies:
- **Windows**: GTK3 for WeasyPrint
- **macOS**: Cairo, Pango libraries
- **Linux**: libcairo2, libpango-1.0-0, etc.

### API Errors

- Verify your API key is correct
- Check API rate limits
- For local models, ensure the server is running

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


# Installation Guide

This guide covers all installation methods for the Notebook Documentation Generator.

## Prerequisites

### Python Requirements

- Python 3.7 or higher
- pip package manager

Check your Python version:

```bash
python --version
# or
python3 --version
```

### System Dependencies for PDF Generation

#### Windows

1. **Python 3.7+** with pip
2. **GTK3** for WeasyPrint:
   - Download from [GTK3 Windows](https://www.gtk.org/docs/installations/windows/)
   - Add GTK3 bin directory to PATH
3. **Visual C++ Build Tools** (if not already installed)

#### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install cairo pango gdk-pixbuf libffi
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-shared libjpeg-dev libopenjp2-7-dev
```

## Installation Steps

### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd doc_generator
```

### Step 2: Install Python Dependencies

#### Option A: Using requirements.txt

```bash
pip install -r requirements.txt
```

#### Option B: Install Individual Packages

```bash
pip install openai nbconvert nbformat markdown weasyprint pypandoc black
```

#### Option C: Using pip with Extras

```bash
pip install openai nbconvert nbformat markdown weasyprint pypandoc black
```

### Step 3: Configure API Access

#### Option A: OpenAI API Key

**Environment Variable (Recommended)**

```bash
# Linux/macOS
export OPENAI_API_KEY=your-api-key-here

# Windows (CMD)
set OPENAI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
```

**VS Code Settings**

1. Open VS Code Settings (Ctrl+, or Cmd+, on macOS)
2. Search for `notebook documentation generator`
3. Add your API key to `notebookDocGenerator.openaiApiKey`

**OpenAI/LM-Studio/Ollama (`--provider openai`):**
```
export OPENAI_API_KEY=sk-...  # Optional for local
export API_BASE_URL=http://localhost:11434/v1  # Ollama
```

**Anthropic/Claude (`--provider anthropic`):**
```
export ANTHROPIC_BASE_URL=https://api.anthropic.com
export ANTHROPIC_AUTH_TOKEN=your-token
```

### Step 4: Verify Installation

```bash
# Test Python module
python -c "import core; print('Core package imported successfully')"

# Test CLI help
python -m core --help
```

### Step 5: Install VS Code Extension (Optional)

```bash
cd vscode-extension
npm install
npm run compile
```

Then in VS Code:
1. Press F5 to launch Extension Development Host
2. Or install from VSIX file: `Extensions > Install from VSIX`

## Usage

### CLI Usage

```bash
# Generate docs for all notebooks in 'notebooks' folder
python -m core

# Generate docs for a specific notebook
python -m core notebooks/my_notebook.ipynb

# Generate docs for a folder
python -m core notebooks/ output/

# Generate without PDF
python -m core notebooks/ --no-pdf

# Use specific model
python -m core notebooks/ --model gpt-4

# Use specific language
python -m core notebooks/ --language spanish
```

### VS Code Extension Usage

1. **Right-click on a notebook** → "Generate Documentation for Notebook"
2. **Right-click on a folder** → "Generate Documentation for Folder"
3. **Command Palette** → "Generate Documentation for Notebook"

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | None |
| `API_BASE_URL` | Custom API URL | None |

### VS Code Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `notebookDocGenerator.openaiApiKey` | API key | "" |
| `notebookDocGenerator.model` | AI model | "gpt-4" |
| `notebookDocGenerator.language` | Language | "english" |
| `notebookDocGenerator.generatePdf` | Generate PDF | true |
| `notebookDocGenerator.pythonPath` | Python path | "" |
| `notebookDocGenerator.apiBaseUrl` | API base URL | "" |

## Troubleshooting

### "Python not found" Error

- Install Python 3.7+ from python.org
- Add Python to system PATH
- Verify with: `python --version`

### "Module not found" Error

- Ensure you're in the project root directory
- Run: `pip install -r requirements.txt`

### "No API key found" Error

- Set `OPENAI_API_KEY` environment variable
- Or configure in VS Code settings

### PDF Generation Fails

- Install system dependencies (see Prerequisites)
- Check WeasyPrint: `python -c "import weasyprint"`
- Try with `--no-pdf` flag

### VS Code Extension Not Loading

- Check Output panel for errors
- Ensure TypeScript compiled: `cd vscode-extension && npm run compile`
- Restart VS Code

## Upgrading

```bash
# Update Python packages
pip install --upgrade -r requirements.txt

# Or upgrade individual packages
pip install --upgrade openai nbconvert nbformat
```

## Uninstallation

```bash
# Remove Python packages
pip uninstall openai nbconvert nbformat markdown weasyprint pypandoc black

# Remove VS Code extension
# In VS Code: Extensions > Notebook Documentation Generator > Uninstall
```

## Support

- Check [README.md](README.md) for usage examples
- Review [TESTING.md](TESTING.md) for testing procedures
- Open an issue on GitHub for bug reports


# Testing Guide

This document covers testing procedures for the Notebook Documentation Generator.

## Prerequisites

Before running tests, ensure:

1. Python 3.7+ is installed
2. All dependencies are installed: `pip install -r requirements.txt`
3. You have an API key configured (or local model running)

## Running Tests

### Test 1: Python Module Import

```bash
# Test core package imports
python -c "import core; print('✓ Core package imported successfully')"

# Test specific functions
python -c "from core import process_notebooks, extract_cells; print('✓ Functions imported')"
```

### Test 2: CLI Help

```bash
# Test CLI help display
python -m core --help
```

Expected output:
```
usage: __main__.py [-h] [--no-pdf] [--language LANGUAGE] [--model MODEL]
                   [--api-key API_KEY] [--api-base API_BASE] [--list-models]
                   [input_path] [output_dir]

Generate documentation from Jupyter notebooks using AI
```

### Test 3: Cell Extraction Test

```bash
# Run the extraction test
python test_extract_cells.py
```

### Test 4: Single Notebook Processing

```bash
# Create a test notebook if needed
# Then process it
python -m core notebooks/Deep_Models.ipynb output/test
```

### Test 5: Full Directory Processing

```bash
# Process all notebooks in the notebooks folder
python -m core notebooks/ output
```

## VS Code Extension Testing

### Test 1: Compile TypeScript

```bash
cd vscode-extension
npm install
npm run compile
```

### Test 2: Launch Extension Host

1. Open VS Code
2. Press F5
3. A new VS Code window opens (Extension Development Host)
4. Check "Notebook Documentation Generator" in Extensions

### Test 3: Test Extension Commands

1. Open a Jupyter notebook (.ipynb)
2. Open Command Palette (Ctrl+Shift+P)
3. Type "Generate Documentation"
4. Verify the command appears

### Test 4: Test Context Menu

1. Right-click on any .ipynb file
2. Verify "Generate Documentation for Notebook" appears
3. Right-click on a folder
4. Verify "Generate Documentation for Folder" appears

## Manual Testing Checklist

### CLI Testing
- [ ] `python -m core --help` works
- [ ] Single notebook processing works
- [ ] Folder processing works
- [ ] PDF generation works (when dependencies installed)
- [ ] --no-pdf flag works
- [ ] Custom output directory works

### Extension Testing
- [ ] Extension loads without errors
- [ ] Python environment check runs
- [ ] Right-click menu appears for notebooks
- [ ] Right-click menu appears for folders
- [ ] Command Palette commands work
- [ ] Output channel shows logs
- [ ] Progress notifications appear

## Troubleshooting Test Failures

### "Module not found" Errors

```bash
# Ensure you're in the project root
cd doc_generator

# Reinstall dependencies
pip install -r requirements.txt
```

### "API Key" Errors

```bash
# Set environment variable
export OPENAI_API_KEY=your-key

# Or test with local model
export API_BASE_URL=http://localhost:1234/v1
```

### TypeScript Compilation Errors

```bash
# Clean and reinstall
cd vscode-extension
rm -rf node_modules package-lock.json
npm install
npm run compile
```

### Extension Not Loading

1. Check Output panel (View > Output > Extension Host)
2. Look for error messages
3. Verify all dependencies installed

## Test Notebooks

The project includes sample notebooks in the `notebooks/` folder:

- `Deep_Models.ipynb` - Deep learning example
- `RL_Agent.ipynb` - Reinforcement learning example

Use these for testing the documentation generation.

## Expected Test Outputs

### Successful Notebook Processing

```
Found 1 notebook(s) in: notebooks
Processing notebook: notebooks/Deep_Models.ipynb
Extracting markdown and code content...
Content extracted successfully.
Sending combined content to the API for documentation generation...
Documentation generated successfully.
Markdown saved to: output/Deep_Models.md
PDF saved to: output/Deep_Models.pdf
Done!
```

### Successful Extension Activation

```
[Extension Host] Notebook Documentation Generator extension is now active!
[Extension Host] Python: python
[Extension Host] Python version: 3.11.4
[Extension Host] ✓ openai is installed
[Extension Host] ✓ nbconvert is installed
[Extension Host] ✓ nbformat is installed
[Extension Host] ✓ markdown is installed
[Extension Host] Python environment is ready!
```


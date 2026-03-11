# Notebook Documentation Generator for VS Code

A Visual Studio Code extension that generates comprehensive documentation from Jupyter notebooks using AI-powered analysis. This extension integrates with the Python-based notebook documentation generator to create both Markdown and PDF documentation from your notebooks.

## Features

- **Active Notebook Documentation**: Generate documentation for the currently open notebook
- **Right-Click Context Menu**: Generate documentation for any `.ipynb` file in the explorer
- **Folder-Wide Generation**: Process all notebooks in a selected folder
- **Progress Notifications**: Real-time feedback on documentation generation progress
- **Output Panel Logging**: Detailed logs for debugging and monitoring
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Automatic Output Folder**: Creates and opens the output directory with generated files

## Requirements

### System Dependencies

The extension requires Python and several system-level dependencies for PDF generation:

#### Windows
- **Python 3.7+** with pip
- **GTK3** for WeasyPrint: Download from [GTK3 Windows](https://www.gtk.org/docs/installations/windows/)
- **Visual C++ Build Tools** (if not already installed)

#### macOS
- **Python 3.7+** with pip
- **Homebrew** (for installing system dependencies)
- **Cairo, Pango, and other libraries**:
  ```bash
  brew install cairo pango gdk-pixbuf libffi
  ```

#### Linux (Ubuntu/Debian)
- **Python 3.7+** with pip
- **System libraries**:
  ```bash
  sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-shared libjpeg-dev libopenjp2-7-dev
  ```

### Python Dependencies

The extension will automatically check for and prompt installation of required Python packages:
- `openai`
- `nbconvert`
- `nbformat`
- `markdown`
- `weasyprint`
- `pypandoc`

## Installation

### 1. Install the Extension

1. Open VS Code
2. Press `Ctrl+P` (or `Cmd+P` on macOS)
3. Type `ext install notebook-documentation-generator` (or install from VSIX if provided)
4. Click Install

### 2. Install Python Dependencies

The extension will automatically detect missing Python packages and prompt you to install them. Alternatively, you can install them manually:

```bash
pip install openai nbconvert nbformat markdown weasyprint pypandoc
```

### 3. Configure OpenAI API Key

Set your OpenAI API key in one of these ways:

1. **Environment Variable** (Recommended):
   ```bash
   # Windows
   set OPENAI_API_KEY=your-api-key-here
   
   # macOS/Linux
   export OPENAI_API_KEY=your-api-key-here
   ```

2. **VS Code Settings**:
   - Open VS Code Settings (`Ctrl+,`)
   - Search for `Notebook Doc Assistant`
   - Enter your API key in the settings

## Usage

### Generate Documentation for Active Notebook

1. Open a Jupyter notebook (`.ipynb` file) in VS Code
2. Open Command Palette (`Ctrl+Shift+P`)
3. Type and select: `Generate Documentation for Notebook`
4. Wait for the process to complete
5. The output folder will automatically open with your generated documentation

### Generate Documentation for Specific Notebook

1. Right-click on any `.ipynb` file in the VS Code Explorer
2. Select `Generate Notebook Documentation`
3. Wait for the process to complete
4. The output folder will open with your generated documentation

### Generate Documentation for All Notebooks in Folder

1. Right-click on any folder in the VS Code Explorer
2. Select `Generate Documentation for Folder`
3. The extension will process all `.ipynb` files in the folder
4. Individual documentation files will be created for each notebook

## Commands

The extension provides the following commands in the Command Palette:

- `Notebook Documentation Generator: Generate Documentation for Notebook` - Active notebook
- `Notebook Documentation Generator: Generate Documentation for Folder` - Selected folder

## Configuration

The extension supports the following VS Code settings:

- `notebookDocGenerator.openaiApiKey` - Your OpenAI API key (alternative to environment variable)
- `notebookDocGenerator.model` - AI model to use (default: gpt-4)
- `notebookDocGenerator.language` - Documentation language (default: english)
- `notebookDocGenerator.generatePdf` - Generate PDF in addition to Markdown (default: true)
- `notebookDocGenerator.pythonPath` - Custom Python executable path (auto-detected by default)
- `notebookDocGenerator.apiBaseUrl` - Custom API base URL for local models

## Output

Generated documentation includes:

- **Markdown files** (`.md`) - Human-readable documentation
- **PDF files** (`.pdf`) - Formatted documentation for sharing
- **Output location**: `output/` folder in your workspace (configurable)

Each notebook generates:
- `{notebook_name}.md` - Markdown documentation
- `{notebook_name}.pdf` - PDF documentation

## Troubleshooting

### Common Issues

#### "Python not found" Error
- Ensure Python 3.7+ is installed and in your system PATH
- Check Python installation: `python --version` or `python3 --version`
- Set custom Python path in VS Code settings if needed

#### "Module not found" Error
- Install missing Python packages: `pip install -r requirements.txt`
- The extension will prompt to install missing dependencies automatically

#### PDF Generation Fails
- Ensure system dependencies are installed (see Requirements section)
- Check WeasyPrint installation: `python -c "import weasyprint"`
- On Windows, ensure GTK3 is properly installed

#### OpenAI API Key Issues
- Verify your API key is valid and has sufficient credits
- Check environment variable is set correctly: `echo $OPENAI_API_KEY`
- Try setting the API key in VS Code settings instead

#### Extension Not Working
1. Check VS Code Output panel for detailed logs
2. Verify all dependencies are installed
3. Restart VS Code after installing dependencies
4. Check Python path in extension settings

### Getting Help

1. **Check Output Panel**: View detailed logs in VS Code Output panel
2. **Check Requirements**: Ensure all system and Python dependencies are installed
3. **Restart VS Code**: Sometimes needed after installing dependencies
4. **Manual Testing**: Try running the Python CLI directly:
   ```bash
   python -m core path/to/notebook.ipynb output/
   ```

## Development

### Building the Extension

```bash
cd vscode-extension
npm install
npm run compile
```

### Packaging the Extension

```bash
npm install -g vsce
vsce package
```

### Testing

1. Open the extension folder in VS Code
2. Press `F5` to launch Extension Development Host
3. Test the extension functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This extension is part of the notebook documentation generator project. See the main project LICENSE file for details.

## Support

For issues and feature requests, please use the GitHub issue tracker. Include:
- VS Code version
- Extension version
- Operating system
- Error messages from Output panel
- Steps to reproduce the issue
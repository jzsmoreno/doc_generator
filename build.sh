#!/bin/bash

# Build script for Notebook Documentation Generator
# This script packages both the Python package and VS Code extension

set -e

echo "=== Notebook Documentation Generator Build Script ==="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ] || [ ! -d "core" ]; then
    print_error "Please run this script from the doc_generator root directory"
    exit 1
fi

print_status "Starting build process..."

# Step 1: Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/ vscode-extension/out/ vscode-extension/node_modules/ vscode-extension/*.vsix

# Step 2: Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Step 3: Test Python package
print_status "Testing Python package..."
python -c "import core; print('✓ Core package imported successfully')"
python -m core --help > /dev/null && echo "✓ CLI help works" || echo "✗ CLI help failed"

# Step 4: Build VS Code extension
print_status "Building VS Code extension..."
cd vscode-extension

# Install npm dependencies
npm install

# Compile TypeScript
npm run compile

# Package extension
if command -v vsce &> /dev/null; then
    vsce package
    print_status "VS Code extension packaged successfully!"
else
    print_warning "vsce not found. Install with: npm install -g vsce"
    print_warning "Extension packaging skipped"
fi

cd ..

# Step 5: Create distribution package
print_status "Creating distribution package..."
mkdir -p dist

# Copy important files
cp -r core dist/
cp -r vscode-extension dist/
cp requirements.txt dist/
cp README.md dist/
cp INSTALLATION.md dist/
cp TESTING.md dist/

# Create installation script
cat > dist/install.sh << 'EOF'
#!/bin/bash

echo "Installing Notebook Documentation Generator..."

# Install Python package
pip install -r requirements.txt

# Install VS Code extension
if [ -f "vscode-extension/*.vsix" ]; then
    echo "Please install the VS Code extension manually:"
    echo "1. Open VS Code"
    echo "2. Go to Extensions view (Ctrl+Shift+X)"
    echo "3. Click menu → Install from VSIX"
    echo "4. Select the .vsix file from vscode-extension folder"
else
    echo "VS Code extension files available in vscode-extension folder"
fi

echo "Installation complete!"
echo "Next steps:"
echo "1. Configure your OpenAI API key in VS Code settings"
echo "2. Test with a Jupyter notebook"
EOF

chmod +x dist/install.sh

# Step 6: Final verification
print_status "Running final verification..."
if python -c "import core" 2>/dev/null; then
    print_status "✓ Python package verification passed"
else
    print_error "✗ Python package verification failed"
    exit 1
fi

# Step 7: Create README for distribution
cat > dist/README.md << 'EOF'
# Notebook Documentation Generator - Distribution Package

This package contains:
- Core Python package for documentation generation
- VS Code extension for integration
- Installation and usage guides

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install VS Code extension**:
   - Open VS Code
   - Install from VSIX file in `vscode-extension/` folder

3. **Configure OpenAI API key** in VS Code settings

4. **Test installation**:
   ```bash
   python -m core --help
   ```

## Documentation
- `INSTALLATION.md` - Detailed installation guide
- `TESTING.md` - Testing procedures
- `README.md` - Main documentation

For more information, see the main repository.
EOF

print_status "Build completed successfully!"
print_status "Distribution package created in 'dist/' folder"
print_status "VS Code extension available in 'dist/vscode-extension/'"
print
print_status "Next steps:"
echo "1. Install the VS Code extension from dist/vscode-extension/"
echo "2. Configure your OpenAI API key"
echo "3. Test with: python -m core notebooks/Deep_Models.ipynb output/test --no-pdf"
echo
print_status "Build script finished!"
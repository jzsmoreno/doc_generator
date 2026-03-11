@echo off
REM Build script for Notebook Documentation Generator (Windows)
REM This script packages both the Python package and VS Code extension

echo === Notebook Documentation Generator Build Script ===
echo.

REM Check if we're in the right directory
if not exist "requirements.txt" (
    echo [ERROR] Please run this script from the doc_generator root directory
    exit /b 1
)

if not exist "core" (
    echo [ERROR] Please run this script from the doc_generator root directory
    exit /b 1
)

echo [INFO] Starting build process...
echo.

REM Step 1: Clean previous builds
echo [INFO] Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.egg-info" rmdir /s /q *.egg-info
if exist "vscode-extension\out" rmdir /s /q vscode-extension\out
if exist "vscode-extension\node_modules" rmdir /s /q vscode-extension\node_modules
if exist "vscode-extension\*.vsix" del vscode-extension\*.vsix

REM Step 2: Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    exit /b 1
)

REM Step 3: Test Python package
echo [INFO] Testing Python package...
python -c "import core; print('Core package imported successfully')"
if errorlevel 1 (
    echo [ERROR] Python package test failed
    exit /b 1
)

python -m core --help > nul
if errorlevel 1 (
    echo [WARNING] CLI help test failed
) else (
    echo CLI help works
)

REM Step 4: Build VS Code extension
echo [INFO] Building VS Code extension...
cd vscode-extension

REM Install npm dependencies
call npm install
if errorlevel 1 (
    echo [ERROR] npm install failed
    exit /b 1
)

REM Compile TypeScript
call npm run compile
if errorlevel 1 (
    echo [ERROR] TypeScript compilation failed
    exit /b 1
)

REM Package extension
where vsce >nul 2>nul
if %errorlevel%==0 (
    vsce package
    echo [INFO] VS Code extension packaged successfully!
) else (
    echo [WARNING] vsce not found. Install with: npm install -g vsce
    echo [WARNING] Extension packaging skipped
)

cd ..

REM Step 5: Create distribution package
echo [INFO] Creating distribution package...
if not exist "dist" mkdir dist

REM Copy important files
xcopy /E /I /Y core dist\core
xcopy /E /I /Y vscode-extension dist\vscode-extension
copy /Y requirements.txt dist\
copy /Y README.md dist\
copy /Y INSTALLATION.md dist\
copy /Y TESTING.md dist\

REM Create installation script
echo @echo off > dist\install.bat
echo echo Installing Notebook Documentation Generator... >> dist\install.bat
echo echo. >> dist\install.bat
echo echo Installing Python dependencies... >> dist\install.bat
echo pip install -r requirements.txt >> dist\install.bat
echo echo. >> dist\install.bat
echo echo Installation complete! >> dist\install.bat
echo echo. >> dist\install.bat
echo echo Next steps: >> dist\install.bat
echo echo 1. Install the VS Code extension from vscode-extension folder >> dist\install.bat
echo echo 2. Configure your OpenAI API key in VS Code settings >> dist\install.bat
echo echo 3. Test with: python -m core notebooks\Deep_Models.ipynb output\test --no-pdf >> dist\install.bat
echo pause >> dist\install.bat

REM Step 6: Final verification
echo [INFO] Running final verification...
python -c "import core" 2>nul
if errorlevel 1 (
    echo [ERROR] Python package verification failed
    exit /b 1
)
echo [INFO] Python package verification passed

REM Step 7: Create README for distribution
echo # Notebook Documentation Generator - Distribution Package > dist\README.md
echo. >> dist\README.md
echo This package contains: >> dist\README.md
echo - Core Python package for documentation generation >> dist\README.md
echo - VS Code extension for integration >> dist\README.md
echo - Installation and usage guides >> dist\README.md
echo. >> dist\README.md
echo ## Quick Start >> dist\README.md
echo. >> dist\README.md
echo 1. **Install dependencies**: >> dist\README.md
echo    ```batch >> dist\README.md
echo    pip install -r requirements.txt >> dist\README.md
echo    ``` >> dist\README.md
echo. >> dist\README.md
echo 2. **Install VS Code extension**: >> dist\README.md
echo    - Open VS Code >> dist\README.md
echo    - Install from VSIX file in `vscode-extension\` folder >> dist\README.md
echo. >> dist\README.md
echo 3. **Configure OpenAI API key** in VS Code settings >> dist\README.md
echo. >> dist\README.md
echo 4. **Test installation**: >> dist\README.md
echo    ```batch >> dist\README.md
echo    python -m core --help >> dist\README.md
echo    ``` >> dist\README.md
echo. >> dist\README.md
echo ## Documentation >> dist\README.md
echo - `INSTALLATION.md` - Detailed installation guide >> dist\README.md
echo - `TESTING.md` - Testing procedures >> dist\README.md
echo - `README.md` - Main documentation >> dist\README.md
echo. >> dist\README.md
echo For more information, see the main repository. >> dist\README.md

echo [INFO] Build completed successfully!
echo [INFO] Distribution package created in 'dist\' folder
echo [INFO] VS Code extension available in 'dist\vscode-extension\'
echo.
echo [INFO] Next steps:
echo 1. Install the VS Code extension from dist\vscode-extension\
echo 2. Configure your OpenAI API key
echo 3. Test with: python -m core notebooks\Deep_Models.ipynb output\test --no-pdf
echo.
echo [INFO] Build script finished!
pause
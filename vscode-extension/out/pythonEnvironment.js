"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getPythonCommand = exports.checkPythonEnvironment = void 0;
const vscode = __importStar(require("vscode"));
const cp = __importStar(require("child_process"));
const fs = __importStar(require("fs"));
/**
 * Checks if Python is available in the system and if required dependencies are installed.
 * @param outputChannel The output channel to write logs to
 * @returns Promise<boolean> True if Python environment is valid, false otherwise
 */
async function checkPythonEnvironment(outputChannel) {
    outputChannel.appendLine('Checking Python environment...');
    try {
        // Find Python executable
        const pythonCommand = findPythonCommand();
        if (!pythonCommand) {
            outputChannel.appendLine('ERROR: Python not found. Please install Python and add it to your PATH.');
            return false;
        }
        outputChannel.appendLine(`Found Python: ${pythonCommand}`);
        // Check Python version
        const version = await getPythonVersion(pythonCommand);
        if (version) {
            outputChannel.appendLine(`Python version: ${version}`);
        }
        // Check if required packages are installed
        const requiredPackages = ['openai', 'nbconvert', 'nbformat', 'markdown'];
        const missingPackages = [];
        for (const packageName of requiredPackages) {
            const isInstalled = await checkPackageInstalled(pythonCommand, packageName);
            if (isInstalled) {
                outputChannel.appendLine(`✓ ${packageName} is installed`);
            }
            else {
                outputChannel.appendLine(`✗ ${packageName} is NOT installed`);
                missingPackages.push(packageName);
            }
        }
        // Check optional packages for PDF generation
        const optionalPackages = ['weasyprint', 'pypandoc'];
        for (const packageName of optionalPackages) {
            const isInstalled = await checkPackageInstalled(pythonCommand, packageName);
            if (isInstalled) {
                outputChannel.appendLine(`✓ ${packageName} is installed (optional)`);
            }
            else {
                outputChannel.appendLine(`- ${packageName} is NOT installed (optional)`);
            }
        }
        if (missingPackages.length > 0) {
            outputChannel.appendLine(`\nPlease install missing packages:`);
            outputChannel.appendLine(`pip install ${missingPackages.join(' ')}`);
            vscode.window.showWarningMessage(`Missing Python packages: ${missingPackages.join(', ')}. Please install them.`, 'Show Output').then(selection => {
                if (selection === 'Show Output') {
                    outputChannel.show();
                }
            });
            return false;
        }
        outputChannel.appendLine('Python environment is ready!');
        return true;
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        outputChannel.appendLine(`Error checking Python environment: ${errorMessage}`);
        return false;
    }
}
exports.checkPythonEnvironment = checkPythonEnvironment;
/**
 * Finds the Python command available on the system
 * @returns The Python command string or null if not found
 */
function findPythonCommand() {
    // Try to get Python path from configuration
    const config = vscode.workspace.getConfiguration('notebookDocGenerator');
    const pythonPath = config.get('pythonPath');
    if (pythonPath && fs.existsSync(pythonPath)) {
        return pythonPath;
    }
    // Try common Python commands based on platform
    const commands = process.platform === 'win32'
        ? ['python', 'python3', 'py']
        : ['python3', 'python'];
    for (const cmd of commands) {
        try {
            cp.execSync(`${cmd} --version`, { stdio: 'ignore' });
            return cmd;
        }
        catch {
            // Continue to next command
        }
    }
    return null;
}
/**
 * Gets the Python version string
 * @param pythonCommand The Python command to check
 * @returns Promise<string | null> The version string or null if not available
 */
async function getPythonVersion(pythonCommand) {
    return new Promise((resolve) => {
        cp.exec(`${pythonCommand} --version`, (error, stdout, stderr) => {
            if (error) {
                resolve(null);
                return;
            }
            resolve(stdout || stderr);
        });
    });
}
/**
 * Checks if a Python package is installed
 * @param pythonCommand The Python command to use
 * @param packageName The package name to check
 * @returns Promise<boolean> True if the package is installed
 */
async function checkPackageInstalled(pythonCommand, packageName) {
    return new Promise((resolve) => {
        // Map package names to their import names
        const importNames = {
            'openai': 'openai',
            'nbconvert': 'nbconvert',
            'nbformat': 'nbformat',
            'markdown': 'markdown',
            'weasyprint': 'weasyprint',
            'pypandoc': 'pypandoc'
        };
        const importName = importNames[packageName] || packageName;
        cp.exec(`${pythonCommand} -c "import ${importName}"`, (error) => {
            resolve(!error);
        });
    });
}
/**
 * Gets the Python command based on configuration or system PATH
 * @returns The Python command string
 */
function getPythonCommand() {
    const config = vscode.workspace.getConfiguration('notebookDocGenerator');
    const pythonPath = config.get('pythonPath');
    if (pythonPath && fs.existsSync(pythonPath)) {
        return pythonPath;
    }
    // Default to python or python3 based on platform
    return process.platform === 'win32' ? 'python' : 'python3';
}
exports.getPythonCommand = getPythonCommand;
//# sourceMappingURL=pythonEnvironment.js.map
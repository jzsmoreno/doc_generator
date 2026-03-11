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
exports.checkSystemDependencies = exports.checkPythonDependencies = exports.runPythonCLI = exports.killCurrentProcess = void 0;
const vscode = __importStar(require("vscode"));
const cp = __importStar(require("child_process"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
// Store the current running process for cancellation
let currentProcess = null;
let currentOutputChannel = null;
function killCurrentProcess() {
    if (currentProcess) {
        if (currentOutputChannel) {
            currentOutputChannel.appendLine('Killing current process...');
        }
        currentProcess.kill('SIGTERM');
        // Force kill after 5 seconds if still running
        setTimeout(() => {
            if (currentProcess && !currentProcess.killed) {
                currentProcess.kill('SIGKILL');
            }
        }, 5000);
        currentProcess = null;
    }
}
exports.killCurrentProcess = killCurrentProcess;
async function runPythonCLI(inputPath, outputDir, outputChannel, config, extensionUri) {
    return new Promise((resolve) => {
        try {
            // Find the workspace folder
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
            if (!workspaceFolder) {
                resolve({
                    success: false,
                    error: 'No workspace folder found'
                });
                return;
            }
            // Determine core module path - prefer extension path for self-contained package
            let coreModulePath;
            let coreModuleWorkingDir;
            if (extensionUri) {
                // Use core from extension path (for packaged extension)
                coreModulePath = path.join(extensionUri.fsPath, 'core');
                coreModuleWorkingDir = extensionUri.fsPath;
            }
            else {
                // Fall back to workspace folder (for development)
                coreModulePath = path.join(workspaceFolder, 'core');
                coreModuleWorkingDir = workspaceFolder;
            }
            // Check if core module exists
            if (!fs.existsSync(coreModulePath)) {
                const errorMsg = extensionUri
                    ? `Core Python module not found in extension at: ${coreModulePath}. Please reinstall the extension.`
                    : 'Core Python module not found. Please ensure the core/ directory exists in your workspace.';
                resolve({
                    success: false,
                    error: errorMsg
                });
                return;
            }
            // Check if Python is available
            const pythonCommand = getPythonCommand();
            // Build CLI arguments - ensure outputDir is an absolute path
            let cliArgs = `"${inputPath}" "${outputDir}"`;
            // Add model if specified
            if (config?.model) {
                cliArgs += ` --model ${config.model}`;
            }
            // Add language if specified
            if (config?.language) {
                cliArgs += ` --language ${config.language}`;
            }
            // Add API key if specified
            if (config?.apiKey) {
                cliArgs += ` --api-key ${config.apiKey}`;
            }
            // Add API base URL if specified
            if (config?.apiBaseUrl) {
                cliArgs += ` --api-base ${config.apiBaseUrl}`;
            }
            // Skip PDF if specified
            if (config?.generatePdf === false) {
                cliArgs += ` --no-pdf`;
            }
            // Build the command - use core module
            const cmd = `${pythonCommand} -m core ${cliArgs}`;
            // Store output channel for cancellation
            currentOutputChannel = outputChannel;
            outputChannel.appendLine(`Executing: ${cmd}`);
            outputChannel.appendLine(`Working directory: ${coreModuleWorkingDir}`);
            outputChannel.appendLine(`Core module path: ${coreModulePath}`);
            // Execute the command - use coreModuleWorkingDir so python -m core works correctly
            currentProcess = cp.exec(cmd, { cwd: coreModuleWorkingDir }, (error, stdout, stderr) => {
                currentProcess = null;
                if (stdout) {
                    outputChannel.appendLine('Python CLI Output:');
                    outputChannel.appendLine(stdout);
                }
                if (stderr) {
                    outputChannel.appendLine('Python CLI Errors:');
                    outputChannel.appendLine(stderr);
                }
                if (error) {
                    resolve({
                        success: false,
                        error: `Process error: ${error.message}`,
                        stdout,
                        stderr
                    });
                }
                else {
                    resolve({
                        success: true,
                        stdout,
                        stderr
                    });
                }
            });
            // Handle process events
            currentProcess.on('exit', (code) => {
                outputChannel.appendLine(`Python CLI process exited with code: ${code}`);
            });
        }
        catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            resolve({
                success: false,
                error: errorMessage
            });
        }
    });
}
exports.runPythonCLI = runPythonCLI;
function getPythonCommand() {
    // Try to get Python command from configuration
    const config = vscode.workspace.getConfiguration('notebookDocGenerator');
    const pythonPath = config.get('pythonPath');
    if (pythonPath && fs.existsSync(pythonPath)) {
        return `"${pythonPath}"`;
    }
    // Try common Python commands
    const pythonCommands = ['python3', 'python'];
    for (const cmd of pythonCommands) {
        try {
            cp.execSync(`${cmd} --version`, { stdio: 'ignore' });
            return cmd;
        }
        catch {
            // Continue to next command
        }
    }
    // Default to python
    return 'python';
}
async function checkPythonDependencies(outputChannel) {
    try {
        const pythonCommand = getPythonCommand();
        // Check if required packages are installed
        const requiredPackages = ['openai', 'nbconvert', 'nbformat', 'markdown', 'weasyprint', 'pypandoc'];
        for (const packageName of requiredPackages) {
            try {
                cp.execSync(`${pythonCommand} -c "import ${packageName}"`, { stdio: 'ignore' });
                outputChannel.appendLine(`✓ ${packageName} is installed`);
            }
            catch {
                outputChannel.appendLine(`✗ ${packageName} is NOT installed`);
                vscode.window.showWarningMessage(`Python package '${packageName}' is not installed. Please install it using: pip install ${packageName}`);
                return false;
            }
        }
        return true;
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        outputChannel.appendLine(`Failed to check Python dependencies: ${errorMessage}`);
        return false;
    }
}
exports.checkPythonDependencies = checkPythonDependencies;
async function checkSystemDependencies(outputChannel) {
    try {
        // Check for system dependencies needed for PDF generation
        const platform = process.platform;
        if (platform === 'win32') {
            // Windows-specific checks
            outputChannel.appendLine('Checking Windows dependencies...');
            // WeasyPrint on Windows might need additional setup
        }
        else if (platform === 'darwin') {
            // macOS-specific checks
            outputChannel.appendLine('Checking macOS dependencies...');
        }
        else {
            // Linux-specific checks
            outputChannel.appendLine('Checking Linux dependencies...');
        }
        // For now, we'll assume system dependencies are available
        // In a production environment, you might want to add more specific checks
        return true;
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        outputChannel.appendLine(`Failed to check system dependencies: ${errorMessage}`);
        return false;
    }
}
exports.checkSystemDependencies = checkSystemDependencies;
//# sourceMappingURL=pythonRunner.js.map
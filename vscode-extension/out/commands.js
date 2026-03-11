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
exports.setExtensionUri = exports.registerCommands = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const pythonRunner_1 = require("./pythonRunner");
const utils_1 = require("./utils");
const configManager_1 = require("./configManager");
function registerCommands(context, outputChannel, extensionUri) {
    // Store extension URI for use in commands
    setExtensionUri(extensionUri);
    // Command for active notebook
    const generateActiveNotebookCommand = vscode.commands.registerCommand('extension.generateNotebookDocumentation', async () => {
        await generateDocumentationForActiveNotebook(outputChannel);
    });
    // Command for selected file (right-click)
    const generateSelectedNotebookCommand = vscode.commands.registerCommand('extension.generateSelectedNotebookDocumentation', async (uri) => {
        await generateDocumentationForSelectedNotebook(uri, outputChannel);
    });
    // Command for folder
    const generateFolderCommand = vscode.commands.registerCommand('extension.generateFolderDocumentation', async (uri) => {
        await generateDocumentationForFolder(uri, outputChannel);
    });
    context.subscriptions.push(generateActiveNotebookCommand, generateSelectedNotebookCommand, generateFolderCommand);
}
exports.registerCommands = registerCommands;
// Global variable to store extension URI
let extensionUri;
function setExtensionUri(uri) {
    extensionUri = uri;
}
exports.setExtensionUri = setExtensionUri;
async function generateDocumentationForActiveNotebook(outputChannel) {
    try {
        const notebookPath = await (0, utils_1.getCurrentNotebookPath)();
        if (!notebookPath) {
            vscode.window.showWarningMessage('No active notebook found. Please open a Jupyter notebook.');
            return;
        }
        await generateDocumentation(notebookPath, outputChannel, extensionUri);
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        vscode.window.showErrorMessage(`Failed to generate documentation: ${errorMessage}`);
        outputChannel.appendLine(`Error: ${errorMessage}`);
    }
}
async function generateDocumentationForSelectedNotebook(uri, outputChannel) {
    try {
        if (!uri.fsPath.endsWith('.ipynb')) {
            vscode.window.showWarningMessage('Please select a Jupyter notebook file (.ipynb)');
            return;
        }
        await generateDocumentation(uri.fsPath, outputChannel, extensionUri);
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        vscode.window.showErrorMessage(`Failed to generate documentation: ${errorMessage}`);
        outputChannel.appendLine(`Error: ${errorMessage}`);
    }
}
async function generateDocumentationForFolder(uri, outputChannel) {
    try {
        const folderPath = uri.fsPath;
        if (!fs.existsSync(folderPath)) {
            vscode.window.showErrorMessage('Selected folder does not exist');
            return;
        }
        const stats = fs.statSync(folderPath);
        if (!stats.isDirectory()) {
            vscode.window.showErrorMessage('Please select a folder, not a file');
            return;
        }
        // Check if there are any .ipynb files in the folder
        const notebookFiles = fs.readdirSync(folderPath)
            .filter(file => file.endsWith('.ipynb'))
            .map(file => path.join(folderPath, file));
        if (notebookFiles.length === 0) {
            vscode.window.showInformationMessage('No Jupyter notebooks found in the selected folder');
            return;
        }
        outputChannel.appendLine(`Found ${notebookFiles.length} notebook(s) in folder: ${folderPath}`);
        // Generate documentation for all notebooks in the folder
        await generateDocumentation(folderPath, outputChannel, extensionUri);
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        vscode.window.showErrorMessage(`Failed to generate folder documentation: ${errorMessage}`);
        outputChannel.appendLine(`Error: ${errorMessage}`);
    }
}
async function generateDocumentation(inputPath, outputChannel, extensionUri) {
    try {
        // Get configuration
        const configManager = new configManager_1.ConfigManager();
        const config = {
            model: configManager.model,
            language: configManager.language,
            generatePdf: configManager.generatePdf,
            apiKey: configManager.openaiApiKey,
            apiBaseUrl: configManager.apiBaseUrl
        };
        // Validate configuration
        const validation = configManager.validateConfig();
        if (!validation.valid) {
            vscode.window.showErrorMessage(validation.errors.join('\n'));
            return;
        }
        // Show progress notification with cancellation support
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Generating notebook documentation...',
            cancellable: true
        }, async (progress, cancellationToken) => {
            progress.report({ increment: 0, message: 'Starting documentation generation...' });
            // Handle cancellation
            cancellationToken.onCancellationRequested(() => {
                outputChannel.appendLine('Cancellation requested. Stopping process...');
                (0, pythonRunner_1.killCurrentProcess)();
                vscode.window.showInformationMessage('Documentation generation cancelled.');
            });
            // Determine output directory
            const workspaceFolder = (0, utils_1.getWorkspaceFolder)();
            if (!workspaceFolder) {
                vscode.window.showErrorMessage('No workspace folder found. Please open a folder in VS Code.');
                return;
            }
            const outputDir = path.join(workspaceFolder, 'output');
            if (!fs.existsSync(outputDir)) {
                fs.mkdirSync(outputDir, { recursive: true });
            }
            outputChannel.appendLine(`Input path: ${inputPath}`);
            outputChannel.appendLine(`Output directory: ${outputDir}`);
            outputChannel.appendLine(`Using model: ${config.model}`);
            outputChannel.appendLine(`Language: ${config.language}`);
            progress.report({ increment: 30, message: 'Running Python CLI...' });
            // Run the Python CLI with config - pass extensionUri for self-contained core module
            const result = await (0, pythonRunner_1.runPythonCLI)(inputPath, outputDir, outputChannel, config, extensionUri);
            progress.report({ increment: 70, message: 'Processing results...' });
            if (result.success) {
                const successMessage = `Documentation generated successfully!\nOutput: ${outputDir}`;
                vscode.window.showInformationMessage(successMessage);
                outputChannel.appendLine('Documentation generation completed successfully');
                // Open the output folder in VS Code
                const outputUri = vscode.Uri.file(outputDir);
                vscode.commands.executeCommand('revealInExplorer', outputUri);
            }
            else {
                throw new Error(result.error || 'Documentation generation failed');
            }
        });
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        vscode.window.showErrorMessage(`Documentation generation failed: ${errorMessage}`);
        outputChannel.appendLine(`Documentation generation failed: ${errorMessage}`);
        throw error;
    }
}
//# sourceMappingURL=commands.js.map
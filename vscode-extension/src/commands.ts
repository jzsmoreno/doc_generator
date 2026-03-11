import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { OutputChannel } from './outputChannel';
import { runPythonCLI, CLIConfig, killCurrentProcess } from './pythonRunner';
import { getCurrentNotebookPath, getSelectedFilePath, getWorkspaceFolder } from './utils';
import { ConfigManager } from './configManager';

export function registerCommands(context: vscode.ExtensionContext, outputChannel: OutputChannel, extensionUri: vscode.Uri) {
    // Store extension URI for use in commands
    setExtensionUri(extensionUri);
    
    // Command for active notebook
    const generateActiveNotebookCommand = vscode.commands.registerCommand(
        'extension.generateNotebookDocumentation',
        async () => {
            await generateDocumentationForActiveNotebook(outputChannel);
        }
    );

    // Command for selected file (right-click)
    const generateSelectedNotebookCommand = vscode.commands.registerCommand(
        'extension.generateSelectedNotebookDocumentation',
        async (uri: vscode.Uri) => {
            await generateDocumentationForSelectedNotebook(uri, outputChannel);
        }
    );

    // Command for folder
    const generateFolderCommand = vscode.commands.registerCommand(
        'extension.generateFolderDocumentation',
        async (uri: vscode.Uri) => {
            await generateDocumentationForFolder(uri, outputChannel);
        }
    );

    context.subscriptions.push(
        generateActiveNotebookCommand,
        generateSelectedNotebookCommand,
        generateFolderCommand
    );
}

// Global variable to store extension URI
let extensionUri: vscode.Uri;

export function setExtensionUri(uri: vscode.Uri) {
    extensionUri = uri;
}

async function generateDocumentationForActiveNotebook(outputChannel: OutputChannel): Promise<void> {
    try {
        const notebookPath = await getCurrentNotebookPath();
        if (!notebookPath) {
            vscode.window.showWarningMessage('No active notebook found. Please open a Jupyter notebook.');
            return;
        }

        await generateDocumentation(notebookPath, outputChannel, extensionUri);
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        vscode.window.showErrorMessage(`Failed to generate documentation: ${errorMessage}`);
        outputChannel.appendLine(`Error: ${errorMessage}`);
    }
}

async function generateDocumentationForSelectedNotebook(uri: vscode.Uri, outputChannel: OutputChannel): Promise<void> {
    try {
        if (!uri.fsPath.endsWith('.ipynb')) {
            vscode.window.showWarningMessage('Please select a Jupyter notebook file (.ipynb)');
            return;
        }

        await generateDocumentation(uri.fsPath, outputChannel, extensionUri);
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        vscode.window.showErrorMessage(`Failed to generate documentation: ${errorMessage}`);
        outputChannel.appendLine(`Error: ${errorMessage}`);
    }
}

async function generateDocumentationForFolder(uri: vscode.Uri, outputChannel: OutputChannel): Promise<void> {
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
        
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        vscode.window.showErrorMessage(`Failed to generate folder documentation: ${errorMessage}`);
        outputChannel.appendLine(`Error: ${errorMessage}`);
    }
}

async function generateDocumentation(inputPath: string, outputChannel: OutputChannel, extensionUri: vscode.Uri): Promise<void> {
    try {
        // Get configuration
        const configManager = new ConfigManager();
        const config: CLIConfig = {
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
                killCurrentProcess();
                vscode.window.showInformationMessage('Documentation generation cancelled.');
            });

            // Determine output directory
            const workspaceFolder = getWorkspaceFolder();
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
            const result = await runPythonCLI(inputPath, outputDir, outputChannel, config, extensionUri);

            progress.report({ increment: 70, message: 'Processing results...' });

            if (result.success) {
                const successMessage = `Documentation generated successfully!\nOutput: ${outputDir}`;
                vscode.window.showInformationMessage(successMessage);
                outputChannel.appendLine('Documentation generation completed successfully');
                
                // Open the output folder in VS Code
                const outputUri = vscode.Uri.file(outputDir);
                vscode.commands.executeCommand('revealInExplorer', outputUri);
            } else {
                throw new Error(result.error || 'Documentation generation failed');
            }
        });

    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        vscode.window.showErrorMessage(`Documentation generation failed: ${errorMessage}`);
        outputChannel.appendLine(`Documentation generation failed: ${errorMessage}`);
        throw error;
    }
}


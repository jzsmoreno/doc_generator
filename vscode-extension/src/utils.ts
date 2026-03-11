import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Gets the path of the currently active notebook
 * @returns Promise<string | null> The notebook path or null if no notebook is active
 */
export async function getCurrentNotebookPath(): Promise<string | null> {
    // Check if there's an active notebook editor (this is the correct way for VS Code)
    const activeNotebookEditor = vscode.window.activeNotebookEditor;
    if (activeNotebookEditor) {
        return activeNotebookEditor.notebook.uri.fsPath;
    }
    
    // Fallback: Check if there's a notebook document open
    const notebookDocuments = vscode.workspace.notebookDocuments;
    for (const doc of notebookDocuments) {
        if (doc.uri.fsPath.endsWith('.ipynb')) {
            return doc.uri.fsPath;
        }
    }
    
    // Fallback: Check active text editor (for older VS Code versions or other edge cases)
    const editor = vscode.window.activeTextEditor;
    if (editor) {
        const document = editor.document;
        if (document.languageId === 'jupyter' || document.uri.fsPath.endsWith('.ipynb')) {
            return document.uri.fsPath;
        }
    }
    
    return null;
}

/**
 * Gets the path of the selected file from the explorer or editor
 * @returns Promise<string | null> The selected file path or null if nothing is selected
 */
export async function getSelectedFilePath(): Promise<string | null> {
    // Check active editor first
    const editor = vscode.window.activeTextEditor;
    if (editor) {
        return editor.document.uri.fsPath;
    }
    
    // Check for selected resource in explorer
    const selection = vscode.window.activeTextEditor?.selection;
    if (selection) {
        const document = vscode.window.activeTextEditor?.document;
        if (document) {
            return document.uri.fsPath;
        }
    }
    
    return null;
}

/**
 * Gets the workspace folder path
 * @returns string | null The workspace folder path or null if no workspace is open
 */
export function getWorkspaceFolder(): string | null {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    
    if (!workspaceFolders || workspaceFolders.length === 0) {
        return null;
    }
    
    // Return the first workspace folder
    return workspaceFolders[0].uri.fsPath;
}

/**
 * Gets all notebook files in a given directory
 * @param directoryPath The directory path to search
 * @returns string[] Array of notebook file paths
 */
export function getNotebookFilesInDirectory(directoryPath: string): string[] {
    try {
        const files = fs.readdirSync(directoryPath);
        return files
            .filter((file: string) => file.endsWith('.ipynb'))
            .map((file: string) => path.join(directoryPath, file));
    } catch (error) {
        console.error('Error reading directory:', error);
        return [];
    }
}

/**
 * Validates if a given path is a valid notebook file
 * @param filePath The file path to validate
 * @returns boolean True if the path is a valid notebook file
 */
export function isValidNotebook(filePath: string): boolean {
    return filePath.endsWith('.ipynb');
}

/**
 * Gets the output filename for a given notebook
 * @param notebookPath The notebook path
 * @returns string The output markdown filename
 */
export function getOutputFilename(notebookPath: string): string {
    const basename = path.basename(notebookPath, '.ipynb');
    return `${basename}.md`;
}


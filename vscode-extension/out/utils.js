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
exports.getOutputFilename = exports.isValidNotebook = exports.getNotebookFilesInDirectory = exports.getWorkspaceFolder = exports.getSelectedFilePath = exports.getCurrentNotebookPath = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
/**
 * Gets the path of the currently active notebook
 * @returns Promise<string | null> The notebook path or null if no notebook is active
 */
async function getCurrentNotebookPath() {
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
exports.getCurrentNotebookPath = getCurrentNotebookPath;
/**
 * Gets the path of the selected file from the explorer or editor
 * @returns Promise<string | null> The selected file path or null if nothing is selected
 */
async function getSelectedFilePath() {
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
exports.getSelectedFilePath = getSelectedFilePath;
/**
 * Gets the workspace folder path
 * @returns string | null The workspace folder path or null if no workspace is open
 */
function getWorkspaceFolder() {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders || workspaceFolders.length === 0) {
        return null;
    }
    // Return the first workspace folder
    return workspaceFolders[0].uri.fsPath;
}
exports.getWorkspaceFolder = getWorkspaceFolder;
/**
 * Gets all notebook files in a given directory
 * @param directoryPath The directory path to search
 * @returns string[] Array of notebook file paths
 */
function getNotebookFilesInDirectory(directoryPath) {
    try {
        const files = fs.readdirSync(directoryPath);
        return files
            .filter((file) => file.endsWith('.ipynb'))
            .map((file) => path.join(directoryPath, file));
    }
    catch (error) {
        console.error('Error reading directory:', error);
        return [];
    }
}
exports.getNotebookFilesInDirectory = getNotebookFilesInDirectory;
/**
 * Validates if a given path is a valid notebook file
 * @param filePath The file path to validate
 * @returns boolean True if the path is a valid notebook file
 */
function isValidNotebook(filePath) {
    return filePath.endsWith('.ipynb');
}
exports.isValidNotebook = isValidNotebook;
/**
 * Gets the output filename for a given notebook
 * @param notebookPath The notebook path
 * @returns string The output markdown filename
 */
function getOutputFilename(notebookPath) {
    const basename = path.basename(notebookPath, '.ipynb');
    return `${basename}.md`;
}
exports.getOutputFilename = getOutputFilename;
//# sourceMappingURL=utils.js.map
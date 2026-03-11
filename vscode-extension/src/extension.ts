import * as vscode from 'vscode';
import { OutputChannel } from './outputChannel';
import { registerCommands } from './commands';
import { checkPythonEnvironment } from './pythonEnvironment';

let outputChannel: OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    console.log('Notebook Documentation Generator extension is now active!');
    
    // Initialize output channel
    outputChannel = new OutputChannel();
    context.subscriptions.push(outputChannel);
    
    // Check Python environment
    checkPythonEnvironment(outputChannel).then(isValid => {
        if (!isValid) {
            vscode.window.showWarningMessage(
                'Python environment not properly configured. Please check the output panel for details.',
                'Show Output'
            ).then(selection => {
                if (selection === 'Show Output') {
                    outputChannel.show();
                }
            });
        }
    });
    
    // Register commands - pass extension URI for self-contained core module
    registerCommands(context, outputChannel, context.extensionUri);
    
    // Show activation message
    vscode.window.showInformationMessage('Notebook Documentation Generator extension activated!');
}

export function deactivate() {
    console.log('Notebook Documentation Generator extension is now deactivated!');
}
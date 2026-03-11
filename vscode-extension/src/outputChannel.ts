import * as vscode from 'vscode';

export class OutputChannel {
    private channel: vscode.OutputChannel;

    constructor() {
        this.channel = vscode.window.createOutputChannel('Notebook Documentation Generator');
    }

    appendLine(message: string): void {
        this.channel.appendLine(`[${new Date().toLocaleTimeString()}] ${message}`);
    }

    append(message: string): void {
        this.channel.append(message);
    }

    show(): void {
        this.channel.show();
    }

    clear(): void {
        this.channel.clear();
    }

    dispose(): void {
        this.channel.dispose();
    }
}
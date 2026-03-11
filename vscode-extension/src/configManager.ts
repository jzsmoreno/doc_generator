import * as vscode from 'vscode';

export interface ExtensionConfig {
    openaiApiKey: string;
    model: string;
    language: string;
    generatePdf: boolean;
    pythonPath: string;
    apiBaseUrl: string;
}

export class ConfigManager {
    private config: vscode.WorkspaceConfiguration;

    constructor() {
        this.config = vscode.workspace.getConfiguration('notebookDocGenerator');
    }

    get openaiApiKey(): string {
        return this.config.get<string>('openaiApiKey') || '';
    }

    get model(): string {
        return this.config.get<string>('model') || 'gpt-4';
    }

    get language(): string {
        return this.config.get<string>('language') || 'english';
    }

    get generatePdf(): boolean {
        return this.config.get<boolean>('generatePdf') !== false;
    }

    get pythonPath(): string {
        return this.config.get<string>('pythonPath') || '';
    }

    get apiBaseUrl(): string {
        return this.config.get<string>('apiBaseUrl') || '';
    }

    async updateConfig(key: string, value: any): Promise<void> {
        await this.config.update(key, value, vscode.ConfigurationTarget.Global);
    }

    validateConfig(): { valid: boolean; errors: string[] } {
        const errors: string[] = [];

        // Only require API key if not using local models
        if (!this.openaiApiKey && !this.apiBaseUrl) {
            errors.push('OpenAI API key is not configured. Please set it in extension settings or configure a local model API URL.');
        }

        if (!this.model) {
            errors.push('AI model is not configured.');
        }

        if (!this.language) {
            errors.push('Documentation language is not configured.');
        }

        return {
            valid: errors.length === 0,
            errors
        };
    }

    async promptForApiKey(): Promise<string | undefined> {
        const apiKey = await vscode.window.showInputBox({
            title: 'OpenAI API Key Required',
            prompt: 'Please enter your OpenAI API key',
            password: true,
            ignoreFocusOut: true,
            validateInput: (value: string) => {
                if (!value || value.trim().length === 0) {
                    return 'API key cannot be empty';
                }
                if (!value.startsWith('sk-')) {
                    return 'Please enter a valid OpenAI API key (starts with sk-)';
                }
                return null;
            }
        });

        if (apiKey) {
            await this.updateConfig('openaiApiKey', apiKey);
        }

        return apiKey;
    }
}
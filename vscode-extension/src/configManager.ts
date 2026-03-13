import * as vscode from 'vscode';

export interface ExtensionConfig {
    provider: string;
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

get provider(): string {
        return this.config.get<string>('provider') || 'openai';
    }

    get apiBaseUrl(): string {
        return this.config.get<string>('apiBaseUrl') || '';
    }

async updateConfig(key: string, value: any): Promise<void> {
        await this.config.update(key, value, vscode.ConfigurationTarget.Global);
        
        // Auto-sync defaults if provider changed
        if (key === 'provider') {
            await this.syncProviderDefaults();
        }
    }

    public async syncProviderDefaults(): Promise<void> {
        const provider = this.provider;
        let model = this.model;
        let apiBaseUrl = this.apiBaseUrl;

        switch (provider) {
            case 'openai':
                model = model || 'gpt-4o-mini';
                apiBaseUrl = '';
                break;
            case 'ollama':
                model = model || 'llama3.1';
                apiBaseUrl = apiBaseUrl || 'http://localhost:11434/v1';
                break;
            case 'lmstudio':
                model = model || 'llama3.1';
                apiBaseUrl = apiBaseUrl || 'http://localhost:1234/v1';
                break;
            case 'claude':
                model = model || 'claude-3-5-sonnet-20240620';
                apiBaseUrl = '';
                break;
        }

        await this.config.update('model', model, vscode.ConfigurationTarget.Global);
        await this.config.update('apiBaseUrl', apiBaseUrl, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage(`Provider changed to ${provider}. Model/API updated to defaults.`);
    }

validateConfig(): { valid: boolean; errors: string[] } {
        const errors: string[] = [];

        const needsApiKey = this.provider === 'openai' || this.provider === 'claude';
        if (needsApiKey && !this.openaiApiKey) {
            errors.push(`API key required for ${this.provider.toUpperCase()}. Please set it in extension settings.`);
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
        const providerName = this.provider.toUpperCase();
        const promptText = this.provider === 'claude' ? 'Please enter your Anthropic API key (starts with sk-ant-)' : 'Please enter your OpenAI API key (starts with sk-)';
        const validatePrefix = this.provider === 'claude' ? 'sk-ant-' : 'sk-';

        const apiKey = await vscode.window.showInputBox({
            title: `${providerName} API Key Required`,
            prompt: promptText,
            password: true,
            ignoreFocusOut: true,
            validateInput: (value: string) => {
                if (!value || value.trim().length === 0) {
                    return 'API key cannot be empty';
                }
                if (!value.startsWith(validatePrefix)) {
                    return `Please enter a valid ${providerName} API key (starts with ${validatePrefix})`;
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

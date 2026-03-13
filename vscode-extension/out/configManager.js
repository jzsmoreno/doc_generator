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
exports.ConfigManager = void 0;
const vscode = __importStar(require("vscode"));
class ConfigManager {
    constructor() {
        this.config = vscode.workspace.getConfiguration('notebookDocGenerator');
    }
    get openaiApiKey() {
        return this.config.get('openaiApiKey') || '';
    }
    get model() {
        return this.config.get('model') || 'gpt-4';
    }
    get language() {
        return this.config.get('language') || 'english';
    }
    get generatePdf() {
        return this.config.get('generatePdf') !== false;
    }
    get pythonPath() {
        return this.config.get('pythonPath') || '';
    }
    get provider() {
        return this.config.get('provider') || 'openai';
    }
    get apiBaseUrl() {
        return this.config.get('apiBaseUrl') || '';
    }
    async updateConfig(key, value) {
        await this.config.update(key, value, vscode.ConfigurationTarget.Global);
        // Auto-sync defaults if provider changed
        if (key === 'provider') {
            await this.syncProviderDefaults();
        }
    }
    async syncProviderDefaults() {
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
    validateConfig() {
        const errors = [];
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
    async promptForApiKey() {
        const providerName = this.provider.toUpperCase();
        const promptText = this.provider === 'claude' ? 'Please enter your Anthropic API key (starts with sk-ant-)' : 'Please enter your OpenAI API key (starts with sk-)';
        const validatePrefix = this.provider === 'claude' ? 'sk-ant-' : 'sk-';
        const apiKey = await vscode.window.showInputBox({
            title: `${providerName} API Key Required`,
            prompt: promptText,
            password: true,
            ignoreFocusOut: true,
            validateInput: (value) => {
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
exports.ConfigManager = ConfigManager;
//# sourceMappingURL=configManager.js.map
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
    get apiBaseUrl() {
        return this.config.get('apiBaseUrl') || '';
    }
    async updateConfig(key, value) {
        await this.config.update(key, value, vscode.ConfigurationTarget.Global);
    }
    validateConfig() {
        const errors = [];
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
    async promptForApiKey() {
        const apiKey = await vscode.window.showInputBox({
            title: 'OpenAI API Key Required',
            prompt: 'Please enter your OpenAI API key',
            password: true,
            ignoreFocusOut: true,
            validateInput: (value) => {
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
exports.ConfigManager = ConfigManager;
//# sourceMappingURL=configManager.js.map
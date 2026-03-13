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
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
const outputChannel_1 = require("./outputChannel");
const commands_1 = require("./commands");
const pythonEnvironment_1 = require("./pythonEnvironment");
const configManager_1 = require("./configManager");
let outputChannel;
function activate(context) {
    console.log('Notebook Documentation Generator extension is now active!');
    // Initialize output channel
    outputChannel = new outputChannel_1.OutputChannel();
    context.subscriptions.push(outputChannel);
    // Check Python environment
    (0, pythonEnvironment_1.checkPythonEnvironment)(outputChannel).then(isValid => {
        if (!isValid) {
            vscode.window.showWarningMessage('Python environment not properly configured. Please check the output panel for details.', 'Show Output').then(selection => {
                if (selection === 'Show Output') {
                    outputChannel.show();
                }
            });
        }
    });
    // Register commands - pass extension URI for self-contained core module
    (0, commands_1.registerCommands)(context, outputChannel, context.extensionUri);
    // Listen for config changes to sync provider defaults
    vscode.workspace.onDidChangeConfiguration(async (e) => {
        if (e.affectsConfiguration('notebookDocGenerator.provider')) {
            try {
                const configManager = new configManager_1.ConfigManager();
                await configManager.syncProviderDefaults();
            }
            catch (error) {
                console.error('Provider sync failed:', error);
            }
        }
    }, null, context.subscriptions);
    // Show activation message
    vscode.window.showInformationMessage('Notebook Documentation Generator extension activated!');
}
exports.activate = activate;
function deactivate() {
    console.log('Notebook Documentation Generator extension is now deactivated!');
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map
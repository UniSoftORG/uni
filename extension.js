const vscode = require('vscode');
const { exec } = require('child_process');

function activate(context) {
  let disposable = vscode.commands.registerCommand('uni.parseFile', function () {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showInformationMessage('No file is open');
      return;
    }

    const filePath = editor.document.fileName;
    if (filePath.endsWith('.uni')) {
      exec(`python C:\\Users\\radei\\Desktop\\unisoft\\uni\\compiler.py "${filePath}"`, (err, stdout, stderr) => {
        if (err) {
          vscode.window.showErrorMessage(`Error: ${stderr}`);
        } else {
          vscode.window.showInformationMessage(`File parsed successfully ${filePath}`);
        }
      });
    } else {
      vscode.window.showErrorMessage('The open file is not a .uni file');
    }
  });

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};

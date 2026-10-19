/**
 * VS Code Tutorial Screen Recording Generator
 * Generates high-fidelity 1920x1080 animated screen recording video clips for Day 1 tutorial.
 */
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const FFMPEG_PATH = path.resolve(__dirname, '../../broll/node_modules/ffmpeg-static/ffmpeg.exe');
const OUT_DIR = path.resolve(__dirname, 'renders');

fs.mkdirSync(OUT_DIR, { recursive: true });

function getVSCodeHTML(state) {
  // state: {
  //   activeFile: string,
  //   files: string[],
  //   editorLines: { num: number, text: string, error?: boolean }[],
  //   terminalLines: { prompt?: string, text: string, color?: string }[],
  //   browserOverlay?: { type: 'python_download' | 'python_install' | 'vscode_download' | 'extension' },
  //   cursorPos?: { line: number, col: number }
  // }
  
  const filesList = (state.files || ['hello.py', 'expression_only.py', 'printed_expression.py', 'broken_example.py', 'types_preview.py'])
    .map(f => {
      const active = f === state.activeFile ? 'active' : '';
      return `<div class="file-item ${active}"><span class="py-icon">PY</span> <span class="file-name">${f}</span></div>`;
    }).join('');

  const editorContent = (state.editorLines || [])
    .map(l => {
      const errClass = l.error ? 'syntax-error' : '';
      return `<div class="code-line ${errClass}"><span class="line-num">${l.num}</span><span class="line-code">${l.text}</span></div>`;
    }).join('');

  const terminalContent = (state.terminalLines || [])
    .map(l => {
      const color = l.color ? `style="color:${l.color};"` : '';
      if (l.prompt) {
        return `<div class="term-line"><span class="term-prompt">${l.prompt}</span><span class="term-cmd" ${color}>${l.text}</span></div>`;
      }
      return `<div class="term-line" ${color}>${l.text}</div>`;
    }).join('');

  let overlayHTML = '';
  if (state.browserOverlay) {
    if (state.browserOverlay.type === 'python_download') {
      overlayHTML = `
      <div class="browser-modal">
        <div class="browser-bar">
          <div class="browser-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
          <div class="browser-url">🔒 https://www.python.org/downloads/</div>
        </div>
        <div class="browser-body">
          <div class="py-header"><span class="py-logo">🐍 python™</span> <span class="py-menu">About · Downloads · Documentation · Community</span></div>
          <div class="py-hero">
            <h2>Download the latest version of Python</h2>
            <p>Download Python 3.13 for Windows</p>
            <div class="download-btn pulse">Download Python 3.13</div>
            <div class="os-note">Note that Python 3.13 cannot be used on Windows 7 or earlier.</div>
          </div>
        </div>
      </div>`;
    } else if (state.browserOverlay.type === 'python_install') {
      overlayHTML = `
      <div class="installer-modal">
        <div class="installer-header">
          <span>Python 3.13 (64-bit) Setup</span>
          <span class="close-x">✕</span>
        </div>
        <div class="installer-body">
          <div class="inst-icon">🐍</div>
          <div class="inst-content">
            <h3>Install Python 3.13 (64-bit)</h3>
            <p>Select Install Now to install Python with default settings.</p>
            <div class="install-option selected">
              <div class="opt-title">⚡ Install Now</div>
              <div class="opt-desc">C:\\Users\\lms-work\\AppData\\Local\\Programs\\Python\\Python313</div>
            </div>
            <div class="path-checkbox-wrapper highlight-box">
              <label><input type="checkbox" checked /> <strong>Add python.exe to PATH</strong></label>
              <div class="callout-arrow">⬅ MUST CHECK THIS BOX!</div>
            </div>
          </div>
        </div>
        <div class="installer-footer">
          <span class="btn-cancel">Cancel</span>
        </div>
      </div>`;
    } else if (state.browserOverlay.type === 'vscode_download') {
      overlayHTML = `
      <div class="browser-modal">
        <div class="browser-bar">
          <div class="browser-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
          <div class="browser-url">🔒 https://code.visualstudio.com/Download</div>
        </div>
        <div class="browser-body vscode-web">
          <div class="vsc-header"><span class="vsc-logo">🔷 Visual Studio Code</span> <span class="py-menu">Docs · Updates · Blog · API · Extensions</span></div>
          <div class="vsc-hero">
            <h2>Download Visual Studio Code</h2>
            <p>Free, built on open source. Runs everywhere.</p>
            <div class="dl-grid">
              <div class="dl-card pulse">
                <div class="dl-os">Windows</div>
                <div class="dl-sub">Windows 10, 11</div>
                <div class="vsc-btn">User Installer (64 bit)</div>
              </div>
            </div>
          </div>
        </div>
      </div>`;
    } else if (state.browserOverlay.type === 'extension') {
      overlayHTML = `
      <div class="ext-modal">
        <div class="ext-header">
          <div class="ext-icon">🐍</div>
          <div class="ext-info">
            <div class="ext-name">Python <span class="verified-badge">✔ Microsoft</span></div>
            <div class="ext-publisher">ms-python.python</div>
            <div class="ext-stats">120M+ installs · ⭐⭐⭐⭐⭐</div>
            <div class="ext-btn installed">✔ Installed</div>
          </div>
        </div>
        <div class="ext-desc">
          IntelliSense (Pylance), Linting, Debugging (Python Debugger), code formatting, refactoring, unit tests, and more.
        </div>
      </div>`;
    }
  }

  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 1920px;
  height: 1080px;
  background: #181818;
  color: #cccccc;
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow: hidden;
  user-select: none;
  display: flex;
  flex-direction: column;
}

/* Title Bar */
.title-bar {
  height: 38px;
  background: #1f1f1f;
  border-bottom: 1px solid #2b2b2b;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  font-size: 13px;
}
.title-left { display: flex; align-items: center; gap: 14px; }
.vsc-mark { color: #007acc; font-weight: bold; font-size: 16px; }
.menu-items { display: flex; gap: 14px; color: #999; }
.title-center { color: #cccccc; font-size: 13px; font-weight: 500; }
.window-controls { display: flex; gap: 14px; color: #888; font-size: 12px; }

/* Main Workspace */
.workspace {
  flex: 1;
  display: flex;
  position: relative;
}

/* Activity Bar */
.activity-bar {
  width: 50px;
  background: #181818;
  border-right: 1px solid #2b2b2b;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 10px;
  gap: 22px;
}
.act-icon { font-size: 20px; color: #858585; cursor: pointer; }
.act-icon.active { color: #ffffff; border-left: 2px solid #007acc; padding-left: 2px; }

/* Side Bar */
.sidebar {
  width: 260px;
  background: #1f1f1f;
  border-right: 1px solid #2b2b2b;
  display: flex;
  flex-direction: column;
}
.sidebar-title {
  padding: 12px 16px 8px;
  font-size: 11px;
  font-weight: bold;
  letter-spacing: 1px;
  color: #bbbbbb;
  text-transform: uppercase;
}
.file-tree { padding: 4px 0; }
.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  font-size: 13px;
  color: #cccccc;
}
.file-item.active { background: #2a2d2e; color: #ffffff; }
.py-icon {
  font-size: 10px;
  font-weight: bold;
  background: #3776ab;
  color: #ffd43b;
  padding: 2px 4px;
  border-radius: 3px;
}

/* Editor & Terminal Area */
.editor-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #1e1e1e;
}

/* Tab Bar */
.tabs-bar {
  height: 38px;
  background: #181818;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #2b2b2b;
}
.tab {
  height: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  background: #1e1e1e;
  border-right: 1px solid #2b2b2b;
  border-top: 2px solid #007acc;
  font-size: 13px;
  color: #ffffff;
}
.tab-close { font-size: 12px; color: #888; }

/* Code Editor */
.editor-body {
  flex: 1;
  padding: 16px 0;
  font-family: 'Cascadia Code', Consolas, 'Courier New', monospace;
  font-size: 16px;
  line-height: 26px;
  overflow: hidden;
}
.code-line {
  display: flex;
  padding: 0 16px;
}
.line-num {
  width: 45px;
  color: #858585;
  text-align: right;
  padding-right: 18px;
  user-select: none;
}
.line-code { color: #d4d4d4; white-space: pre; }
.syntax-error { text-decoration: underline wavy #f14c4c; }

/* Syntax Highlights */
.kw { color: #c586c0; font-weight: bold; }
.fn { color: #dcdcaa; }
.str { color: #ce9178; }
.num { color: #b5cea8; }
.comment { color: #6a9955; font-style: italic; }
.var { color: #9cdcfe; }

/* Integrated Terminal */
.terminal-panel {
  height: 420px;
  background: #181818;
  border-top: 1px solid #2b2b2b;
  display: flex;
  flex-direction: column;
}
.term-header {
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid #242424;
  font-size: 12px;
}
.term-tabs { display: flex; gap: 16px; font-weight: 500; }
.term-tab.active { color: #ffffff; border-bottom: 2px solid #007acc; padding-bottom: 7px; }
.term-tab { color: #888888; }
.term-right { display: flex; gap: 12px; color: #888; }
.term-body {
  flex: 1;
  padding: 12px 16px;
  font-family: 'Cascadia Code', Consolas, 'Courier New', monospace;
  font-size: 15px;
  line-height: 24px;
  color: #cccccc;
  overflow: hidden;
}
.term-line { white-space: pre-wrap; margin-bottom: 2px; }
.term-prompt { color: #23d18b; font-weight: bold; }
.term-cmd { color: #ffffff; }

/* Status Bar */
.status-bar {
  height: 24px;
  background: #007acc;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
  font-size: 12px;
}
.status-left, .status-right { display: flex; gap: 14px; align-items: center; }

/* Modals & Overlays */
.browser-modal {
  position: absolute;
  top: 55px;
  left: 280px;
  width: 1360px;
  height: 800px;
  background: #ffffff;
  color: #222222;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.7);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #555;
  z-index: 50;
  animation: popIn 0.3s ease;
}
.browser-bar {
  height: 42px;
  background: #f1f3f4;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 16px;
  border-bottom: 1px solid #dadce0;
}
.browser-dots { display: flex; gap: 8px; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot.red { background: #ed6a5e; }
.dot.yellow { background: #f5bf4f; }
.dot.green { background: #62c554; }
.browser-url {
  flex: 1;
  background: #ffffff;
  height: 28px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  padding: 0 14px;
  font-size: 13px;
  color: #3c4043;
  border: 1px solid #dadce0;
}
.browser-body {
  flex: 1;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
}
.py-header {
  height: 60px;
  background: #1f374c;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  font-size: 14px;
}
.py-logo { font-size: 20px; font-weight: bold; color: #ffd43b; }
.py-hero {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  text-align: center;
  padding: 40px;
}
.py-hero h2 { font-size: 32px; color: #2b5b84; }
.py-hero p { font-size: 18px; color: #555555; }
.download-btn {
  background: #ffc107;
  color: #212529;
  padding: 16px 36px;
  font-size: 20px;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.os-note { font-size: 13px; color: #777777; }

/* Installer Dialog */
.installer-modal {
  position: absolute;
  top: 180px;
  left: 600px;
  width: 720px;
  height: 480px;
  background: #f0f0f0;
  color: #111111;
  border-radius: 6px;
  box-shadow: 0 25px 70px rgba(0,0,0,0.8);
  display: flex;
  flex-direction: column;
  border: 1px solid #777777;
  z-index: 100;
  animation: popIn 0.3s ease;
}
.installer-header {
  height: 36px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  font-size: 13px;
  font-weight: 500;
  border-bottom: 1px solid #e0e0e0;
}
.installer-body {
  flex: 1;
  padding: 24px 32px;
  display: flex;
  gap: 24px;
}
.inst-icon { font-size: 48px; }
.inst-content { flex: 1; display: flex; flex-direction: column; gap: 14px; }
.inst-content h3 { font-size: 20px; color: #1e395b; }
.install-option {
  background: #ffffff;
  border: 1px solid #0078d7;
  border-radius: 4px;
  padding: 12px 16px;
  cursor: pointer;
}
.opt-title { font-size: 15px; font-weight: bold; color: #0078d7; }
.opt-desc { font-size: 11px; color: #666; margin-top: 4px; }
.highlight-box {
  background: #fff8e1;
  border: 2px solid #ff9800;
  border-radius: 6px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 0 15px rgba(255, 152, 0, 0.4);
}
.callout-arrow {
  color: #d84315;
  font-weight: bold;
  font-size: 13px;
  animation: bounceRight 1s infinite alternate;
}
.installer-footer {
  height: 50px;
  background: #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
  border-top: 1px solid #d0d0d0;
}
.btn-cancel {
  background: #ffffff;
  border: 1px solid #adadad;
  padding: 6px 18px;
  font-size: 13px;
  border-radius: 2px;
}

/* VS Code Download */
.vscode-web { background: #001122; color: #ffffff; }
.vsc-header { height: 60px; background: #000b18; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
.vsc-logo { font-size: 20px; font-weight: bold; color: #007acc; }
.vsc-hero { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; }
.dl-card { background: #002244; padding: 24px 40px; border-radius: 8px; text-align: center; border: 1px solid #0055aa; }
.dl-os { font-size: 24px; font-weight: bold; color: #ffffff; }
.dl-sub { font-size: 13px; color: #88bbff; margin: 6px 0 14px; }
.vsc-btn { background: #007acc; color: white; padding: 12px 24px; font-weight: bold; border-radius: 4px; }

/* Extensions Modal */
.ext-modal {
  position: absolute;
  top: 150px;
  left: 320px;
  width: 680px;
  background: #252526;
  border: 1px solid #454545;
  border-radius: 6px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.6);
  padding: 20px;
  z-index: 50;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.ext-header { display: flex; gap: 16px; align-items: center; }
.ext-icon { font-size: 40px; }
.ext-info { flex: 1; display: flex; flex-direction: column; gap: 4px; }
.ext-name { font-size: 18px; font-weight: bold; color: #ffffff; }
.verified-badge { color: #3794ff; font-size: 13px; font-weight: normal; margin-left: 6px; }
.ext-publisher { font-size: 12px; color: #888888; }
.ext-stats { font-size: 12px; color: #cccccc; }
.ext-btn.installed { background: #388e3c; color: white; padding: 6px 14px; border-radius: 3px; font-size: 12px; font-weight: bold; align-self: flex-start; margin-top: 6px; }
.ext-desc { font-size: 13px; color: #cccccc; line-height: 20px; }

@keyframes popIn {
  from { opacity: 0; transform: scale(0.96); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes bounceRight {
  from { transform: translateX(0); }
  to { transform: translateX(8px); }
}
</style>
</head>
<body>

<!-- Title Bar -->
<div class="title-bar">
  <div class="title-left">
    <span class="vsc-mark">🔷</span>
    <div class="menu-items">
      <span>File</span><span>Edit</span><span>Selection</span><span>View</span><span>Go</span><span>Run</span><span>Terminal</span><span>Help</span>
    </div>
  </div>
  <div class="title-center">${state.activeFile ? state.activeFile + ' - ' : ''}python-30-days - Visual Studio Code</div>
  <div class="window-controls">
    <span>─</span><span>◻</span><span>✕</span>
  </div>
</div>

<!-- Main Workspace -->
<div class="workspace">
  <!-- Activity Bar -->
  <div class="activity-bar">
    <div class="act-icon ${state.browserOverlay?.type === 'extension' ? '' : 'active'}">📁</div>
    <div class="act-icon">🔍</div>
    <div class="act-icon">🔀</div>
    <div class="act-icon">🐞</div>
    <div class="act-icon ${state.browserOverlay?.type === 'extension' ? 'active' : ''}">🧩</div>
  </div>

  <!-- Sidebar -->
  <div class="sidebar">
    <div class="sidebar-title">Explorer: python-30-days</div>
    <div class="file-tree">
      ${filesList}
    </div>
  </div>

  <!-- Editor Container -->
  <div class="editor-container">
    <div class="tabs-bar">
      <div class="tab">
        <span class="py-icon">PY</span>
        <span>${state.activeFile || 'hello.py'}</span>
        <span class="tab-close">✕</span>
      </div>
    </div>
    <div class="editor-body">
      ${editorContent}
    </div>

    <!-- Terminal Panel -->
    <div class="terminal-panel">
      <div class="term-header">
        <div class="term-tabs">
          <span>PROBLEMS</span><span>OUTPUT</span><span>DEBUG CONSOLE</span>
          <span class="term-tab active">TERMINAL</span>
        </div>
        <div class="term-right">
          <span>1: pwsh</span><span>+</span><span>^</span><span>✕</span>
        </div>
      </div>
      <div class="term-body">
        ${terminalContent}
      </div>
    </div>
  </div>

  <!-- Browser or Installer Overlay -->
  ${overlayHTML}
</div>

<!-- Status Bar -->
<div class="status-bar">
  <div class="status-left">
    <span>🔀 main*</span>
    <span>⚡ 0 ⚠ 0</span>
  </div>
  <div class="status-right">
    <span>Spaces: 4</span>
    <span>UTF-8</span>
    <span>Python 3.13.15 64-bit</span>
  </div>
</div>

</body>
</html>`;
}

module.exports = { getVSCodeHTML, CHROME_PATH, FFMPEG_PATH, OUT_DIR };

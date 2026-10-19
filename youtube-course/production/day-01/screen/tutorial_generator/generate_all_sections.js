/**
 * Generate All 11 Authentic VS Code Tutorial Screen Recording Video Clips
 * Synchronized with the 11 audio narration sections (total 359.68s).
 */
const fs = require('fs');
const path = require('path');
const puppeteer = require('../../broll/node_modules/puppeteer-core');
const { execSync } = require('child_process');
const { getVSCodeHTML, CHROME_PATH, FFMPEG_PATH } = require('./vscode_template');

const MANIFEST_PATH = path.resolve(__dirname, '../../voice/v2/manifest.json');
const CAPTURES_DIR = path.resolve(__dirname, '../v2/captures');
const FRAMES_DIR = path.resolve(__dirname, 'temp_frames');

fs.mkdirSync(CAPTURES_DIR, { recursive: true });
fs.mkdirSync(FRAMES_DIR, { recursive: true });

// Section storyboard definitions matching the audio script
const STORYBOARDS = {
  '01': [
    // 12.49s total
    {
      dur: 3.5,
      state: {
        activeFile: 'expression_only.py',
        editorLines: [
          { num: 1, text: '<span class="num">10</span> + <span class="num">20</span>' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python' },
          { text: 'Python 3.13.15 (main) [MSC v.1944 64 bit] on win32' },
          { prompt: '>>> ', text: '10 + 20' },
          { text: '<span class="num">30</span>', color: '#b5cea8' },
          { prompt: '>>> ', text: 'exit()' },
          { prompt: 'PS C:\\python-30-days> ', text: 'python expression_only.py' }
        ]
      }
    },
    {
      dur: 4.5,
      state: {
        activeFile: 'expression_only.py',
        editorLines: [
          { num: 1, text: '<span class="num">10</span> + <span class="num">20</span>' }
        ],
        terminalLines: [
          { prompt: '>>> ', text: '10 + 20' },
          { text: '<span class="num">30</span>', color: '#b5cea8' },
          { prompt: '>>> ', text: 'exit()' },
          { prompt: 'PS C:\\python-30-days> ', text: 'python expression_only.py' },
          { text: '<span style="color:#888;">(nothing printed — returns to prompt)</span>' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 4.49,
      state: {
        activeFile: 'printed_expression.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python expression_only.py' },
          { text: '<span style="color:#888;">(nothing printed)</span>' },
          { prompt: 'PS C:\\python-30-days> ', text: 'python printed_expression.py' },
          { text: '<span class="num">30</span>', color: '#23d18b' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '02': [
    // 13.56s total
    {
      dur: 6.5,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>)' },
          { num: 2, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' }
        ]
      }
    },
    {
      dur: 7.06,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>)' },
          { num: 2, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: '<span class="str">Hello, Python!</span>', color: '#4ec9b0' },
          { text: '<span class="num">30</span>', color: '#b5cea8' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '03': [
    // 31.08s total
    {
      dur: 10.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># Python: General Purpose Programming</span>' },
          { num: 2, text: '<span class="fn">print</span>(<span class="str">"1. Automation: renaming files, scripting"</span>)' },
          { num: 3, text: '<span class="fn">print</span>(<span class="str">"2. Data Analysis: pandas, tables, charts"</span>)' },
          { num: 4, text: '<span class="fn">print</span>(<span class="str">"3. Web & AI: FastAPI, PyTorch, LLMs"</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: 'Hello, Python!' },
          { text: '30' }
        ]
      }
    },
    {
      dur: 11.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># Our Day 1 testable goal:</span>' },
          { num: 2, text: '<span class="fn">print</span>(<span class="str">"Can you run a file, change it,"</span>)' },
          { num: 3, text: '<span class="fn">print</span>(<span class="str">"and explain what changed?"</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: 'Can you run a file, change it,' },
          { text: 'and explain what changed?' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 10.08,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>)' },
          { num: 2, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: 'Hello, Python!' },
          { text: '30' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '04': [
    // 39.59s total - Python Installation & Version Walkthrough
    {
      dur: 8.0,
      state: {
        activeFile: 'terminal',
        editorLines: [
          { num: 1, text: '<span class="comment"># Check Python Installation</span>' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python --version' },
          { text: 'Python 3.13.15', color: '#23d18b' },
          { prompt: 'PS C:\\python-30-days> ', text: 'py --version' },
          { text: 'Python 3.13.15', color: '#23d18b' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 15.0,
      state: {
        activeFile: 'terminal',
        editorLines: [],
        terminalLines: [],
        browserOverlay: { type: 'python_download' }
      }
    },
    {
      dur: 12.0,
      state: {
        activeFile: 'terminal',
        editorLines: [],
        terminalLines: [],
        browserOverlay: { type: 'python_install' }
      }
    },
    {
      dur: 4.59,
      state: {
        activeFile: 'terminal',
        editorLines: [
          { num: 1, text: '<span class="comment"># Python installed and verified successfully</span>' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python --version' },
          { text: 'Python 3.13.15', color: '#23d18b' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '05': [
    // 33.24s total - Know Which Prompt
    {
      dur: 8.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># Notice the difference between Terminal and Python Shell:</span>' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python' },
          { text: 'Python 3.13.15 (main, Oct 2026, 64 bit) [MSC v.1944] on win32' },
          { text: 'Type "help", "copyright", "credits" or "license" for more information.' },
          { prompt: '>>> ', text: '<span style="background:#007acc;color:white;padding:1px 4px;">&gt;&gt;&gt; (You are inside Python interactive shell)</span>' }
        ]
      }
    },
    {
      dur: 12.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># NEVER run terminal commands inside the >>> prompt!</span>' }
        ],
        terminalLines: [
          { text: 'Python 3.13.15 on win32' },
          { prompt: '>>> ', text: 'python hello.py' },
          { text: '  File "&lt;stdin&gt;", line 1\n    python hello.py\n           ^^^^^\nSyntaxError: invalid syntax', color: '#f14c4c' },
          { prompt: '>>> ', text: '' }
        ]
      }
    },
    {
      dur: 13.24,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># Leave the shell with exit(), then run your file:</span>' }
        ],
        terminalLines: [
          { prompt: '>>> ', text: 'exit()' },
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: 'Hello, Python!' },
          { text: '30' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '06': [
    // 30.40s total - First Expressions
    {
      dur: 7.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [],
        terminalLines: [
          { prompt: '>>> ', text: '10 + 20' },
          { text: '<span class="num">30</span>', color: '#b5cea8' },
          { prompt: '>>> ', text: '' }
        ]
      }
    },
    {
      dur: 7.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [],
        terminalLines: [
          { prompt: '>>> ', text: '10 + 20' },
          { text: '<span class="num">30</span>', color: '#b5cea8' },
          { prompt: '>>> ', text: '10 - 3' },
          { text: '<span class="num">7</span>', color: '#b5cea8' },
          { prompt: '>>> ', text: '4 * 5' },
          { text: '<span class="num">20</span>', color: '#b5cea8' }
        ]
      }
    },
    {
      dur: 8.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [],
        terminalLines: [
          { prompt: '>>> ', text: '4 * 5' },
          { text: '<span class="num">20</span>' },
          { prompt: '>>> ', text: 'print("Hello, Python!")' },
          { text: '<span class="str">Hello, Python!</span>', color: '#4ec9b0' }
        ]
      }
    },
    {
      dur: 8.40,
      state: {
        activeFile: 'hello.py',
        editorLines: [],
        terminalLines: [
          { prompt: '>>> ', text: 'print("Hello, Python!")' },
          { text: 'Hello, Python!' },
          { prompt: '>>> ', text: 'print("Welcome to Day 1!")' },
          { text: '<span class="str">Welcome to Day 1!</span>', color: '#4ec9b0' },
          { prompt: '>>> ', text: '' }
        ]
      }
    }
  ],

  '07': [
    // 34.19s total - Break One Line & Recover
    {
      dur: 10.0,
      state: {
        activeFile: 'broken_example.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>', error: true }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python broken_example.py' }
        ]
      }
    },
    {
      dur: 12.0,
      state: {
        activeFile: 'broken_example.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>', error: true }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python broken_example.py' },
          { text: '  File "broken_example.py", line 1\n    print("Hello, Python!"\n         ^\nSyntaxError: \'(\' was never closed', color: '#f14c4c' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 12.19,
      state: {
        activeFile: 'broken_example.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python broken_example.py' },
          { text: 'SyntaxError: \'(\' was never closed', color: '#f14c4c' },
          { text: '<span style="color:#23d18b;"># Added missing closing parenthesis ")" and saved file</span>' },
          { prompt: 'PS C:\\python-30-days> ', text: 'python broken_example.py' },
          { text: '<span class="str">Hello, Python!</span>', color: '#23d18b' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '08': [
    // 76.06s total - VS Code Setup & Save/Run File
    {
      dur: 15.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [],
        terminalLines: [],
        browserOverlay: { type: 'vscode_download' }
      }
    },
    {
      dur: 16.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [],
        terminalLines: [],
        browserOverlay: { type: 'extension' }
      }
    },
    {
      dur: 15.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>)' },
          { num: 2, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: 'Hello, Python!' },
          { text: '30' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 15.0,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, World!"</span>)' },
          { num: 2, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: 'Hello, World!' },
          { text: '30' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 15.06,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>)' },
          { num: 2, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'Get-Location' },
          { text: 'Path: C:\\Users\\lms-work\\python-30-days' },
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: 'Hello, Python!' },
          { text: '30' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '09': [
    // 34.59s total - Resolve Puzzle
    {
      dur: 11.0,
      state: {
        activeFile: 'expression_only.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># In a script file, writing an expression alone has no printed output:</span>' },
          { num: 2, text: '<span class="num">10</span> + <span class="num">20</span>' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python expression_only.py' },
          { text: '<span style="color:#888;">(blank line — no output)</span>' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 11.0,
      state: {
        activeFile: 'printed_expression.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># Use print() when your script needs to show the result:</span>' },
          { num: 2, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python printed_expression.py' },
          { text: '<span class="num">30</span>', color: '#23d18b' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 12.59,
      state: {
        activeFile: 'hello.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># Summary: Shell = fast experiments | File = reproducible code</span>' },
          { num: 2, text: '<span class="fn">print</span>(<span class="str">"Hello, Python!"</span>)' },
          { num: 3, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python hello.py' },
          { text: 'Hello, Python!' },
          { text: '30' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '10': [
    // 36.63s total - Types Preview & Comments
    {
      dur: 12.0,
      state: {
        activeFile: 'types_preview.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># Inspect the kinds of values Python is working with.</span>' },
          { num: 2, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="num">30</span>))' },
          { num: 3, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="num">3.5</span>))' },
          { num: 4, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="str">"Python"</span>))' },
          { num: 5, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="kw">True</span>))' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python types_preview.py' }
        ]
      }
    },
    {
      dur: 14.0,
      state: {
        activeFile: 'types_preview.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># Notice: integer vs float vs string vs boolean:</span>' },
          { num: 2, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="num">30</span>))       <span class="comment"># &lt;class \'int\'&gt;</span>' },
          { num: 3, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="num">3.5</span>))      <span class="comment"># &lt;class \'float\'&gt;</span>' },
          { num: 4, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="str">"Python"</span>)) <span class="comment"># &lt;class \'str\'&gt;</span>' },
          { num: 5, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="kw">True</span>))     <span class="comment"># &lt;class \'bool\'&gt;</span>' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python types_preview.py' },
          { text: "&lt;class 'int'&gt;", color: '#4ec9b0' },
          { text: "&lt;class 'float'&gt;", color: '#4ec9b0' },
          { text: "&lt;class 'str'&gt;", color: '#4ec9b0' },
          { text: "&lt;class 'bool'&gt;", color: '#4ec9b0' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 10.63,
      state: {
        activeFile: 'types_preview.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># The line starting with # is a comment (does not execute)</span>' },
          { num: 2, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="num">30</span>))       <span class="comment"># int</span>' },
          { num: 3, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="str">"30"</span>))     <span class="comment"># str (text containing digits)</span>' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python -c \'print(type(30), type("30"))\'' },
          { text: "&lt;class 'int'&gt; &lt;class 'str'&gt;", color: '#4ec9b0' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ],

  '11': [
    // 17.86s total - Challenge
    {
      dur: 8.0,
      state: {
        activeFile: 'day1_challenge.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># DAY 1 PRACTICE CHALLENGE:</span>' },
          { num: 2, text: '<span class="comment"># 1. Print your name</span>' },
          { num: 3, text: '<span class="comment"># 2. Print result of 10 + 20</span>' },
          { num: 4, text: '<span class="comment"># 3. Print types of 30, 3.5, and "Python"</span>' },
          { num: 5, text: '' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'New-Item day1_challenge.py' },
          { text: '    Directory: C:\\Users\\lms-work\\python-30-days\nMode      Name\n-a---     day1_challenge.py' },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    },
    {
      dur: 9.86,
      state: {
        activeFile: 'day1_challenge.py',
        editorLines: [
          { num: 1, text: '<span class="comment"># DAY 1 PRACTICE CHALLENGE:</span>' },
          { num: 2, text: '<span class="fn">print</span>(<span class="str">"My Name is Learner"</span>)' },
          { num: 3, text: '<span class="fn">print</span>(<span class="num">10</span> + <span class="num">20</span>)' },
          { num: 4, text: '<span class="fn">print</span>(<span class="fn">type</span>(<span class="num">30</span>), <span class="fn">type</span>(<span class="num">3.5</span>), <span class="fn">type</span>(<span class="str">"Python"</span>))' }
        ],
        terminalLines: [
          { prompt: 'PS C:\\python-30-days> ', text: 'python day1_challenge.py' },
          { text: 'My Name is Learner' },
          { text: '30' },
          { text: "&lt;class 'int'&gt; &lt;class 'float'&gt; &lt;class 'str'&gt;" },
          { prompt: 'PS C:\\python-30-days> ', text: '' }
        ]
      }
    }
  ]
};

async function main() {
  console.log('Launching headless Chrome...');
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf-8'));
  console.log(`Loaded manifest: ${manifest.sections.length} sections.`);

  for (const sec of manifest.sections) {
    const secId = sec.id;
    const targetDur = sec.audio.duration_seconds;
    const steps = STORYBOARDS[secId];
    if (!steps) {
      console.warn(`No storyboard for section ${secId}, skipping.`);
      continue;
    }

    console.log(`\n[${secId}/11] Rendering ${sec.title} (${targetDur}s, ${steps.length} steps)...`);
    const stepVideoFiles = [];

    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      const html = getVSCodeHTML(step.state);
      await page.setContent(html);

      const frameImgPath = path.join(FRAMES_DIR, `s${secId}_step${i}.png`);
      await page.screenshot({ path: frameImgPath, type: 'png' });

      const stepMp4Path = path.join(FRAMES_DIR, `s${secId}_step${i}.mp4`);
      // Encode image to video of step.dur seconds at 30 fps
      const cmd = `"${FFMPEG_PATH}" -hide_banner -loglevel error -y -loop 1 -t ${step.dur.toFixed(3)} -i "${frameImgPath}" -c:v libx264 -preset veryfast -pix_fmt yuv420p -r 30 "${stepMp4Path}"`;
      execSync(cmd);
      stepVideoFiles.push(stepMp4Path);
    }

    // Concatenate steps for this section
    const concatTxt = path.join(FRAMES_DIR, `s${secId}_concat.txt`);
    fs.writeFileSync(concatTxt, stepVideoFiles.map(f => `file '${f.replace(/\\/g, '/')}'\n`).join(''), 'utf-8');

    const outMkv = path.join(CAPTURES_DIR, `section-${secId}-obs.mkv`);
    // Concat and clamp exactly to targetDur
    const finalCmd = `"${FFMPEG_PATH}" -hide_banner -loglevel error -y -f concat -safe 0 -i "${concatTxt}" -t ${targetDur.toFixed(3)} -c:v libx264 -preset veryfast -pix_fmt yuv420p -r 30 "${outMkv}"`;
    execSync(finalCmd);

    const stats = fs.statSync(outMkv);
    console.log(`Saved: section-${secId}-obs.mkv (${(stats.size/1024).toFixed(1)} KB)`);
  }

  await browser.close();
  console.log('\nAll 11 VS Code screen recording tutorial clips generated successfully!');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});

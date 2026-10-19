// Authored instructional graphics. Text and outputs follow day-01-spoken-script.md.
export const scenes = [
  {
    id: '01-shell-vs-script', duration: 4,
    placement: 'Hook or section 9: after live shell/file demonstration; do not replace the real proof shot.',
    title: 'Same expression. Different display.',
    body: `<div class="columns">
      <div class="panel reveal"><div class="panel-top"><span class="dot"></span> PYTHON SHELL <span class="tag">INTERACTIVE</span></div><div class="code">&gt;&gt;&gt; <b>10 + 20</b><br><span class="answer">30</span></div><div class="note">The shell displays an expression's value.</div></div>
      <div class="panel reveal"><div class="panel-top"><span class="dot"></span> HELLO.PY <span class="tag">SAVED FILE</span></div><div class="code"><span class="muted">01</span> <b>10 + 20</b><br><span class="muted">$ python hello.py</span><br><span class="quiet">(no printed output)</span></div><div class="note">A script needs <em>print(…)</em> to show it.</div></div>
    </div><div class="ribbon reveal">The calculation runs in both places. Only one displays it automatically.</div>`,
  },
  {
    id: '02-execution-flow', duration: 3.5,
    placement: 'Section 3 or 8: explain instructions → interpreter → output, before or after the real terminal run.',
    title: 'Your code becomes a result.',
    body: `<div class="flow"><div class="flow-card reveal"><div class="symbol">{ }</div><h2>WRITE</h2><p>hello.py</p><code>print(10 + 20)</code></div><div class="connector reveal">→</div><div class="flow-card reveal"><div class="symbol">▶</div><h2>RUN</h2><p>Python interpreter</p><code>python hello.py</code></div><div class="connector reveal">→</div><div class="flow-card reveal"><div class="symbol">30</div><h2>SEE</h2><p>terminal output</p><code>30</code></div></div><div class="ribbon reveal">The editor stores the file; the interpreter executes it.</div>`,
  },
  {
    id: '03-python-uses', duration: 3.5,
    placement: 'Section 3: short bridge over the spoken applications list; return quickly to the working file.',
    title: 'One starting point. Many directions.',
    body: `<div class="trio"><div class="topic reveal"><div class="topic-mark">↻</div><h2>AUTOMATION</h2><p>Repeat a task reliably</p><div class="diagram">input → steps → done</div></div><div class="topic reveal"><div class="topic-mark">▥</div><h2>DATA</h2><p>Find a pattern in values</p><div class="bars"><i></i><i></i><i></i><i></i><i></i></div></div><div class="topic reveal"><div class="topic-mark">⌘</div><h2>WEB</h2><p>Build an application</p><div class="diagram">request → response</div></div></div><div class="ribbon reveal">AI tools are another destination. Start with one clear instruction.</div>`,
  },
  {
    id: '04-prompt-map', duration: 3.5,
    placement: 'Section 5: insert after demonstrating exit() in the actual terminal.',
    title: 'Look at the prompt first.',
    body: `<div class="columns"><div class="panel reveal"><div class="panel-top">TERMINAL <span class="tag">STARTS PROGRAMS</span></div><div class="code"><span class="yellow">$</span> python --version<br><span class="yellow">$</span> python hello.py</div><div class="note">Use your working command: python, py or python3.</div></div><div class="panel reveal"><div class="panel-top">PYTHON SHELL <span class="tag">ACCEPTS PYTHON CODE</span></div><div class="code"><span class="blue">&gt;&gt;&gt;</span> 10 + 20<br><span class="answer">30</span><br><span class="blue">&gt;&gt;&gt;</span> exit()</div><div class="note">Leave the shell before running a terminal command.</div></div></div><div class="ribbon reveal">Terminal command ≠ Python statement</div>`,
  },
  {
    id: '05-syntax-repair', duration: 4,
    placement: 'Section 7: after live broken-file capture, use as an annotated replay of the one-character repair.',
    title: 'One missing character. One clear fix.',
    body: `<div class="repair panel reveal"><div class="panel-top"><span class="dot"></span> HELLO.PY <span class="tag">BROKEN EXAMPLE → FIX</span></div><div class="code large"><span class="muted">01</span> <span class="bad step-before">print("Hello, Python!"<span class="cursor">▏</span></span><span class="good step-after">print("Hello, Python!")</span></div><div class="error-line step-before">SyntaxError: '(' was never closed</div><div class="success-line step-after">$ python hello.py<br>Hello, Python!</div></div><div class="ribbon reveal">Compare the punctuation. Add <strong>)</strong>. Run again.</div>`,
  },
  {
    id: '06-types-map', duration: 4,
    placement: 'Section 10: preview beside the actual type() demonstration, not instead of live output.',
    title: 'What kind of value is this?',
    body: `<div class="types"><div class="type reveal"><span class="sample">30</span><span class="type-name">int</span><span class="type-desc">whole number</span></div><div class="type reveal"><span class="sample">3.5</span><span class="type-name">float</span><span class="type-desc">decimal</span></div><div class="type reveal"><span class="sample">"Python"</span><span class="type-name">str</span><span class="type-desc">text</span></div><div class="type reveal"><span class="sample">True</span><span class="type-name">bool</span><span class="type-desc">Boolean</span></div></div><div class="ribbon reveal"><code>type(30)</code> → <code>&lt;class 'int'&gt;</code> · <code>"30"</code> is text, not a number.</div>`,
  },
  {
    id: '07-exercise-card', duration: 4.5,
    placement: 'Section 11: hold or loop while asking learner to pause; keep solution hidden.',
    title: 'Your turn: build it, run it, change it.',
    body: `<div class="challenge"><div class="challenge-num reveal">01</div><div class="challenge-steps"><div class="reveal"><span>1</span> Create a new <code>.py</code> file.</div><div class="reveal"><span>2</span> Print your name and <code>10 + 20</code>.</div><div class="reveal"><span>3</span> Show the types of <code>30</code>, <code>3.5</code> and <code>"Python"</code>.</div><div class="reveal"><span>4</span> Run it, change one line, run it again.</div></div></div><div class="ribbon reveal">PAUSE HERE · Try it before opening the lab solution.</div>`,
  },
];

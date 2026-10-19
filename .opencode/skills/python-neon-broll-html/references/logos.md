# Brand logos

Rule: when the script, title or any on-screen word names a language, tool, library, platform or social network, show **its real logo**, resolved from the keyword. Examples: "Python" → Python logo, "pip" → PyPI, "GitHub" → GitHub, "YouTube", "Instagram", "X"/"Twitter" → X.

## How
- Heading badge for the scene's subject: `logo:"python"` or `logos:["python","github"]` in the scene file (max 3).
- Inline wherever a brand appears in text, cells, nodes or outputs: `{{logo:youtube}}` (renders at 1.1em, in the text colour rules below).
- Check a keyword: `node scripts/logos.js <keyword>`. Aliases handled: py, js, ts, node, gh, vscode, pip, k8s, mongo, c++, html, twitter→x, yt, ig, fb, bash…
- ~66 popular logos are bundled offline (`assets/logos/bundle.json`: languages, Python libraries, dev tools, cloud, social). Anything else among ~3,400 brands is fetched once from the `simple-icons` npm package and cached, if the machine has npm access.

## Rules
- Use the published mark as is: brand colour on the dark background, except near-black brands (GitHub, X, TikTok, Threads, Medium…) which render white so they stay visible. Do not recolour to the neon palette, rotate, skew, crop, animate the shape, or add effects. A logo is an exception to the green/violet/cyan role colours.
- Fade/slide in with the element it belongs to; keep it the same size and place across scenes.
- Not every brand exists (LinkedIn, Microsoft/Azure/Windows, AWS, VS Code, OpenAI, Slack, C#, CSS3 were absent from the bundled set at the time of writing). For those: ask the user for the official SVG and save it to `assets/logos/custom/<slug>.svg`; otherwise leave the logo out. **Never hand-draw or approximate a logo.**
- Logos are trademarks of their owners; the icon data is CC0 (Simple Icons). Use them only to identify the thing being taught (nominative use) and don't imply endorsement. Check a brand's guidelines for monetised or sponsored use.

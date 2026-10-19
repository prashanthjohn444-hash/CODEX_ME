# Concept recipes

Working scenes live in `assets/scenes/`: `strings.js` (lanes), `decision.js` (decision), `loop.js` (loop). Copy one, change the strings and step times, and build with `node scripts/build.js scene.js <outDir> --target all`. Step command syntax is in SKILL.md.

## Ready (copy and edit)
- **Strings, indexing and slicing:** `strings.js`. Add `name[-1]` → `n` as a second scene instead of crowding this one.
- **if / else:** `decision.js` (`age = 20` → TRUE branch runs, FALSE dims). For `elif`, make a second scene.
- **while loop:** `loop.js` (three passes, then the check turns `False`). For `for i in range(3)`: use nodes NEXT ITEM → HAS MORE? → BODY → (blank/“next”), and note that `range(3)` stops before 3.

## Lanes recipes (change `input`, `memory`, `output`, `steps`)
- **Variables / reassignment:** input `score = 25`, `score = 30`, `print(score)`; memory one cell `[["25","score"]]`; at the reassignment line add `set:c0=30`; output `30`. Say the box is a metaphor: a name is bound to a value.
- **Lists:** input `fruits = ["apple", "kiwi", "plum"]`, `fruits.append("fig")`, `print(len(fruits))`; memory 4 cells (apple kiwi plum fig, indexes 0–3), reveal the 4th on the append line; output `4`.
- **Functions:** input `def double(n):` / `&nbsp;&nbsp;&nbsp;&nbsp;return n * 2` / `print(double(4))`; memory cells `[["4","n"],["8","return"]]` revealed in order; output `8`.
- **Dict lookup:** memory cells `[["'a'","key"],["1","value"]]` pairs; `hot:` the matching pair.

## Extending the template
- **New layout:** add a function to `LAY` in the engine returning panel HTML built with `P(cls,id,title,body)`; reuse `show/lit/dim/set` so the timeline keeps working. Give every animated element an id and the `fade` class (or `ln`/`cell`).
- **Side-by-side comparison:** two `.col` panels with matching row ids (`a0,b0`…), same colour roles, `lit` the row being compared.
- **More than 6 cells:** shrink `.cell` width in `cqw`; never shrink text below 1.6cqw.
- **Exact fonts:** if Bebas Neue/Barlow are installed locally the stacks pick them up; do not add CDN links (the file must work offline).

## Logo examples
- Tooling scene: `logos:["python","pypi"]`, input `pip install requests`, output cell `{{logo:pypi}}`.
- Social call-to-action: title `FOLLOW`, cells `[["{{logo:youtube}}","YouTube"],["{{logo:instagram}}","Instagram"],["{{logo:x}}","X"]]`, `hot:` each in turn.
- Version control: `logo:"git"`, nodes `INIT / ADD / COMMIT / PUSH` with `{{logo:github}}` in the last node text.

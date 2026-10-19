/* Day 1 · Section 08 — edit, save, run, then change one line and run again.
   Learner outcome: the terminal command 'python hello.py' prints the file; changing the file means
   saving it and running the same command again.
   Verified with real Python runs: python g_hello.py -> 'Hello, Python!' then 30. */
const SCENE={
 layout:"flow", theme:"neon", title:"EDIT · SAVE · RUN", subtitle:"Change one line, then run it again", logo:"python",
 input:{label:"FILE · hello.py", lines:['print("Hello, Python!")','print(10 + 20)']},
 nodes:[["EDIT","hello.py"],["SAVE","Ctrl+S"],["RUN","python hello.py"],["CHANGE","one line"]],
 output:{label:"TERMINAL", lines:['Hello, Python!','30']},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.5,"show:l1"],[0.9,"show:nodes"],[1.15,"lit:n0"],[1.65,"lit:n1"],
  [2.15,"lit:n2"],[2.55,"show:pout"],[2.65,"show:o0"],[3.1,"show:o1"],[3.5,"lit:n3"]],
 duration:4.0
};

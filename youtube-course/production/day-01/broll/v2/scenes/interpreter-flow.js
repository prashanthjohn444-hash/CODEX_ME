/* Day 1 · Section 04 — what actually runs the file.
   Learner outcome: the editor only writes the file; python.exe (3.x) is the program that executes it.
   Verified with real Python runs: python g_hello.py -> 'Hello, Python!' then 30 ;
   python --version -> Python 3.13.15 (the exact interpreter used for this batch). */
const SCENE={
 layout:"flow", theme:"neon", title:"INTERPRETER FLOW", subtitle:"python.exe runs the file, not the editor", logo:"python",
 input:{label:"FILE · hello.py", lines:['print("Hello, Python!")','print(10 + 20)']},
 nodes:[["FILE","hello.py"],["COMMAND","python hello.py"],["INTERPRETER","python.exe"],["OUTPUT","terminal"]],
 output:{label:"PRINTS", lines:['Hello, Python!','30']},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.5,"show:l1"],[0.9,"show:nodes"],[1.15,"lit:n0"],[1.65,"lit:n1"],
  [2.15,"lit:n2"],[2.65,"lit:n3"],[3.05,"lit:"],[3.1,"show:pout,o0"],[3.5,"show:o1"]],
 duration:4.0
};

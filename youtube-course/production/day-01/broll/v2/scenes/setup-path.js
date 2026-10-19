/* Day 1 · Section 02 — the destination of the lesson: setup -> shell -> file -> run.
   Learner outcome: Python, somewhere to write code, and a way to run it are the three things needed.
   Verified with real Python runs: the two print lines below output 'Hello, Python!' then 30. */
const SCENE={
 layout:"flow", theme:"neon", title:"SETUP PATH", subtitle:"Python, a shell, then a file", logo:"python",
 input:{label:"DESTINATION · hello.py", lines:['print("Hello, Python!")','print(10 + 20)']},
 nodes:[["SETUP","python.org"],["SHELL","try it"],["FILE","hello.py"],["RUN","python hello.py"]],
 output:{label:"TERMINAL", lines:['Hello, Python!','30']},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.5,"show:l1"],[0.9,"show:nodes"],[1.15,"lit:n0"],[1.65,"lit:n1"],
  [2.15,"lit:n2"],[2.65,"lit:n3"],[3.05,"lit:"],[3.1,"show:pout,o0"],[3.5,"show:o1"]],
 duration:4.0
};

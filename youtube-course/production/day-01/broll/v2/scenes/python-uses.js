/* Day 1 · Section 03 — one interpreter, several destinations.
   Learner outcome: automation, data and web/AI all start from the same tiny instruction plus its result.
   Verified with real Python runs: 'print("Hello, Python!")' -> Hello, Python! ; 'print(10 + 20)' -> 30. */
const SCENE={
 layout:"flow", theme:"paper", title:"WHAT PYTHON DOES", subtitle:"One interpreter, then three destinations", logo:"python",
 input:{label:"THE SAME START", lines:['print("Hello, Python!")','print(10 + 20)']},
 nodes:[["PYTHON","interpreter"],["AUTOMATION","scripts"],["DATA","analysis"],["WEB + AI","apps"]],
 output:{label:"SAME FIRST STEP", lines:['Hello, Python!','30']},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.5,"show:l1"],[0.9,"show:nodes"],[1.15,"lit:n0"],[1.65,"lit:n1"],
  [2.15,"lit:n2"],[2.65,"lit:n3"],[3.05,"lit:"],[3.1,"show:pout,o0"],[3.5,"show:o1"]],
 duration:4.0
};

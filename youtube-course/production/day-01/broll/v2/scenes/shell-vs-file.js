/* Day 1 · Section 01 + 09 — the opening puzzle: the shell echoes a value, a saved file does not.
   Learner outcome: an expression alone prints nothing in a file; print(...) is what shows it.
   Verified with real Python runs: REPL '10 + 20' -> 30 ; file containing only '10 + 20' -> no output ;
   print(10 + 20) -> 30. */
const SCENE={
 layout:"compare", theme:"paper", title:"SHELL vs FILE", subtitle:"Same line, different result", logo:"python",
 input:{label:"ONE CALCULATION", lines:['10 + 20','print(10 + 20)']},
 left:{label:"PYTHON SHELL", lines:['>>> 10 + 20','30']},
 right:{label:"SAVED FILE", lines:['10 + 20','nothing printed']},
 output:{label:"WHY", lines:['shell echoes the value → 30','file stays quiet → use print()']},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.45,"show:l1"],[0.9,"show:bt"],[1.05,"show:a0,a1"],[1.4,"lit:bt"],
  [1.95,"show:bf"],[2.1,"show:b0,b1"],[2.4,"lit:bf"],[2.9,"lit:"],[2.95,"show:pout,o0"],[3.35,"show:o1"]],
 duration:4.0
};

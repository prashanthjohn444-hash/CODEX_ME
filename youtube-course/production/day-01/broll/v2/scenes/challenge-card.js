/* Day 1 · Section 11 — the challenge card (still-card, no logo emphasis, under 4 s).
   Learner outcome: write a greeting file, run it from the terminal, then change one line.
   Verified with a real Python run of exactly the three lines in YOUR FILE, in order:
   print("Hello, Python!") -> Hello, Python!
   print(10 + 20)          -> 30
   print(type(30))         -> <class 'int'> */
const SCENE={
 layout:"flow", theme:"paper", title:"DAY 1 CHALLENGE", subtitle:"Save and run your own greeting file",
 input:{label:"YOUR FILE", lines:['print("Hello, Python!")','print(10 + 20)','print(type(30))']},
 nodes:[["WRITE","greeting.py"],["SAVE","Ctrl+S"],["RUN","in terminal"],["CHANGE","one line"]],
 output:{label:"YOU SHOULD SEE", lines:['Hello, Python!','30',"&lt;class 'int'&gt;"]},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.45,"show:l1"],[0.6,"show:l2"],[0.8,"show:nodes"],[1.0,"lit:n0"],
  [1.5,"lit:n1"],[2.0,"lit:n2"],[2.5,"lit:n3"],[2.9,"lit:"],[2.95,"show:pout,o0"],[3.2,"show:o1"],[3.4,"show:o2"]],
 duration:3.6
};

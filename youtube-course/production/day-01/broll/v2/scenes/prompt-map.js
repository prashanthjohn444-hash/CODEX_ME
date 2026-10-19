/* Day 1 · Section 05 — which prompt am I looking at?
   Learner outcome: >>> is the Python shell, PS> is the terminal; exit() leaves the shell so
   'python hello.py' can be typed at the terminal.
   Verified with real Python runs: REPL '10 + 20' -> 30 ; REPL 'exit()' -> no output, prompt returns ;
   python g_hello.py -> 'Hello, Python!' then 30. */
const SCENE={
 layout:"compare", theme:"paper", title:"WHICH PROMPT?", subtitle:"Terminal starts programs; the shell takes code", logo:"python",
 input:{label:"READ THE PROMPT", lines:['>>>   inside Python','PS>   in the terminal']},
 left:{label:"PYTHON SHELL", lines:['>>> 10 + 20','30','>>> exit()']},
 right:{label:"TERMINAL", lines:['PS C:\\python-30-days>','python hello.py','Hello, Python!']},
 output:{label:"TO RUN A FILE", lines:['still in the shell → exit()','then type → python hello.py']},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.45,"show:l1"],[0.9,"show:bt"],[1.05,"show:a0,a1,a2"],[1.4,"lit:bt"],
  [1.95,"show:bf"],[2.1,"show:b0,b1,b2"],[2.4,"lit:bf"],[2.9,"lit:"],[2.95,"show:pout,o0"],[3.35,"show:o1"]],
 duration:4.0
};

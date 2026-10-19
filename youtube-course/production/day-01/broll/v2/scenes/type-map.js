/* Day 1 · Section 10 — 30 and "30" look the same when printed, but they are different types.
   Learner outcome: type(30) is int, type('30') is str; quotes make text.
   Verified with real Python runs (Python 3.13.15):
   print(30) -> 30 ; print("30") -> 30 ; type(30) -> <class 'int'> ; type('30') -> <class 'str'>. */
const SCENE={
 layout:"compare", theme:"paper", title:"SAME LOOK, TWO TYPES", subtitle:"Digits inside quotes are text", logo:"python",
 input:{label:"BOTH PRINT 30", lines:['print(30)','print("30")']},
 left:{label:"30 · NUMBER", lines:["type(30)","&lt;class 'int'&gt;"]},
 right:{label:"'30' · TEXT", lines:["type('30')","&lt;class 'str'&gt;"]},
 output:{label:"SAME LOOK, DIFFERENT TYPE", lines:['print(30) → int','print("30") → str']},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.45,"show:l1"],[0.9,"show:bt"],[1.05,"show:a0,a1"],[1.4,"lit:bt"],
  [1.95,"show:bf"],[2.1,"show:b0,b1"],[2.4,"lit:bf"],[2.9,"lit:"],[2.95,"show:pout,o0"],[3.35,"show:o1"]],
 duration:4.0
};

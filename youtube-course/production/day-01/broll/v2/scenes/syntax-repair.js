/* Day 1 · Section 07 — break one line, then repair it.
   Learner outcome: a missing closing parenthesis is a syntax error, not a broken learner;
   adding ) makes the same line run and print.
   Verified with real Python runs (Python 3.13.15): running a file whose first line is
   'print("Hello, Python!"' exits 1 with the last line 'SyntaxError: '(' was never closed' ;
   the repaired line prints exactly: Hello, Python! */
const SCENE={
 layout:"decision", theme:"neon", title:"SYNTAX REPAIR", subtitle:"Close the parenthesis, then it runs", logo:"python",
 input:{label:"BROKEN EXAMPLE", lines:['print("Hello, Python!"','print(10 + 20)']},
 cond:{label:"CLOSING PARENTHESIS", text:"opening (  =  closing )", start:"missing"},
 branches:{t:['print("Hello, Python!")'], f:['print("Hello, Python!"']},
 output:{label:"RESULT", lines:["SyntaxError: '(' was never closed",'repaired → Hello, Python!']},
 steps:[[0.12,"show:h"],[0.3,"show:pin,l0"],[0.45,"show:l1"],[0.85,"show:cond"],[1.15,"show:bt,bf"],
  [1.45,"lit:bf"],[1.75,"show:pout,o0"],[2.35,"lit:"],[2.4,"set:cv=added"],[2.7,"lit:bt"],[2.75,"dim:bf"],
  [3.1,"show:o1"]],
 duration:4.0
};

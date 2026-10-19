const SCENE={
 layout:"decision", title:"IF / ELSE", subtitle:"Only one branch runs", logo:"python",
 input:{label:"INPUT", lines:['age = 20','if age >= 18:','&nbsp;&nbsp;&nbsp;&nbsp;print("adult")','else:','&nbsp;&nbsp;&nbsp;&nbsp;print("minor")']},
 cond:{label:"CONDITION", text:"age >= 18", start:"?"},
 branches:{t:['print("adult")'], f:['print("minor")']},
 output:{label:"OUTPUT", lines:['<em>printed</em>→<strong>adult</strong>']},
 steps:[[0.15,"show:h"],[0.35,"show:pin"],[0.5,"show:l0"],[0.65,"show:l1"],[0.8,"show:l2"],[0.95,"show:l3"],[1.1,"show:l4"],
  [1.5,"show:cond"],[1.7,"show:bt,bf"],[2.2,"set:cv=True"],[2.5,"lit:bt"],[2.5,"dim:bf"],[3.1,"show:pout,o0"]],
 duration:4.5
};

const SCENE={
 layout:"lanes", title:"STRINGS", subtitle:"Text is a sequence of characters, counted from 0", logo:"python",
 input:{label:"INPUT", lines:['name = "Python"','print(name[0])','print(name[1:4])']},
 memory:{label:"MEMORY · name", cells:[["P",0],["y",1],["t",2],["h",3],["o",4],["n",5]]},
 output:{label:"OUTPUT", lines:['<em>name[0]</em>→<strong>P</strong>','<em>name[1:4]</em>→<strong>yth</strong><em>(stops before index 4)</em>']},
 steps:[[0.15,"show:h"],[0.4,"show:pin"],[0.55,"show:l0"],[1.1,"show:pmem"],
  [1.3,"show:c0"],[1.48,"show:c1"],[1.65,"show:c2"],[1.82,"show:c3"],[2,"show:c4"],[2.17,"show:c5"],
  [2.5,"show:l1"],[2.7,"hot:0"],[2.95,"show:pout,o0"],
  [3.45,"show:l2"],[3.45,"hot:"],[3.65,"hot:1,2,3"],[3.95,"show:o1"]],
 duration:4.5
};

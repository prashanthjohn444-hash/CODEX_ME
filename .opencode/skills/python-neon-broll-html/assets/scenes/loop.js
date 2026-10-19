const SCENE={
 layout:"loop", title:"WHILE LOOP", subtitle:"Check, run the body, update, repeat", logo:"python",
 input:{label:"INPUT", lines:['i = 0','while i &lt; 3:','&nbsp;&nbsp;&nbsp;&nbsp;print(i)','&nbsp;&nbsp;&nbsp;&nbsp;i += 1']},
 nodes:[["INIT","i = 0"],["CHECK","i &lt; 3"],["BODY","print(i)"],["UPDATE","i += 1"]],
 counter:{name:"i", value:"0"},
 output:{label:"OUTPUT", lines:['<strong>0</strong>','<strong>1</strong>','<strong>2</strong>']},
 steps:[[0.15,"show:h"],[0.35,"show:pin"],[0.5,"show:l0"],[0.6,"show:l1"],[0.7,"show:l2"],[0.8,"show:l3"],
  [1.05,"show:nodes,c0"],[1.25,"lit:n0"],
  [1.5,"lit:n1"],[1.75,"lit:n2"],[1.75,"show:pout,o0"],[2,"lit:n3"],[2,"set:c0=1"],
  [2.2,"lit:n1"],[2.4,"lit:n2"],[2.4,"show:o1"],[2.6,"lit:n3"],[2.6,"set:c0=2"],
  [2.8,"lit:n1"],[3,"lit:n2"],[3,"show:o2"],[3.2,"lit:n3"],[3.2,"set:c0=3"],
  [3.45,"lit:n1"],[3.45,"set:n1=False"],[3.8,"lit:"]],
 duration:4.5
};

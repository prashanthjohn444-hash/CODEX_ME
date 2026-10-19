const SCENE={
 layout:"compare", theme:"paper", title:"LIST vs TUPLE", subtitle:"Square brackets can change; round ones can't", logo:"python",
 input:{label:"INPUT", lines:['a = [1, 2, 3]','b = (1, 2, 3)']},
 left:{label:"LIST [ ]", lines:['a[0] = 9','print(a) → [9, 2, 3]']},
 right:{label:"TUPLE ( )", lines:['b[0] = 9','TypeError: not assignable']},
 output:{label:"RESULT", lines:['<em>list</em><strong>mutable</strong>','<em>tuple</em><strong>immutable</strong>']},
 steps:[[0.15,"show:h"],[0.35,"show:pin,l0"],[0.55,"show:l1"],[0.9,"show:bt,a0"],[1.15,"show:bf,b0"],[1.5,"show:a1"],[1.5,"lit:bt"],[1.9,"show:b1"],[1.9,"lit:bf"],[1.9,"dim:bt"],[2.7,"show:pout,o0"],[3.2,"show:o1"]],
 duration:4.5
};

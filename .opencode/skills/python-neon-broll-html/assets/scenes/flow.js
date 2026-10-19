const SCENE={
 layout:"flow", theme:"neon", title:"FUNCTION CALL", subtitle:"Arguments go in, a value comes back", logo:"python",
 input:{label:"INPUT", lines:['def add(a, b):','    return a + b','print(add(2, 3))']},
 nodes:[["CALL","add(2, 3)"],["PARAMS","a=2, b=3"],["BODY","a + b"],["RETURN","?"]],
 output:{label:"OUTPUT", lines:['<em>print(add(2, 3))</em>→<strong>5</strong>']},
 steps:[[0.15,"show:h"],[0.3,"show:pin,l0"],[0.45,"show:l1"],[0.6,"show:l2"],[0.9,"show:nodes"],[1.1,"lit:n0"],[1.5,"lit:n1"],[1.9,"lit:n2"],[2.3,"lit:n3"],[2.3,"set:n3=5"],[3.0,"show:pout,o0"]],
 duration:4.5
};

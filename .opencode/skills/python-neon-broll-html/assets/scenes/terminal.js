const SCENE={
 layout:"flow", theme:"terminal", title:"pip install", subtitle:"Fetch a library from PyPI", logos:["python","pypi"],
 input:{label:"TERMINAL", lines:['$ pip install requests']},
 nodes:[["pip","install"],["{{logo:pypi}}","find package"],["DOWNLOAD","requests"],["READY","import requests"]],
 output:{label:"RESULT", lines:['<em>Successfully installed</em><strong>requests</strong>']},
 steps:[[0.15,"show:h"],[0.3,"show:pin,l0"],[0.7,"show:nodes"],[0.9,"lit:n0"],[1.3,"lit:n1"],[1.7,"lit:n2"],[2.1,"lit:n3"],[2.7,"show:pout,o0"]],
 duration:4.5
};

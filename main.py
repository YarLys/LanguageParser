import json
from lark import Lark, Transformer, v_args, tree

G = r'''
NUM: /[0-9]+/
NAME: /[a-zA-Z_]+/
STR: /"[^"]*"/
OPER: /["+"|"-"|"*"]/
WS: /\s+|REM.*|<#[\s\S]*?#>/
%ignore WS

?val: NUM | STR | dict 

assign: NAME "=" val

const: NAME ":" val ";"

addition: "$(+" NAME [" "] val ")"

subtraction: "$(-" NAME [" "] val ")"

multiplication: "$(*" NAME [" "] val ")"

variable: const | assign

max: "max" "(" NAME [", "] NAME ")"

dict: NAME "([" [assign ("," assign)*] "]" ")"

start: (dict | variable | addition | subtraction | multiplication | max)* -> obj
'''

src = '''
REM TEST PROGRAM

<#vm = {
    ar = [1 2 3]
}
r = "MIREA"
#>

first: "privet";

table([
    a = 1,
    basdf_ = "hello", 
    c_fsdaf = dict([
        hello = "hi"
    ])
])

constant: 213;
const: 500;

$(+ constant 4)

max(constant, const)

$(* constant 5)

<#
alo
alo??
#>
'''.strip()

variables = dict()  # словарь для хранения констант
json_output = []  # список для хранения результата
inside_dict = False  # флаг, указывающий, находимся ли мы внутри словаря

@v_args(inline=True)
class Tree(Transformer):
    NAME = str
    NUM = int

    def STR(self, x):
        return x[1:-1]
    def assign(self, k, v):
        if not inside_dict:  # Проверяем, не находимся ли мы внутри словаря
            variables[k] = v
            typ = type(v)
            json_output.append({"type": typ, "name": k, "value": v})
        return (k, v)

    def const(self, k, v):
        if not inside_dict:  # Проверяем, не находимся ли мы внутри словаря
            variables[k] = v
            typ = type(v)
            json_output.append({"type": typ, "name": k, "value": v})
        return (k, v)

    def dict(self, name, *assigns):
        global inside_dict
        inside_dict = True
        variables[name] = assigns
        json_output.append({"type": "dict", "name": name, "values": ""})
        for assign in assigns:
            json_output[len(json_output)-1]["values"] += (Tree(assign))
        inside_dict = False
        return ('dict', list(assigns))

    def addition(self, name, v):
        variables[name] += v
        json_output.append({"type": "addition", "name": name, "new_value": variables[name]})
        return (name, variables[name])

    def subtraction(self, name, v):
        variables[name] -= v
        json_output.append({"type": "subtraction", "name": name, "new_value": variables[name]})
        return (name, variables[name])

    def multiplication(self, name, v):
        variables[name] *= v
        json_output.append({"type": "multiplication", "name": name, "new_value": variables[name]})
        return (name, variables[name])

    def max(self, a, b):
        c = max(variables[a], variables[b])
        json_output.append({"type": "max", a: variables[a], b: variables[b], "result": c})
        return ('max', a, b)

parser = Lark(G, parser="lalr", transformer=Tree(), start='start')
parser.parse(src)
json_result = json.dumps(json_output, indent=4, ensure_ascii=False)
print(json_result)
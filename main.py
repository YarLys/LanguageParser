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

max: "max" "(" NAME [", "] NAME ")"

dict: NAME "([" [assign ("," [assign | dict])*] "]" ")"

start: (dict | const | assign | addition | subtraction | multiplication | max)* 
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
    dict([
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
@v_args(inline=True)
class Tree(Transformer):
    NAME = str
    NUM = int

    def STR(self, x):
        return x[1:-1]
    def assign(self, k, v):
        return (k, v)

    def const(self, k, v):
        return (k, v)

    def dict(self, name, *assigns):
        return ('dict', name, list(assigns))

    def addition(self, name, v):
        return (name, v)

    def subtraction(self, name, v):
        return (name, v)

    def multiplication(self, name, v):
        return (name, v)

    def max(self, a, b):
        return ('max', a, b)

def execute(tree, inside_dict):
    match tree:
        case (k, v):
            typ = type(v).__name__
            if not inside_dict:  # Проверяем, не находимся ли мы внутри словаря
                variables[k] = v
                json_output.append({"type": typ, "name": k, "value": v})
                return {}
            else:
                return {"type": typ, "name": k, "value": v}

        case ('dict', name, assigns):
            if not inside_dict:
                variables[name] = assigns
                json_output.append({"type": "dict", "name": name, "values": []})
                for assign in assigns:
                    d = execute(assign, True)
                    json_output[len(json_output) - 1]["values"].append(d)
                return {}
            else:
                variables[name] = assigns
                out = {"type": "dict", "name": name, "values": []}
                for assign in assigns:
                    d = execute(assign, True)
                    out["values"].append(d)
                return out

        case ('addition', name, v):
            if not inside_dict:
                variables[name] += v
                json_output.append({"type": "addition", "name": name, "new_value": variables[name]})
                return {}
            else:  # пока что по сути переписываю логику в else, тк ещё не ясно, нужен ли он будет вообще. А так нагляднее и удобнее для изменений
                variables[name] += v
                return {"type": "addition", "name": name, "new_value": variables[name]}

        case ('subtraction', name, v):
            if not inside_dict:
                variables[name] -= v
                json_output.append({"type": "subtraction", "name": name, "new_value": variables[name]})
            else:
                variables[name] -= v
                return {"type": "subtraction", "name": name, "new_value": variables[name]}

        case ('multiplication', name, v):
            if not inside_dict:
                variables[name] *= v
                json_output.append({"type": "multiplication", "name": name, "new_value": variables[name]})
            else:
                variables[name] *= v
                return {"type": "multiplication", "name": name, "new_value": variables[name]}

        case ('max', a, b):
            if not inside_dict:
                print(variables)
                c = max(variables[a], variables[b])
                json_output.append({"type": "max", a: variables[a], b: variables[b], "result": c})
            else:
                c = max(variables[a], variables[b])
                return {"type": "max", a: variables[a], b: variables[b], "result": c}


parser = Lark(G, parser="lalr", transformer=Tree(), start='start')
tree = parser.parse(src)
print(tree)
# Запускаем execute для каждого узла дерева
for node in tree.children:
    execute(node, False)
# Сериализация в JSON
json_result = json.dumps(json_output, indent=4, ensure_ascii=False)
print(json_result)
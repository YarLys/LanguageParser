import sys
from pprint import pprint
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
@v_args(inline=True)
class Tree(Transformer):
    NAME = str
    NUM = int

    def STR(self, x):
        return x[1:-1]

    def assign(self, k, v):
        print(k, '=', v)
        variables[k] = v
        return (k, v)

    def const(self, k, v):
        print(k, '=', v)
        variables[k] = v
        return (k, v)

    def dict(self, name, *assigns):
        print(name)
        variables[name] = assigns
        return ('dict', list(assigns))

    def addition(self, name, v):
        variables[name] += v
        return (name, variables[name])

    def subtraction(self, name, v):
        variables[name] -= v
        return (name, variables[name])

    def multiplication(self, name, v):
        variables[name] *= v
        return (name, variables[name])

    def max(self, a, b):
        c = max(variables[a], variables[b])
        return ('max', a, b)


'''def execute(tree):
    match tree:
        case ('max', a, b):
            print('Maximum between', a, 'and', b, '=', max(a, b))
        case (name, value):  # любое присваивание
            print(name, "=", value)
        case ('dict', dictionary):
            # print(name, '=')
            for assign in dictionary:
                execute(assign)'''


parser = Lark(G, parser="lalr", transformer=Tree())
parser.parse(src)
print(variables)
#print(parser.parse(src).pretty())
#execute(parser.parse(src))

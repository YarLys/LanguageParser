import json
import sys
from lark import Lark, Transformer, v_args, tree, LarkError, exceptions

G = r'''
NUM: /[0-9]+/
NAME: /[a-zA-Z_]+/
STR: /"[^"]*"/
OPER: /["+"|"-"|"*"]/
WS: /\s+|REM.*|<#[\s\S]*?#>/
%ignore WS

?val: NUM | STR | dict | max

assign: NAME "=" val

const: NAME ":" val ";"

addition: "$(+" NAME [" "] val ")"

subtraction: "$(-" NAME [" "] val ")"

multiplication: "$(*" NAME [" "] val ")"

max: "max" "(" NAME [", "] NAME ")"

dict: NAME "([" [assign ("," [assign | dict])*] "]" ")"

start: (dict | const | assign | addition | subtraction | multiplication | max)* 
'''

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
        return ('addition', name, v)

    def subtraction(self, name, v):
        return ('subtraction', name, v)

    def multiplication(self, name, v):
        return ('multiplication', name, v)

    def max(self, a, b):
        return ('max', a, b)

def execute(tree, inside_dict, json_output, variables):
    match tree:
        case (k, v):
            if (k in variables):
                raise LarkError(f"Константа {k} уже существует!")
            typ = type(v).__name__
            if not inside_dict:  # Проверяем, не находимся ли мы внутри словаря
                if typ != 'tuple':
                    variables[k] = v
                    json_output.append({f"{k}": v})
                    return {}
                else:
                    c = execute(v, inside_dict, json_output, variables)
                    variables[k] = c
                    json_output.append({f"{k}": c})
            else:
                if typ != 'tuple':
                    variables[k] = v
                    return {f"{k}": v}
                else:
                    c = execute(v, inside_dict, json_output, variables)
                    variables[k] = c
                    return {f"{k}": c}

        case ('dict', name, assigns):
            if (name in variables):
                raise LarkError(f"Словарь {name} уже существует!")
            if not inside_dict:
                variables[name] = assigns
                json_output.append({"type": "dict", "name": name, "values": []})
                for assign in assigns:
                    d = execute(assign, True, json_output, variables)
                    json_output[len(json_output) - 1]["values"].append(d)
                return {}
            else:
                variables[name] = assigns
                out = {"type": "dict", "name": name, "values": []}
                for assign in assigns:
                    d = execute(assign, True, json_output, variables)
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
            c = max(variables[a], variables[b])
            return c


def parse(src):
    try:
        parser = Lark(G, parser="lalr", transformer=Tree(), start='start')
        tree = parser.parse(src)
        # Запускаем execute для каждого узла дерева
        variables = dict()  # словарь для хранения констант
        json_output = [] # Список для хранения результата
        for node in tree.children:
            execute(node, False, json_output, variables)
        # Сериализация в JSON
        json_result = json.dumps(json_output, indent=4, ensure_ascii=False)
        return json_result
    except exceptions.UnexpectedCharacters as uc:
        return f"Синтаксическая ошибка:\n{str(uc)}"
    except exceptions.LarkError as le:
        return f"Ошибка при обработке исходной программы:\n{str(le)}"


if __name__ == "__main__":
    src = sys.stdin.read()
    output = parse(src.strip())
    print(output)

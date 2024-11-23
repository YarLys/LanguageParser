import unittest
from main import parse

class TestParser(unittest.TestCase):
    def test_one_comment(self):
        src = '''
                REM Однострочный комментарий
                <#Большой
                многострочный
                комментарий#>
                REM Всем пока!
                '''.strip()
        expected = '''[]'''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

    def test_constants(self):
        src = '''
            first_const: "hello world";
            second: 500;
            third: "bye bye";
            '''.strip()
        expected = '''
            [
                {
                    "type": "str",
                    "name": "first_const",
                    "value": "hello world"
                },
                {
                    "type": "int",
                    "name": "second",
                    "value": 500
                },
                {
                    "type": "str",
                    "name": "third",
                    "value": "bye bye"
                }
            ]
        '''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

    def test_calculations(self):
        src = '''
            a: 100;
            b: 7435;
            $(+ a 50)
            $(- b 7000)
        '''.strip()
        expected = '''
            [
                {
                    "type": "int",
                    "name": "a",
                    "value": 100
                },
                {
                    "type": "int",
                    "name": "b",
                    "value": 7435
                },
                {
                    "type": "addition",
                    "name": "a",
                    "new_value": 150
                },
                {
                    "type": "subtraction",
                    "name": "b",
                    "new_value": 435
                }
            ]
        '''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

    def test_max(self):
        src = '''
            a: 100;
            b: 7435;
            max(a, b)
        '''.strip()
        expected = '''
            [
                {
                    "type": "int",
                    "name": "a",
                    "value": 100
                },
                {
                    "type": "int",
                    "name": "b",
                    "value": 7435
                },
                {
                    "type": "max",
                    "a": 100,
                    "b": 7435,
                    "result": 7435
                }
            ]
        '''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

    def test_dictionaries(self):
        src = '''
            slovar([
                privet = "hello",
                num = 100,
                dict_inside([
                    mir = "world",
                    test = 123
                ])
            ])
        '''.strip()
        expected = '''
        [
            {
                "type": "dict",
                "name": "slovar",
                "values": [
                    {
                        "type": "str",
                        "name": "privet",
                        "value": "hello"
                    },
                    {
                        "type": "int",
                        "name": "num",
                        "value": 100
                    },
                    {
                        "type": "dict",
                        "name": "dict_inside",
                        "values": [
                            {
                                "type": "str",
                                "name": "mir",
                                "value": "world"
                            },
                            {
                                "type": "int",
                                "name": "test",
                                "value": 123
                            }
                        ]
                    }
                ]
            }
        ]
        '''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

    def test_big_prog(self):
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
        expected = '''
        [
        {
            "type": "str",
            "name": "first",
            "value": "privet"
        },
        {
            "type": "dict",
            "name": "table",
            "values": [
                {
                    "type": "int",
                    "name": "a",
                    "value": 1
                },
                {
                    "type": "str",
                    "name": "basdf_",
                    "value": "hello"
                },
                {
                    "type": "dict",
                    "name": "dict",
                    "values": [
                        {
                            "type": "str",
                            "name": "hello",
                            "value": "hi"
                        }
                    ]
                }
            ]
        },
        {
            "type": "int",
            "name": "constant",
            "value": 213
        },
        {
            "type": "int",
            "name": "const",
            "value": 500
        },
        {
            "type": "addition",
            "name": "constant",
            "new_value": 217
        },
        {
            "type": "max",
            "constant": 217,
            "const": 500,
            "result": 500
        },
        {
            "type": "multiplication",
            "name": "constant",
            "new_value": 1085
        }
        ]
        '''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

if __name__ == '__main__':
    unittest.main()
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
        expected = '''{}S'''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

    def test_constants(self):
        src = '''
            first_const: "hello world";
            second: 500;
            third: "bye bye";
            '''.strip()
        expected = '''
            {
                "first_const": "hello world",
                "second": 500,
                "third": "bye bye"
            }
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
            {
                "a": 150,
                "b": 435
            }
        '''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

    def test_max(self):
        src = '''
            a: 100;
            b: 7435;
            c: max(a, b);
        '''.strip()
        expected = '''
            {
                "a": 100,
                "b": 7435,
                "c": 7435
            }
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
        {
            "slovar": [
                {
                    "privet": "hello"
                },
                {
                    "num": 100
                },
                {
                    "dict_inside": [
                        {
                            "mir": "world"
                        },
                        {
                            "test": 123
                        }
                    ]
                }
            ]
        }
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
        
        maxi: max(constant, const);
        
        $(* constant 5)
        
        <#
        alo
        alo??
        #>
        '''.strip()
        expected = '''
        {
            "first": "privet",
            "table": [
                {
                    "a": 1
                },
                {
                    "basdf_": "hello"
                },
                {
                    "dict": [
                        {
                            "hello": "hi"
                        }
                    ]
                }
            ],
            "constant": 1085,
            "const": 500,
            "maxi": 500
        }
        '''
        self.assertEqual(parse(src).strip().split(), expected.strip().split())

if __name__ == '__main__':
    unittest.main()

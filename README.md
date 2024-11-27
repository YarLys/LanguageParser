# Домашнее задание 3 по конфигурационному управлению
## Лысаков Ярослав, ИКБО-50-23
## Этапы запуска проекта репозитория
1. Загрузить репозиторий на компьютер. 'git clone https://github.com/YarLys/LanguageParser'
2. Перейти в директорию проекта: 'cd LanguageParser'
3. Выполнить инициализирующий скрипт: 'bash script.sh'. Также можно воспользоваться командой 'pip install lark'.
4. Запустить программу командой: 'python main.py'.
5. Ввести код исходной программы согласно заданию.
6. Завершить ввод нажатием сочетания клавиш 'Ctrl + Z'.
## Описание задания
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на учебном конфигурационном языке принимается из
стандартного ввода. Выходной текст на языке json попадает в стандартный
вывод.
## Синтаксис учебного конфигурационного языка
### Однострочные комментарии:
REM Это однострочный комментарий
### Многострочные комментарии:
<#
Это многострочный
комментарий
#>
### Словари:
table([
 имя = значение,
 имя = значение,
 имя = значение,
 ...
])
### Имена:
[_a-zA-Z]+
### Значения:
• Числа.
• Строки.
• Словари.
### Строки:
"Это строка"
### Объявление константы на этапе трансляции:
имя: значение;
### Вычисление константного выражения на этапе трансляции (префиксная форма), пример:
$(+ имя 1)
Результатом вычисления константного выражения является значение.
### Для константных вычислений определены операции и функции:
1. Сложение.
2. Вычитание.
3. Умножение.
4. max().

## Реализованные функции
### class Tree():
Содержит функции по каждой возможности языка. Нужен для разбора дерева лексем.
### def execute():
Выполняет необходимые действия в зависимости от каждой лексемы, которая поступает ему в качестве аргумента.
### def parse():
Формирование дерева лексем, его разбор, формирование выходного текста в JSON-формате.
### def main():
Ввод кода на учебном конфигурационном языке и вывод результата после преобразования.

## Примеры работы программы
### Пример 1
#### Код, поступающий на вход программы:
  ```
  REM Это пример с нахождением максимума 
  a: 40;
  b: 20;
  c: max(a, b);
  ```
#### Результат работы программы:
  ```
  [
    {
        "a": 40
    },
    {
        "b": 20
    },
    {
        "c": 40
    }
  ]
  ```
### Пример 2
#### Код, поступающий на вход программы:
  ```
  REM Это пример со словарями 
    slovar([
        privet = "hello",
        num = 100,
        dict_inside([
            mir = "world",
            test = 123
        ])
    ])
  ```
#### Результат работы программы:
  ```
  [
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
  ]
  ```
### Пример 3
#### Код, поступающий на вход программы:
  ```
  first_const: "hello world";
  second: 500;
  third: "bye bye";
  ```
#### Результат работы программы:
  ```
  [
        {
            "first_const": "hello world"
        },
        {
            "second": 500
        },
        {
            "third": "bye bye"
        }
    ]
  ```
## Результаты тестирования
![image](https://github.com/user-attachments/assets/70d47fb3-a6c5-4684-9e66-83fb623f2198)
![image](https://github.com/user-attachments/assets/effca65a-da5e-4dfe-8705-4a0919084228)
![image](https://github.com/user-attachments/assets/0bb20d14-5bf2-46b0-b92b-253513be6f5e)
![image](https://github.com/user-attachments/assets/6ebc71e9-1f89-49b6-a0ef-a7a66e2bec9b)
![image](https://github.com/user-attachments/assets/9876a18d-b23f-4ef7-8d3f-681483575a17)
![image](https://github.com/user-attachments/assets/c7da9bcf-c518-47c8-bc83-585db2c313e7)
![image](https://github.com/user-attachments/assets/2c834686-ad67-4090-b379-a3f37af04b5d)
![image](https://github.com/user-attachments/assets/1f0c40ae-95cc-4d84-9607-2bd80eb8832a)
![image](https://github.com/user-attachments/assets/1fd16bfa-d452-4268-bf89-59ef0ac77bc9)
![image](https://github.com/user-attachments/assets/c35af375-ba25-4ec9-b195-503934659fd8)
![image](https://github.com/user-attachments/assets/10188416-5e15-4cb8-a240-c533d93a96a6)
![image](https://github.com/user-attachments/assets/021c281a-1316-4c7e-85b2-bd709fde4c55)

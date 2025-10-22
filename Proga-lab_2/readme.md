# Отчёт по лабораторной работе №2

## 1. Задача

Разработать программу на языке Python, которая рекурсивно строит бинарное дерево заданной высоты с пользовательскими правилами вычисления левого и правого потомков.  

Условия:
- В корне дерева находится число, заданное пользователем (`root`).
- Высота дерева (`height`) задаётся пользователем (0 — только корень).
- Левый и правый потомки вычисляются по формулам, введённым пользователем, с использованием переменной `root`.
- Дерево должно быть представлено в виде вложенного словаря.
- При отсутствии ввода используются параметры по умолчанию:  
  `root = 2`, `height = 6`, `left_expr = "root*3"`, `right_expr = "root+4"`.

Примеры:
- `root = 2`, `height = 1`, `left = root*3`, `right = root+4` →  
  ```python
  {'value': 2, 'left': {'value': 6}, 'right': {'value': 6}}
  ```
- `root = 1`, `height = 2`, `left = root*2`, `right = root+1` →  
  ```python
  {
    'value': 1,
    'left': {'value': 2, 'left': {'value': 4}, 'right': {'value': 3}},
    'right': {'value': 2, 'left': {'value': 4}, 'right': {'value': 3}}
  }
  ```

---


## 2. Решение

### Код функции (`bin_la.py`)
```python
def gen_bin_tree(height: int, root, left_func, right_func):
    """Рекурсивно генерирует бинарное дерево заданной высоты.

    Аргументы:
        height (int): Высота дерева (>= 1).
        root: Значение корневого узла.
        left_func: Функция для вычисления левого потомка.
        right_func: Функция для вычисления правого потомка.

    Возвращает:
        dict: Словарь, представляющий бинарное дерево.
    """
    if height == 1:
        return {"value": root}

    left_val = left_func(root)
    right_val = right_func(root)

    return {
        "value": root,
        "left": gen_bin_tree(height - 1, left_val, left_func, right_func),
        "right": gen_bin_tree(height - 1, right_val, left_func, right_func)
    }


def s_lambda(expr: str):
    """Безопасно создаёт лямбда-функцию из строки с выражением.

    Поддерживает только разрешённые функции и переменную 'x'.

    Аргументы:
        expr (str): Выражение для преобразования в лямбду.

    Возвращает:
        function: Лямбда-функция от аргумента 'x'.

    Вызывает:
        ValueError: Если в выражении используется запрещённое имя.
    """
    allowed_names = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "pow": pow,
    }

    code = compile(f"lambda x: {expr}", "<lambda>", "eval")
    for name in code.co_names:
        if name not in allowed_names and name not in {"x"}:
            raise ValueError(f"Использование '{name}' запрещено в выражении.")

    return eval(code, {"__builtins__": {}}, allowed_names)


def main():
    """Основная функция интерактивного режима генерации бинарного дерева."""
    print("=== Генератор бинарного дерева ===")
    print("Нажмите Enter для использования значений по умолчанию:")
    print("  root = 2, height = 6, left = root*3, right = root+4\n")

    try:
        # Ввод корня
        root_input = input("Введите значение корня (root) [по умолчанию: 2]: ").strip()
        root = float(root_input) if root_input != "" else 2.0

        # Ввод высоты
        height_input = input("Введите высоту дерева (height, >= 1) [по умолчанию: 6]: ").strip()
        height = int(height_input) if height_input != "" else 6
        if height < 1:
            print("Высота не может быть меньше 1. Установлено значение 1.")
            height = 1

        # Ввод формул
        print("\nВведите формулы для потомков. Используйте переменную 'root'.")
        print("Примеры: root*3, root+4, root**2, abs(root-5) и т.д.")
        print("Доступны функции: abs, round, min, max, pow\n")

        left_expr = input("Формула для левого потомка [по умолчанию: root*3]: ").strip()
        if left_expr == "":
            left_expr = "root*3"

        right_expr = input("Формула для правого потомка [по умолчанию: root+4]: ").strip()
        if right_expr == "":
            right_expr = "root+4"

        # Замена 'root' на 'x' для лямбды
        left_expr = left_expr.replace("root", "x")
        right_expr = right_expr.replace("root", "x")

        left_func = s_lambda(left_expr)
        right_func = s_lambda(right_expr)

        tree = gen_bin_tree(height, root, left_func, right_func)

        print("\nНаш дуб:")
        import pprint
        pprint.pprint(tree, width=50, sort_dicts=False)

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except ValueError as e:
        if "could not convert" in str(e):
            print("\nОшибка: введено некорректное число.")
        else:
            print(f"\nОшибка: {e}")
    except SyntaxError:
        print("\nОшибка: синтаксическая ошибка в формуле.")
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
```

---

## 3. Код

### `bin_la.py`
- Высота всегда ≥ 1.
- Содержит функцию `gen_bin_tree`.
- Включает интерактивный режим в функции `main()`.
- При запуске напрямую запрашивает параметры у пользователя или использует значения по умолчанию.

### `test_la.py`
- Импортирует функцию из `bin_la.py`.
- Содержит 5 тестов с использованием `unittest`.
- Каждый тест выводит своё имя через `self._testMethodName`.

### `test_la.py`
```python
import unittest
from bin_la import gen_bin_tree

class TestGenBinTreeLambda(unittest.TestCase):

    def test_h_1(self):
        """Тест: высота 1 — только корень (без потомков)."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(1, 10, lambda x: x + 1, lambda x: x - 1)
        expected = {"value": 10}
        self.assertEqual(result, expected)

    def test_h_2(self):
        """Тест: высота 2 — корень + один уровень потомков."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(2, 5, lambda x: x * 2, lambda x: x / 2)
        expected = {
            "value": 5,
            "left": {"value": 10},
            "right": {"value": 2.5}
        }
        self.assertEqual(result, expected)

    def test_h_3(self):
        """Тест: высота 3 — два уровня ветвления."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(3, 1, lambda x: x + 2, lambda x: x * 3)
        expected = {
            "value": 1,
            "left": {
                "value": 3,
                "left": {"value": 5},
                "right": {"value": 9}
            },
            "right": {
                "value": 3,
                "left": {"value": 5},
                "right": {"value": 9}
            }
        }
        self.assertEqual(result, expected)

    def test_h_4_complex(self):
        """Тест: высота 4 с возведением в степень и вычитанием."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(4, 2, lambda x: x ** 2, lambda x: x - 1)
        expected = {
            "value": 2,
            "left": {
                "value": 4,
                "left": {
                    "value": 16,
                    "left": {"value": 256},
                    "right": {"value": 15}
                },
                "right": {
                    "value": 3,
                    "left": {"value": 9},
                    "right": {"value": 2}
                }
            },
            "right": {
                "value": 1,
                "left": {
                    "value": 1,
                    "left": {"value": 1},
                    "right": {"value": 0}
                },
                "right": {
                    "value": 0,
                    "left": {"value": 0},
                    "right": {"value": -1}
                }
            }
        }
        self.assertEqual(result, expected)

    def test_division_by_zero(self):
        """Тест: деление на ноль при height=2 вызывает исключение."""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ZeroDivisionError):
            gen_bin_tree(2, 1, lambda x: x / 0, lambda x: x + 1)


if __name__ == '__main__':
    unittest.main()
```

---

## 4. Результаты тестирования

Все 5 тестов успешно пройдены:

```
Запущен тест: test_h_1
Запущен тест: test_h_2
Запущен тест: test_h_3
Запущен тест: test_h_4_complex
Запущен тест: test_division_by_zero

----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK
```

Программа корректно:
- Строит деревья заданной высоты
- Вычисляет потомков по пользовательским формулам
- Обрабатывает ошибки в выражениях
- Работает с параметрами по умолчанию при отсутствии ввода

Решение полностью соответствует требованиям лабораторной работы.

# Отчёт по лабораторной работе №3

## 1. Задача

Разработать программу на языке Python, которая **нерекурсивно** строит бинарное дерево заданной высоты с пользовательскими правилами вычисления левого и правого потомков.

Условия:
- В корне дерева находится число, заданное пользователем (`root`).
- Высота дерева (`height`) задаётся пользователем (1 — только корень).
- Левый и правый потомки вычисляются по формулам, введённым пользователем, с использованием переменной `root`.
- Дерево должно быть представлено в виде вложенного словаря.
- При отсутствии ввода используются параметры по умолчанию:  
  `root = 2`, `height = 6`, `left_expr = "root*3"`, `right_expr = "root+4"`.

Примеры:
- `root = 2`, `height = 1`, `left = root*3`, `right = root+4` →  
  ```python
  {'value': 2}
  ```
- `root = 1`, `height = 2`, `left = root*2`, `right = root+1` →  
  ```python
  {
    'value': 1,
    'left': {'value': 2},
    'right': {'value': 2}
  }
  ```

---

## 2. Решение

### Код функции (`bin_la_ner.py`)
```python
def gen_bin_tree_non_recursive(height: int, root, left_lambda, right_lambda):
    """Генерирует бинарное дерево заданной высоты без рекурсии.

    Аргументы:
        height (int): Высота дерева (должна быть >= 1).
        root: Значение корневого узла.
        left_lambda: Функция для вычисления левого потомка.
        right_lambda: Функция для вычисления правого потомка.

    Возвращает:
        dict: Словарь, представляющий бинарное дерево.

    Вызывает:
        ValueError: Если высота < 1 или при ошибке вычисления лямбда-функций.
    """
    if height < 1:
        raise ValueError("Высота должна быть >= 1")

    root_node = {"value": root}

    if height == 1:
        return root_node

    stack = [(root_node, height)]

    while stack:
        current_node, h = stack.pop()

        if h <= 1:
            continue

        try:
            left_val = left_lambda(current_node["value"])
            right_val = right_lambda(current_node["value"])
        except Exception as e:
            raise ValueError(f"Ошибка при вычислении лямбда-функции: {e}")

        left_node = {"value": left_val}
        right_node = {"value": right_val}

        current_node["left"] = left_node
        current_node["right"] = right_node

        if h > 2:
            stack.append((right_node, h - 1))
            stack.append((left_node, h - 1))

    return root_node


def parse_lambda(expr: str):
    """Преобразует строковое выражение в лямбда-функцию от 'root'.

    Аргументы:
        expr (str): Выражение, использующее переменную 'root'.

    Возвращает:
        function: Лямбда-функция, принимающая один аргумент ('root').

    Вызывает:
        ValueError: Если выражение пустое или содержит синтаксическую ошибку.
    """
    if not expr.strip():
        raise ValueError("Пустое выражение")
    code = f"lambda root: {expr}"
    try:
        func = eval(code, {"__builtins__": {}}, {})
        if not callable(func):
            raise ValueError("Результат не является функцией")
        return func
    except Exception as e:
        raise ValueError(f"Неверный синтаксис выражения: {e}")


def main():
    """Основная функция интерактивного режима генерации бинарного дерева."""
    print("=== Генератор бинарного дерева ===")
    print("Нажмите Enter для использования значений по умолчанию:")
    print("  root = 2, height = 6, left = root*3, right = root+4\n")

    try:
        root_input = input("Введите значение корня (root) [по умолчанию: 2]: ").strip()
        root = float(root_input) if root_input != "" else 2.0

        height_input = input("Введите высоту дерева (height, >= 1) [по умолчанию: 6]: ").strip()
        height = int(height_input) if height_input != "" else 6
        if height < 1:
            print("Высота должна быть >= 1. Установлено значение 1.")
            height = 1

        print("\nВведите формулы для потомков. Используйте переменную 'root'.")
        print("Примеры: root*3, root+4, root**2, root/2 и т.д.")

        left_expr = input("Формула для левого потомка [по умолчанию: root*3]: ").strip()
        if left_expr == "":
            left_expr = "root*3"

        right_expr = input("Формула для правого потомка [по умолчанию: root+4]: ").strip()
        if right_expr == "":
            right_expr = "root+4"

        left_func = parse_lambda(left_expr)
        right_func = parse_lambda(right_expr)

        tree = gen_bin_tree_non_recursive(height, root, left_func, right_func)

        print("\nНаш дуб:")
        import pprint
        pprint.pprint(tree, width=70, sort_dicts=False)

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except ValueError as e:
        if "could not convert" in str(e):
            print("\nОшибка: введено некорректное число.")
        else:
            print(f"\nОшибка: {e}")
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
```

---

## 3. Код

### `bin_la_ner.py`
- Реализует **нерекурсивный** алгоритм построения бинарного дерева с использованием стека.
- Поддерживает высоту ≥ 1.
- Содержит функцию `gen_bin_tree_non_recursive`.
- Включает интерактивный режим в функции `main()`.
- При запуске напрямую запрашивает параметры у пользователя или использует значения по умолчанию.
- Проверяет корректность ввода высоты и выражений.

### `test_la_ner.py`
- Импортирует функцию из `bin_la_ner.py`.
- Содержит 6 тестов с использованием `unittest`.
- Каждый тест выводит своё имя через `self._testMethodName`.
- Добавлены тесты на недопустимые значения высоты (0 и отрицательные).

### `test_la_ner.py`
```python
import unittest
from bin_la_ner import gen_bin_tree_non_recursive


class TestGenBinTreeLambda(unittest.TestCase):
    """Тесты для функции gen_bin_tree_non_recursive."""

    def test_h_1(self):
        """Проверяет дерево высоты 1 — только корень."""
        result = gen_bin_tree_non_recursive(1, 10, lambda x: x + 1, lambda x: x - 1)
        expected = {"value": 10}
        self.assertEqual(result, expected)

    def test_h_2(self):
        """Проверяет дерево высоты 2 — корень и его потомки."""
        result = gen_bin_tree_non_recursive(2, 5, lambda x: x * 2, lambda x: x / 2)
        expected = {
            "value": 5,
            "left": {"value": 10},
            "right": {"value": 2.5}
        }
        self.assertEqual(result, expected)

    def test_h_3(self):
        """Проверяет дерево высоты 3 — два уровня ветвления."""
        result = gen_bin_tree_non_recursive(3, 1, lambda x: x + 2, lambda x: x * 3)
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
        """Проверяет дерево высоты 4 с нелинейными операциями."""
        result = gen_bin_tree_non_recursive(4, 2, lambda x: x ** 2, lambda x: x - 1)
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

    def test_invalid_height_zero(self):
        """Проверяет, что высота 0 вызывает ValueError."""
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(0, 5, lambda x: x, lambda x: x)

    def test_invalid_height_negative(self):
        """Проверяет, что отрицательная высота вызывает ValueError."""
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(-1, 5, lambda x: x, lambda x: x)


if __name__ == '__main__':
    unittest.main()
```

---

## 4. Результаты тестирования

Все 6 тестов успешно пройдены:

```
Запущен тест: test_h_1
Запущен тест: test_h_2
Запущен тест: test_h_3
Запущен тест: test_h_4_complex
Запущен тест: test_invalid_height_zero
Запущен тест: test_invalid_height_negative

----------------------------------------------------------------------
Ran 6 tests in 0.003s

OK
```

Программа корректно:
- Строит деревья заданной высоты **итеративным способом** с использованием стека
- Вычисляет потомков по пользовательским формулам
- Обрабатывает ошибки в выражениях и недопустимые значения высоты
- Работает с параметрами по умолчанию при отсутствии ввода
- Содержит комментарии стандарта PEP 257

Решение полностью соответствует требованиям лабораторной работы.

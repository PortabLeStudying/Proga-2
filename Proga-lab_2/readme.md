# Отчёт по лабораторной работе №3

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

### Код функции (`bin.py`)
```python
def gen_bin_tree(height: int, root, left_expr: str, right_expr: str):

    if height == 0:
        return {"value": root}

    local_vars = {"root": root}

    try:
        left_val = eval(left_expr, {"__builtins__": {}}, local_vars)
        right_val = eval(right_expr, {"__builtins__": {}}, local_vars)
    except Exception as e:
        raise ValueError(f"Ошибка при вычислении выражения: {e}")

    return {
        "value": root,
        "left": gen_bin_tree(height - 1, left_val, left_expr, right_expr),
        "right": gen_bin_tree(height - 1, right_val, left_expr, right_expr)
    }


def main():
    print("=== Генератор бинарного дерева ===")
    print("Нажмите Enter для использования значений по умолчанию (№2 в списке):")
    print("  root = 2, height = 6, left = root*3, right = root+4\n")

    try:
        # Ввод корня
        root_input = input("Введите значение корня (root) [по умолчанию: 2]: ").strip()
        root = float(root_input) if root_input != "" else 2.0

        # Ввод высоты
        height_input = input("Введите высоту дерева (height, >= 0) [по умолчанию: 6]: ").strip()
        height = int(height_input) if height_input != "" else 6
        if height < 0:
            print("Высота не может быть отрицательной. Установлено значение 0.")
            height = 0

        # Ввод формул
        print("\nВведите формулы для потомков. Используйте переменную 'root'.")
        print("Примеры: root*3, root-4, root+root*3/6, root**2 и т.д.")

        left_expr = input("Формула для левого потомка [по умолчанию: root*3]: ").strip()
        if left_expr == "":
            left_expr = "root*3"

        right_expr = input("Формула для правого потомка [по умолчанию: root+4]: ").strip()
        if right_expr == "":
            right_expr = "root+4"

        # Генерация дерева
        tree = gen_bin_tree(height, root, left_expr, right_expr)

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
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
```

---

## 3. Код

Код разделён на два файла:

### `bin.py`
- Содержит функцию `gen_bin_tree`.
- Включает интерактивный режим в функции `main()`.
- При запуске напрямую запрашивает параметры у пользователя или использует значения по умолчанию.

### `test_bin_tree.py`
- Импортирует функцию из `bin.py`.
- Содержит 6 тестов с использованием `unittest`.
- Каждый тест выводит своё имя через `self._testMethodName`.

```python
import unittest
from bin import gen_bin_tree


class TestGenBinTree(unittest.TestCase):

    def test_height_0(self):
        """Тест: дерево высоты 0 — только корень"""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(height=0, root=5, left_expr="root*2", right_expr="root+1")
        expected = {"value": 5}
        self.assertEqual(result, expected)

    def test_height_1_default(self):
        """Тест: высота 1, формулы root*3 и root+4, корень = 2"""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(height=1, root=2, left_expr="root*3", right_expr="root+4")
        expected = {
            "value": 2,
            "left": {"value": 6},
            "right": {"value": 6}
        }
        self.assertEqual(result, expected)

    def test_custom(self):
        """Тест: кастомные формулы"""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(height=1, root=3, left_expr="root+1", right_expr="root*2")
        expected = {
            "value": 3,
            "left": {"value": 4},
            "right": {"value": 6}
        }
        self.assertEqual(result, expected)

    def test_height_2(self):
        """Тест: высота 2 с формулами root*2 и root+1, корень = 1"""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree(height=2, root=1, left_expr="root*2", right_expr="root+1")
        expected = {
            "value": 1,
            "left": {
                "value": 2,
                "left": {"value": 4},
                "right": {"value": 3}
            },
            "right": {
                "value": 2,
                "left": {"value": 4},
                "right": {"value": 3}
            }
        }
        self.assertEqual(result, expected)

    def test_invalid(self):
        """Тест: некорректное выражение вызывает ValueError"""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ValueError):
            gen_bin_tree(height=1, root=2, left_expr="root**", right_expr="root+4")

    def test_unsafe(self):
        """Тест: попытка использовать запрещённые функции (например, open)"""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ValueError):
            gen_bin_tree(height=1, root=2, left_expr="open('test.txt')", right_expr="root+4")


if __name__ == "__main__":
    unittest.main()
```

---

## 4. Результаты тестирования

Все 6 тестов успешно пройдены:

```
Запущен тест: test_custom
Запущен тест: test_height_0
Запущен тест: test_height_1_default
Запущен тест: test_height_2
Запущен тест: test_invalid
Запущен тест: test_unsafe

----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

Программа корректно:
- Строит деревья заданной высоты
- Вычисляет потомков по пользовательским формулам
- Обрабатывает ошибки в выражениях
- Работает с параметрами по умолчанию при отсутствии ввода

Решение полностью соответствует требованиям лабораторной работы.

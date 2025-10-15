# Отчёт по лабораторной работе №3

## 1. Задача

Разработать программу на языке Python, которая нерекурсивно строит бинарное дерево заданной высоты с пользовательскими правилами вычисления левого и правого потомков.

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
  {'value': 2}
  ```
- `root = 1`, `height = 2`, `left = root+2`, `right = root*3` →  
  ```python
  {
    'value': 1,
    'left': {'value': 3},
    'right': {'value': 3}
  }
  ```
- `root = 2`, `height = 3`, `left = root**2`, `right = root-1` →  
  ```python
  {
    'value': 2,
    'left': {
      'value': 4,
      'left': {'value': 16},
      'right': {'value': 3}
    },
    'right': {
      'value': 1,
      'left': {'value': 1},
      'right': {'value': 0}
    }
  }
  ```

---

## 2. Решение

### Код функции (`bin_nerek.py`)
```python
def gen_bin_tree_non_recursive(height: int, root, left_expr: str, right_expr: str):
    if height == 0:
        return {"value": root}

    root_node = {"value": root}
    if height == 0:
        return root_node

    stack = [(root_node, height)]

    while stack:
        current_node, h = stack.pop()

        if h <= 1:
            continue

        local_vars = {"root": current_node["value"]}
        try:
            left_val = eval(left_expr, {"__builtins__": {}}, local_vars)
            right_val = eval(right_expr, {"__builtins__": {}}, local_vars)
        except Exception as e:
            raise ValueError(f"Ошибка при вычислении выражения: {e}")

        left_node = {"value": left_val}
        right_node = {"value": right_val}

        current_node["left"] = left_node
        current_node["right"] = right_node

        if h > 2:
            stack.append((right_node, h - 1))
            stack.append((left_node, h - 1))

    return root_node


def main():
    print("=== Генератор бинарного дерева ===")
    print("Нажмите Enter для использования значений по умолчанию:")
    print("  root = 2, height = 6, left = root*3, right = root+4\n")

    try:
        root_input = input("Введите значение корня (root) [по умолчанию: 2]: ").strip()
        root = float(root_input) if root_input != "" else 2.0

        height_input = input("Введите высоту дерева (height, >= 0) [по умолчанию: 6]: ").strip()
        height = int(height_input) if height_input != "" else 6
        if height < 0:
            print("Высота не может быть отрицательной. Установлено значение 0.")
            height = 0

        print("\nВведите формулы для потомков. Используйте переменную 'root'.")
        print("Примеры: root*3, root+4, root-4, root+root*3/6, root**2 и т.д.")

        left_expr = input("Формула для левого потомка [по умолчанию: root*3]: ").strip()
        if left_expr == "":
            left_expr = "root*3"

        right_expr = input("Формула для правого потомка [по умолчанию: root+4]: ").strip()
        if right_expr == "":
            right_expr = "root+4"

        tree = gen_bin_tree_non_recursive(height, root, left_expr, right_expr)

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

Код разделён на два файла:

### `bin_nerek.py`
- Содержит функцию `gen_bin_tree_non_recursive`, реализующую стековый подход к построению бинарного дерева.
- При запуске напрямую запрашивает параметры у пользователя или использует значения по умолчанию.

### `test_bin_nerek.py`
- Импортирует функцию из `bin_nerek.py`.
- Содержит 7 тестов с использованием `unittest`.

```python
import unittest
from bin_nerek import gen_bin_tree_non_recursive

class TestGenBinTreeNonRecursive(unittest.TestCase):

    def test_h_0(self):
        """Тест: высота 0, должно вернуть корень."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree_non_recursive(0, 10, "root + 1", "root - 1")
        expected = {"value": 10}
        self.assertEqual(result, expected)

    def test_h_1(self):
        """Тест: высота 1, без вычислений."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree_non_recursive(1, 5, "root * 2", "root / 2")
        expected = {"value": 5}
        self.assertEqual(result, expected)

    def test_h_2_c(self):
        """Тест: высота 2, вычисления с выражениями."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree_non_recursive(2, 1, "root + 2", "root * 3")
        expected = {
            "value": 1,
            "left": {"value": 3},  # root(1) + 2
            "right": {"value": 3}  # root(1) * 3
        }
        self.assertEqual(result, expected)

    def test_h_3_cf(self):
        """Тест: высота 3, сложные выражения."""
        print(f"Запущен тест: {self._testMethodName}")
        result = gen_bin_tree_non_recursive(3, 2, "root ** 2", "root - 1")
        expected = {
            "value": 2,
            "left": {
                "value": 4, # 2**2
                "left": {"value": 16}, # 4**2
                "right": {"value": 3}  # 4-1
            },
            "right": {
                "value": 1, # 2-1
                "left": {"value": 1},  # 1**2
                "right": {"value": 0}   # 1-1
            }
        }
        self.assertEqual(result, expected)

    def test_invalid(self):
        """Тест: неверное выражение должно вызвать ValueError."""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(2, 1, "root / 0", "root + 1")

    def test_ext_var(self):
        """Тест: нет доступа к внешним переменным."""
        print(f"Запущен тест: {self._testMethodName}")
        global external_var
        external_var = 100
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(2, 1, "external_var", "root + 1")

    def test_builtin(self):
        """Тест: нет доступа к встроенным функциям."""
        print(f"Запущен тест: {self._testMethodName}")
        with self.assertRaises(ValueError):
            gen_bin_tree_non_recursive(2, 1, "len(str(root))", "root + 1")


if __name__ == '__main__':
    unittest.main()
```

---

## 4. Результаты тестирования

Все 7 тестов успешно пройдены:

```
Запущен тест: test_h_0
Запущен тест: test_h_1
Запущен тест: test_h_2_c
Запущен тест: test_h_3_cf
Запущен тест: test_invalid
Запущен тест: test_ext_var
Запущен тест: test_builtin

----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```

Программа корректно:
- Строит деревья заданной высоты.
- Вычисляет потомков по пользовательским формулам на каждом уровне.
- Обрабатывает ошибки в выражениях (некорректный синтаксис, деление на ноль и т.п.).
- Обеспечивает безопасность выполнения выражений: запрещает доступ к встроенным функциям и внешним переменным.
- Работает с параметрами по умолчанию при отсутствии ввода.

Решение полностью соответствует требованиям лабораторной работы. 

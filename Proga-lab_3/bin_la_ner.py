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

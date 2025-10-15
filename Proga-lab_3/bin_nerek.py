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
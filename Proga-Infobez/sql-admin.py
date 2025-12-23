import sqlite3
# admin' -- или admin' OR '1'='1
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    # Добавим админа (пароль: "correct_pass")
    try:
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'correct_pass')")
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

def vulnerable_login():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    username = input("Логин: ")
    password = input("Пароль: ")

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[DEBUG] Выполняется запрос: {query}")

    # SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = '' - and идет выше or, поэтому SELECT * FROM users WHERE username = ('admin') OR ('1'='1' AND password = '')

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Успешный вход! Привет, {user[1]}!")
        if user[1] == 'admin':
            print("[СКРЫТАЯ ФУНКЦИЯ] Система под вашим контролем, мастер.")
    else:
        print("Ошибка входа!")

if __name__ == "__main__":
    init_db()
    vulnerable_login()
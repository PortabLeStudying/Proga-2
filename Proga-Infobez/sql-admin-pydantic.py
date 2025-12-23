import sqlite3
import re
from pydantic import BaseModel, Field, field_validator
from typing import Annotated

class LoginRequest(BaseModel):
    username: Annotated[str, Field(min_length=1, max_length=50)]
    password: Annotated[str, Field(min_length=1, max_length=100)]

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        # Удаляем пробелы по краям (аналог strip_whitespace)
        v = v.strip()
        if not v:
            raise ValueError("Логин не может быть пустым")
        if "'" in v or '"' in v:
            raise ValueError("Логин не должен содержать кавычек")
        if not re.fullmatch(r"[a-zA-Z0-9_]+", v):
            raise ValueError("Логин может содержать только буквы, цифры и символ '_")
        return v


# ---------- Инициализация базы данных ----------
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "correct_pass"))
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

def safe_login():
    try:
        raw_username = input("Логин: ")
        raw_password = input("Пароль: ")

        # Валидация через Pydantic V2
        login_data = LoginRequest(username=raw_username, password=raw_password)

    except ValueError as e:
        # Pydantic выбрасывает ValidationError, но при ручном вызове — ValueError вложен
        print(f"Некорректный ввод: {e}")
        return

    # Безопасное подключение и запрос
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Параметризованный запрос — SQL-инъекция невозможна
    cursor.execute(
        "SELECT username FROM users WHERE username = ? AND password = ?",
        (login_data.username, login_data.password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Успешный вход! Привет, {user[0]}!")
        if user[0] == 'admin':
            print("[СКРЫТАЯ ФУНКЦИЯ] Система под вашим контролем, мастер.")
    else:
        print("Неверный логин или пароль.")

if __name__ == "__main__":
    init_db()
    safe_login()
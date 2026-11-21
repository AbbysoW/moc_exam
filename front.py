import tkinter as tk
from typing import Optional, Tuple, Dict, Any


def login_form() -> Optional[Tuple[str, str]]:
    root = tk.Tk()
    root.title("Вход")
    result: list = []

    tk.Label(root, text="Логин").grid(row=0, column=0, sticky="e")
    login = tk.Entry(root)
    login.grid(row=0, column=1)

    tk.Label(root, text="Пароль").grid(row=1, column=0, sticky="e")
    password = tk.Entry(root, show="*")
    password.grid(row=1, column=1)

    def submit(login_value: str, password_value: str) -> None:
        result.append((login_value, password_value))
        root.destroy()

    tk.Button(
        root,
        text="Войти",
        command=lambda: submit(login.get(), password.get()),
    ).grid(row=2, column=0, columnspan=2, sticky="ew")
    tk.Button(
        root,
        text="Войти как гость",
        command=lambda: submit("guest", ""),
    ).grid(row=3, column=0, columnspan=2, sticky="ew")

    login.focus_set()
    root.mainloop()

    return result[0] if result else None

def store_page(user: Optional[Dict[str, Any]] = None) -> None:
    root = tk.Tk()
    root.title("Магазин")

    if user:
        tk.Label(root, text=f"Привет, {user['name']}!").pack(padx=20, pady=(20, 0))
        tk.Label(root, text=f"Роль: {user['role']}").pack(padx=20)

    tk.Label(root, text="Тут будет лента товаров").pack(padx=20, pady=20)

    root.mainloop()

from tkinter import messagebox

from db import DB
from front import login_form, store_page

if __name__ == "__main__":
    db = DB()
    db.init_db()

    credentials = login_form()
    if credentials:
        login, password = credentials

        if login == "guest":
            store_page()
        else:
            user = db.read_user_by_login(login)
            if user and user["password"] == password:
                store_page(user)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")

    db.close()

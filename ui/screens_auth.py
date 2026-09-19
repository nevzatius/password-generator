"""Account creation and login screens."""

import tkinter as tk
from tkinter import ttk

import auth


class CreateAccountFrame(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, padding=24)
        self.on_success = on_success

        ttk.Label(self, text="Hesap Oluştur", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 16)
        )

        ttk.Label(self, text="Kullanıcı adı:").grid(row=1, column=0, sticky="e", pady=4)
        self.username_entry = ttk.Entry(self, width=28)
        self.username_entry.grid(row=1, column=1, pady=4)

        ttk.Label(self, text="Şifre:").grid(row=2, column=0, sticky="e", pady=4)
        self.password_entry = ttk.Entry(self, width=28, show="*")
        self.password_entry.grid(row=2, column=1, pady=4)

        ttk.Label(self, text="Şifre (tekrar):").grid(row=3, column=0, sticky="e", pady=4)
        self.confirm_entry = ttk.Entry(self, width=28, show="*")
        self.confirm_entry.grid(row=3, column=1, pady=4)

        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(row=4, column=0, columnspan=2, pady=(4, 0))

        create_btn = ttk.Button(self, text="Hesap Oluştur", command=self._submit)
        create_btn.grid(row=5, column=0, columnspan=2, pady=(12, 0))

        self.username_entry.focus_set()
        self.bind_all("<Return>", lambda e: self._submit())

    def _submit(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not username:
            self.error_label.config(text="Kullanıcı adı boş olamaz.")
            return
        if not password:
            self.error_label.config(text="Şifre boş olamaz.")
            return
        if password != confirm:
            self.error_label.config(text="Şifreler eşleşmiyor.")
            self.confirm_entry.delete(0, tk.END)
            return

        auth.create_account(username, password)
        self.on_success(password)


class LoginFrame(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, padding=24)
        self.on_success = on_success

        username = auth.get_stored_username()

        ttk.Label(self, text=f"Hoş geldin, {username}", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 16)
        )

        ttk.Label(self, text="Şifre:").grid(row=1, column=0, sticky="e", pady=4)
        self.password_entry = ttk.Entry(self, width=28, show="*")
        self.password_entry.grid(row=1, column=1, pady=4)

        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(row=2, column=0, columnspan=2, pady=(4, 0))

        login_btn = ttk.Button(self, text="Giriş Yap", command=self._submit)
        login_btn.grid(row=3, column=0, columnspan=2, pady=(12, 0))

        self.password_entry.focus_set()
        self.bind_all("<Return>", lambda e: self._submit())

    def _submit(self):
        password = self.password_entry.get()
        if not auth.verify_login(password):
            self.error_label.config(text="Hatalı şifre.")
            self.password_entry.delete(0, tk.END)
            return
        self.on_success(password)

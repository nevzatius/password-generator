"""Root Tk window and screen-switching controller."""

import tkinter as tk
from tkinter import messagebox

from cryptography.fernet import InvalidToken

import auth
import vault as vault_module
from ui.screens_auth import CreateAccountFrame, LoginFrame
from ui.screens_main import MainFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Şifre Yöneticisi")
        self.geometry("520x560")
        self.resizable(False, False)

        self.vault: vault_module.Vault | None = None
        self._current_frame: tk.Widget | None = None

        self._show_initial_screen()

    def _show_initial_screen(self):
        if not auth.account_exists():
            self._switch_to(CreateAccountFrame(self, on_success=self._on_login_success))
        else:
            self._switch_to(LoginFrame(self, on_success=self._on_login_success))

    def _on_login_success(self, password: str):
        try:
            self.vault = vault_module.load_vault(password)
        except InvalidToken:
            messagebox.showerror(
                "Kasa Hatası",
                "Kasa dosyası çözülemedi (bozuk veya değiştirilmiş olabilir).",
            )
            return

        self._switch_to(
            MainFrame(self, self.vault, on_vault_change=self._persist_vault)
        )

    def _persist_vault(self):
        vault_module.save_vault(self.vault)

    def _switch_to(self, frame: tk.Widget):
        self.unbind_all("<Return>")
        if self._current_frame is not None:
            self._current_frame.destroy()
        self._current_frame = frame
        frame.pack(fill="both", expand=True)

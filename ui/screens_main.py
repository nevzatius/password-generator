"""Main application screen: password generator + saved vault tabs."""

import tkinter as tk
from tkinter import messagebox, ttk

import password_gen
from vault import Vault


class GeneratorTab(ttk.Frame):
    def __init__(self, master, vault: Vault, on_vault_change):
        super().__init__(master, padding=16)
        self.vault = vault
        self.on_vault_change = on_vault_change

        options = ttk.LabelFrame(self, text="Üretim Seçenekleri", padding=12)
        options.grid(row=0, column=0, sticky="ew")

        ttk.Label(options, text="Uzunluk:").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=16)
        length_spin = ttk.Spinbox(
            options, from_=4, to=64, width=6, textvariable=self.length_var
        )
        length_spin.grid(row=0, column=1, sticky="w", padx=(6, 0))

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        ttk.Checkbutton(options, text="Büyük harf (A-Z)", variable=self.use_upper).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )
        ttk.Checkbutton(options, text="Küçük harf (a-z)", variable=self.use_lower).grid(
            row=2, column=0, columnspan=2, sticky="w"
        )
        ttk.Checkbutton(options, text="Rakam (0-9)", variable=self.use_digits).grid(
            row=3, column=0, columnspan=2, sticky="w"
        )
        ttk.Checkbutton(options, text="Sembol (!@#$...)", variable=self.use_symbols).grid(
            row=4, column=0, columnspan=2, sticky="w"
        )

        ttk.Button(options, text="Üret", command=self._generate).grid(
            row=5, column=0, columnspan=2, pady=(12, 0)
        )

        result_frame = ttk.LabelFrame(self, text="Üretilen Şifre", padding=12)
        result_frame.grid(row=1, column=0, sticky="ew", pady=(16, 0))

        self.result_var = tk.StringVar(value="")
        result_entry = ttk.Entry(
            result_frame, textvariable=self.result_var, width=40, state="readonly"
        )
        result_entry.grid(row=0, column=0, sticky="ew")

        ttk.Button(result_frame, text="Panoya Kopyala", command=self._copy).grid(
            row=0, column=1, padx=(8, 0)
        )

        save_frame = ttk.LabelFrame(self, text="Kasaya Kaydet", padding=12)
        save_frame.grid(row=2, column=0, sticky="ew", pady=(16, 0))

        ttk.Label(save_frame, text="Alan/Site adı:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(save_frame, width=28)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=(6, 0))

        ttk.Button(save_frame, text="Kasaya Kaydet", command=self._save).grid(
            row=1, column=0, columnspan=2, pady=(12, 0)
        )

    def _generate(self):
        try:
            password = password_gen.generate_password(
                self.length_var.get(),
                self.use_upper.get(),
                self.use_lower.get(),
                self.use_digits.get(),
                self.use_symbols.get(),
            )
        except (ValueError, tk.TclError) as exc:
            messagebox.showerror("Üretim Hatası", str(exc))
            return
        self.result_var.set(password)

    def _copy(self):
        password = self.result_var.get()
        if not password:
            return
        self.clipboard_clear()
        self.clipboard_append(password)

    def _save(self):
        password = self.result_var.get()
        name = self.name_entry.get().strip()
        if not password:
            messagebox.showerror("Hata", "Önce bir şifre üretin.")
            return
        if not name:
            messagebox.showerror("Hata", "Alan/site adı boş olamaz.")
            return
        self.vault.add_entry(name, password)
        self.on_vault_change()
        self.name_entry.delete(0, tk.END)
        messagebox.showinfo("Kaydedildi", f"\"{name}\" için şifre kasaya kaydedildi.")


class VaultTab(ttk.Frame):
    def __init__(self, master, vault: Vault, on_vault_change):
        super().__init__(master, padding=16)
        self.vault = vault
        self.on_vault_change = on_vault_change

        self.tree = ttk.Treeview(
            self, columns=("name", "password"), show="headings", selectmode="browse"
        )
        self.tree.heading("name", text="Alan/Site")
        self.tree.heading("password", text="Şifre")
        self.tree.column("name", width=200)
        self.tree.column("password", width=260)
        self.tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=3, sticky="ns")

        ttk.Button(self, text="Kopyala", command=self._copy_selected).grid(
            row=1, column=0, pady=(8, 0), sticky="w"
        )
        ttk.Button(self, text="Sil", command=self._delete_selected).grid(
            row=1, column=1, pady=(8, 0), sticky="w"
        )
        ttk.Button(self, text="Yenile", command=self.refresh).grid(
            row=1, column=2, pady=(8, 0), sticky="w"
        )

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for entry in self.vault.entries:
            self.tree.insert("", tk.END, iid=entry.id, values=(entry.name, entry.password))

    def _copy_selected(self):
        selection = self.tree.selection()
        if not selection:
            return
        entry_id = selection[0]
        entry = next((e for e in self.vault.entries if e.id == entry_id), None)
        if entry:
            self.clipboard_clear()
            self.clipboard_append(entry.password)

    def _delete_selected(self):
        selection = self.tree.selection()
        if not selection:
            return
        entry_id = selection[0]
        entry = next((e for e in self.vault.entries if e.id == entry_id), None)
        if not entry:
            return
        if not messagebox.askyesno("Sil", f"\"{entry.name}\" kaydı silinsin mi?"):
            return
        self.vault.delete_entry(entry_id)
        self.on_vault_change()
        self.refresh()


class MainFrame(ttk.Frame):
    def __init__(self, master, vault: Vault, on_vault_change):
        super().__init__(master)
        self.vault = vault
        self.on_vault_change = on_vault_change

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.generator_tab = GeneratorTab(notebook, vault, self._handle_change)
        self.vault_tab = VaultTab(notebook, vault, self._handle_change)

        notebook.add(self.generator_tab, text="Şifre Üret")
        notebook.add(self.vault_tab, text="Kayıtlı Şifreler")

        notebook.bind("<<NotebookTabChanged>>", lambda e: self.vault_tab.refresh())

    def _handle_change(self):
        self.on_vault_change()
        self.vault_tab.refresh()

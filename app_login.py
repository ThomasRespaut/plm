import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class LoginWindow:
    def __init__(self, root, db_manager, on_login_success):
        self.root = root
        self.db_manager = db_manager
        self.on_login_success = on_login_success

        self.root.title("Connexion")
        self.root.geometry("300x200")

        self.username_label = tk.Label(root, text="Nom d'utilisateur:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Mot de passe:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Se connecter", command=self.authenticate)
        self.login_button.pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.db_manager.check_user_credentials(username, password)

        if role:
            messagebox.showinfo("Succès", f"Bienvenue {username} ({role})")
            self.root.destroy()
            self.on_login_success(role)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects.")


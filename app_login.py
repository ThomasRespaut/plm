import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class LoginWindow:
    def __init__(self, root, db_manager, on_login_success):
        self.root = root
        self.db_manager = db_manager
        self.on_login_success = on_login_success

        self.root.title("Connexion")
        self.root.geometry("300x250")

        # Champs de connexion
        self.username_label = tk.Label(root, text="Nom d'utilisateur:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Mot de passe:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        # Boutons
        self.login_button = tk.Button(root, text="Se connecter", command=self.authenticate)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(root, text="Créer un compte", command=self.create_account_form)
        self.register_button.pack(pady=10)

        self.guest_button = tk.Button(root, text="Mode Invité", command=self.guest_mode)
        self.guest_button.pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.db_manager.check_user_credentials(username, password)

        if role:
            messagebox.showinfo("Succès", f"Bienvenue {username} ({role})")
            self.root.destroy()
            self.on_login_success(username,role)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects.")

    def create_account_form(self):
        # Nouvelle fenêtre pour le formulaire de création de compte
        self.create_account_window = tk.Toplevel(self.root)
        self.create_account_window.title("Créer un compte")
        self.create_account_window.geometry("400x600")

        # Labels et champs
        self.fields = {
            "Prénom": tk.Entry(self.create_account_window),
            "Nom": tk.Entry(self.create_account_window),
            "Email": tk.Entry(self.create_account_window),
            "Téléphone": tk.Entry(self.create_account_window),
            "Adresse": tk.Entry(self.create_account_window),
            "Ville": tk.Entry(self.create_account_window),
            "Pays": tk.Entry(self.create_account_window),
            "Mot de passe": tk.Entry(self.create_account_window, show="*"),
        }

        for label, entry in self.fields.items():
            tk.Label(self.create_account_window, text=label + ":").pack(pady=5)
            entry.pack(pady=5)

        # Bouton pour soumettre
        submit_button = tk.Button(self.create_account_window, text="Créer", command=self.submit_account)
        submit_button.pack(pady=10)

    def submit_account(self):
        # Récupérer les valeurs
        account_data = {field: entry.get() for field, entry in self.fields.items()}

        # Validation des champs requis
        if not account_data["Prénom"] or not account_data["Nom"] or not account_data["Email"] or not account_data[
            "Mot de passe"]:
            messagebox.showerror("Erreur", "Les champs Prénom, Nom, Email et Mot de passe sont obligatoires.")
            return

        # Ajouter à la base de données
        success = self.db_manager.add_customer(
            account_data["Prénom"],
            account_data["Nom"],
            account_data["Email"],
            account_data["Téléphone"],
            account_data["Adresse"],
            account_data["Ville"],
            account_data["Pays"],
            account_data["Mot de passe"]
        )

        if success:
            messagebox.showinfo("Succès", "Compte créé avec succès!")
            self.create_account_window.destroy()
        else:
            messagebox.showerror("Erreur", "Erreur lors de la création du compte.")

    def guest_mode(self):
        messagebox.showinfo("Mode Invité", "Vous utilisez le mode invité.")
        self.root.destroy()
        self.on_login_success("Invité")

import openai
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_manager import DatabaseManager
from app_login import LoginWindow
import os
from dotenv import load_dotenv
import threading
import time
from chatbot import ChatbotClient  # Importer la classe extérieure

load_dotenv()

# Initialiser le client chatbot
chatbot_client = ChatbotClient()

class App:
    def __init__(self, root, db_manager, username, role):
        self.root = root
        self.db_manager = db_manager
        self.username = username
        self.role = role

        self.root.title("Perfumery.exe")
        self.root.geometry("1200x700")  # Taille adaptée pour inclure les ajustements

        # Ajouter un label en haut à droite pour afficher le rôle de l'utilisateur connecté
        self.role_label = tk.Label(
            self.root,
            text=f"Connecté en tant que : {username} ({role})",
            anchor="e",  # Aligner à droite
            bg="lightgrey",
            font=("Arial", 10, "italic")
        )
        self.role_label.pack(side="top", fill="x")  # S'étendre horizontalement en haut

        # Cadre principal (Gestion des proportions)
        self.main_frame = tk.PanedWindow(self.root, orient="horizontal", sashwidth=5)
        self.main_frame.pack(fill="both", expand=True)

        # Définir l'interface en fonction du rôle
        if role == "admin":
            self.setup_admin_interface()
        elif role == "editor":
            self.setup_editor_interface()
        elif role == "customer":
            self.setup_customer_interface()
        elif role == "viewer":
            self.setup_viewer_interface()
        else:
            # Par défaut, on considère le rôle comme "viewer"
            self.setup_viewer_interface()

    def setup_admin_interface(self):
        """Configurer l'interface pour le rôle admin."""
        # Cadre gauche pour la gestion des tables
        self.left_frame = tk.Frame(self.main_frame, bg="white")
        self.main_frame.add(self.left_frame, width=900)  # 75% de la largeur

        # Cadre droit pour le chatbot
        self.right_frame = tk.Frame(self.main_frame, bg="lightgrey")
        self.main_frame.add(self.right_frame, width=300)  # 25% de la largeur

        # Interface de gestion des tables
        self.setup_table_management()

        # Boutons pour les actions CRUD
        self.setup_crud_buttons(admin=True)

        # Interface du chatbot
        self.setup_chatbot_interface()

    def setup_editor_interface(self):
        """Configurer l'interface pour le rôle editor."""
        # Cadre gauche pour la gestion des tables
        self.left_frame = tk.Frame(self.main_frame, bg="white")
        self.main_frame.add(self.left_frame, width=900)

        # Cadre droit pour le chatbot
        self.right_frame = tk.Frame(self.main_frame, bg="lightgrey")
        self.main_frame.add(self.right_frame, width=300)

        # Interface de gestion des tables
        self.setup_table_management()

        # Boutons pour les actions CRUD (pas de suppression)
        self.setup_crud_buttons(admin=False)

        # Interface du chatbot
        self.setup_chatbot_interface()

    def setup_customer_interface(self):
        """Configurer l'interface pour le rôle customer."""
        # Cadre pour le chatbot uniquement
        self.right_frame = tk.Frame(self.main_frame, bg="lightgrey")
        self.main_frame.add(self.right_frame)  # Prend toute la largeur

        # Interface du chatbot
        self.setup_chatbot_interface()

    def setup_viewer_interface(self):
        """Configurer l'interface pour le rôle viewer."""
        # Cadre pour le chatbot uniquement (ou autre interface spécifique)
        self.right_frame = tk.Frame(self.main_frame, bg="lightgrey")
        self.main_frame.add(self.right_frame)

        # Interface du chatbot
        self.setup_chatbot_interface()

    def setup_table_management(self):
        """Configurer l'interface de gestion des tables."""
        # Interface de gestion des tables
        self.table_label = tk.Label(self.left_frame, text="Choisissez une table :")
        self.table_label.pack(pady=10)

        self.table_combobox = ttk.Combobox(
            self.left_frame,
            values=["customers", "products", "product_ranges", "range_references"]
        )
        self.table_combobox.pack(pady=10)
        self.table_combobox.bind("<<ComboboxSelected>>", self.show_table_data)

        # Ajouter un cadre pour le Treeview avec des barres de défilement
        self.tree_frame = tk.Frame(self.left_frame)
        self.tree_frame.pack(expand=True, fill="both", pady=10)

        self.tree_scroll_y = tk.Scrollbar(self.tree_frame, orient="vertical")
        self.tree_scroll_x = tk.Scrollbar(self.tree_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            self.tree_frame, columns=(), show="headings",
            yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set
        )
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        self.tree_scroll_y.pack(side="right", fill="y")
        self.tree_scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(expand=True, fill="both")

    def setup_crud_buttons(self, admin=False):
        """Configurer les boutons CRUD."""
        self.action_frame = tk.Frame(self.left_frame)
        self.action_frame.pack(pady=10)

        self.insert_button = tk.Button(
            self.action_frame, text="Insérer une ligne", command=self.insert_row
        )
        self.insert_button.grid(row=0, column=0, padx=10)

        self.update_button = tk.Button(
            self.action_frame, text="Modifier une ligne", command=self.edit_row
        )
        self.update_button.grid(row=0, column=1, padx=10)

        self.delete_button = tk.Button(
            self.action_frame, text="Supprimer une ligne", command=self.delete_row
        )
        self.delete_button.grid(row=0, column=2, padx=10)

        if not admin:
            # Désactiver le bouton de suppression pour les éditeurs
            self.delete_button.config(state="disabled")

    def setup_chatbot_interface(self):
        """Configurer l'interface du chatbot."""
        self.chat_label = tk.Label(self.right_frame, text="Chatbot OpenAI", bg="lightgrey")
        self.chat_label.pack(pady=5)

        self.chat_display = tk.Text(
            self.right_frame, height=20, state="disabled", bg="white", wrap="word"
        )
        self.chat_display.pack(expand=True, fill="both", padx=10, pady=5)

        self.chat_entry = tk.Entry(self.right_frame)
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        self.chat_send_button = tk.Button(
            self.right_frame, text="Envoyer", command=self.send_to_chatbot
        )
        self.chat_send_button.pack(side="right", padx=10, pady=5)

    def show_table_data(self, event):
        selected_table = self.table_combobox.get()
        columns, rows = self.db_manager.fetch_all(selected_table)

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        for row in rows:
            self.tree.insert("", "end", values=row)

    def insert_row(self):
        selected_table = self.table_combobox.get()
        if not selected_table:
            messagebox.showwarning("Alerte", "Veuillez sélectionner une table.")
            return

        columns, _ = self.db_manager.fetch_all(selected_table)
        if not columns:
            messagebox.showerror("Erreur", "Impossible de récupérer les colonnes pour cette table.")
            return

        editable_columns = [col for col in columns if col not in ("customer_id", "created_at", "id")]
        values = []
        for column in editable_columns:
            value = simpledialog.askstring("Insertion", f"Entrez la valeur pour {column} :")
            if value is None:
                return
            values.append(value)

        try:
            self.db_manager.insert_row(selected_table, editable_columns, values)
            messagebox.showinfo("Succès", "Ligne insérée avec succès.")
            self.show_table_data(None)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def edit_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Alerte", "Veuillez sélectionner une ligne à modifier.")
            return

        row_data = self.tree.item(selected_item)["values"]
        selected_table = self.table_combobox.get()
        columns = self.tree["columns"]
        editable_columns = [col for col in columns if col not in ("customer_id", "created_at", "id")]

        updates = {}
        for col in editable_columns:
            current_value = row_data[columns.index(col)]
            new_value = simpledialog.askstring(
                "Modification", f"Nouvelle valeur pour {col} (actuel : {current_value}):"
            )
            if new_value:
                updates[col] = new_value

        if updates:
            try:
                self.db_manager.update_row(selected_table, updates, columns[0], row_data[0])
                messagebox.showinfo("Succès", "Ligne mise à jour avec succès.")
                self.show_table_data(None)
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def delete_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Alerte", "Veuillez sélectionner une ligne à supprimer.")
            return

        row_data = self.tree.item(selected_item)["values"]
        selected_table = self.table_combobox.get()

        confirm = messagebox.askyesno(
            "Confirmation", f"Êtes-vous sûr de vouloir supprimer l'ID {row_data[0]} ?"
        )
        if confirm:
            try:
                self.db_manager.delete_row(selected_table, self.tree["columns"][0], row_data[0])
                messagebox.showinfo("Succès", "Ligne supprimée avec succès.")
                self.show_table_data(None)
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def send_to_chatbot(self):
        user_message = self.chat_entry.get()
        if not user_message.strip():
            messagebox.showwarning("Alerte", "Veuillez entrer un message.")
            return

        try:
            # Obtenir la réponse du bot via la classe ChatbotClient
            bot_response = chatbot_client.get_response(user_message)

            # Afficher le message utilisateur
            self.chat_display.config(state="normal")
            self.chat_display.insert(tk.END, f"Vous: {user_message}\n", "user")
            self.chat_display.tag_config("user", foreground="blue")  # Couleur pour l'utilisateur
            self.chat_entry.delete(0, tk.END)

            # Effet de saisie progressive
            def type_response():
                self.chat_display.config(state="normal")
                self.chat_display.insert(tk.END, "Bot: ", "bot")
                self.chat_display.tag_config("bot", foreground="green")  # Couleur pour le bot

                for char in bot_response:
                    self.chat_display.insert(tk.END, char, "bot")
                    self.chat_display.see(tk.END)  # Faire défiler automatiquement
                    time.sleep(0.03)  # Temps pour chaque caractère

                self.chat_display.insert(tk.END, "\n")  # Ajouter un saut de ligne après la réponse
                self.chat_display.config(state="disabled")

            # Utilisation d'un thread pour ne pas bloquer l'interface graphique
            threading.Thread(target=type_response).start()

        except RuntimeError as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


if __name__ == "__main__":
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'root'
    DATABASE = 'perfumery'

    db_manager = DatabaseManager(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    db_manager.connect()

    def on_login_success(username, role):
        root = tk.Tk()
        app = App(root, db_manager, username, role)
        root.mainloop()

    login_root = tk.Tk()
    login_app = LoginWindow(login_root, db_manager, on_login_success)
    login_root.mainloop()

    db_manager.close()

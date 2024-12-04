import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("Connexion à MySQL réussie.")
        except mysql.connector.Error as err:
            print(f"Erreur lors de la connexion : {err}")
            raise

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connexion MySQL fermée.")

    def fetch_all(self, table):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return columns, results
        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return [], []

    def check_user_credentials(self, username, password):
        try:
            cursor = self.connection.cursor()
            query = "SELECT role FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as e:
            print(f"Erreur lors de la vérification des identifiants : {e}")
            return None

    def insert_row(self, table, columns, values):
        """
        Insère une nouvelle ligne dans la table.
        :param table: Nom de la table.
        :param columns: Liste des colonnes à remplir.
        :param values: Liste des valeurs correspondantes.
        """
        try:
            col_names = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Insertion réussie.")
        except mysql.connector.Error as e:
            print(f"Erreur lors de l'insertion : {e}")
            raise

    def update_row(self, table, updates, condition_column, condition_value):
        """
        Met à jour une ligne existante dans la table.
        :param table: Nom de la table.
        :param updates: Dictionnaire {colonne: nouvelle_valeur}.
        :param condition_column: Colonne de condition (souvent ID).
        :param condition_value: Valeur de la condition.
        """
        try:
            set_clause = ', '.join([f"{col} = %s" for col in updates.keys()])
            values = list(updates.values()) + [condition_value]
            query = f"UPDATE {table} SET {set_clause} WHERE {condition_column} = %s"
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Mise à jour réussie.")
        except mysql.connector.Error as e:
            print(f"Erreur lors de la mise à jour : {e}")
            raise

    def delete_row(self, table, condition_column, condition_value):
        """
        Supprime une ligne de la table.
        :param table: Nom de la table.
        :param condition_column: Colonne de condition (souvent ID).
        :param condition_value: Valeur de la condition.
        """
        try:
            query = f"DELETE FROM {table} WHERE {condition_column} = %s"
            cursor = self.connection.cursor()
            cursor.execute(query, (condition_value,))
            self.connection.commit()
            print("Suppression réussie.")
        except mysql.connector.Error as e:
            print(f"Erreur lors de la suppression : {e}")
            raise


from openai import OpenAI
import os
import mysql.connector


class ChatbotClient:
    def __init__(self, api_key=None):
        """
        Initialise le client OpenAI avec la clé API.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("La clé API OpenAI est manquante.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"
        self.messages = []

    def get_response(self, user_message):
        """
        Envoie un message à OpenAI et retourne la réponse.
        :param user_message: Message de l'utilisateur
        :param model: Modèle OpenAI à utiliser
        :return: Réponse du chatbot
        """

        nv_message = {"role": "user", "content": user_message}
        self.messages.append(nv_message)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            bot_response = response.choices[0].message.content.strip()
            nv_reponse = {"role": "user", "content": bot_response}
            self.messages.append(nv_reponse)

            return bot_response
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la communication avec OpenAI : {e}")


    def retrieval_amplified_generation(self):
        """
        Récupère les données des produits depuis la base de données et génère des recommandations.
        """
        # Connexion à la base de données
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            raise RuntimeError(f"Erreur lors de la connexion à la base de données : {err}")

        # Transformation des données pour le modèle OpenAI
        product_details = "\n".join(
            [f"Nom: {p['product_name']}, Description: {p['product_description']}, Prix: {p['product_price']}€"
             for p in products]
        )

        # Message pour le modèle OpenAI
        prompt = (
            "Voici la liste des produits disponibles chez notre compagnie :\n\n"
            f"{product_details}\n\n"
            "Pouvez-vous recommander certains produits à un client qui cherche quelque chose de spécial ?"
        )

        # Interaction avec OpenAI
        try:
            response = self.get_response(prompt)
            return response
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la génération des recommandations : {e}")


import os
from dotenv import load_dotenv

import json

load_dotenv()

class Assistant:

    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_model = "chatgpt4o-mini"

        # Récupérer les fonctions possibles :
        with open("tools.json", "r") as file:
            self.tools = json.load(file)

        print(self.tools)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    assistant = Assistant()



import logging
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_market(content: str):
    if not content:
        return {"error": "Aucun contenu fourni."}

    try:
        logging.info("Analyse de marché en cours...")

        prompt = f"""
        Tu es un analyste expert en étude de marché.
        À partir des informations ci-dessous, rédige une analyse du marché :

        {content}

        Structure attendue :
        1. Structure du marché
        2. Tendances économiques et technologiques
        3. Réglementation et évolutions ESG
        4. Évolutions récentes et perspectives futures

        Rédige de manière analytique, claire et professionnelle.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse de marché."},
                {"role": "user", "content": prompt}
            ]
        )

        return {"market_analysis": response.choices[0].message.content}

    except Exception as e:
        logging.error(f"Erreur analyse marché : {e}")
        return {"error": str(e)}

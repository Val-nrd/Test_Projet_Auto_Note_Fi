from fastapi import APIRouter
import logging
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

router = APIRouter()
logging.basicConfig(level=logging.INFO)

@router.post("/analyze_company/")
async def analyze_company(content: str = None):
    if not content:
        return {"error": "Aucun contenu fourni."}

    try:
        logging.info("Appel à l'API OpenAI pour l'analyse de l'entreprise...")

        prompt = f"""
        Tu es un expert en stratégie d'entreprise.
        À partir du texte ci-dessous, rédige une fiche complète de présentation de l'entreprise :

        {content}

        Structure attendue :
        1. Historique et grandes étapes
        2. Philosophie et mission
        3. Organisation interne (dirigeants, départements, effectifs)
        4. Ressources clés (machines, outils, infrastructures)

        Rédige de manière claire, concise, professionnelle.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un analyste d'entreprise."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        logging.error(f"Erreur lors de l'analyse de l'entreprise : {e}")
        return {"error": str(e)}


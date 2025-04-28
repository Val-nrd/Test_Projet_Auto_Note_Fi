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

@router.post("/analyze_competition/")
async def analyze_competition(content: str = None):
    if not content:
        return {"error": "Aucun contenu fourni."}

    try:
        logging.info("Appel à OpenAI pour analyse concurrentielle...")

        prompt = f"""
        Tu es un expert en stratégie concurrentielle.
        Rédige une analyse concurrentielle basée sur ce contenu :

        {content}

        Structure attendue :
        1. Principaux concurrents directs et indirects
        2. Avantages et faiblesses comparatives
        3. Menaces potentielles
        4. Opportunités stratégiques

        Sois structuré, professionnel et factuel.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en stratégie d'entreprise."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        logging.error(f"Erreur analyse concurrence : {e}")
        return {"error": str(e)}


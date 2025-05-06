from fastapi import FastAPI, File, UploadFile
from typing import List
from pydantic import BaseModel
import os
import shutil
import logging
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

# 🔐 Environnement et client OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# 📦 Import des fonctions d'extraction
from utils.file_extraction import (
    extract_text_from_pdf,
    extract_text_from_word,
    extract_data_from_excel,
    extract_all_uploaded_content,
)

# 📦 Import des agents
from agents.analyze_company import analyze_company
from agents.analyze_market import analyze_market
from agents.analyze_competition import analyze_competition

# 🚀 FastAPI App
app = FastAPI()

# 🌐 CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📁 Répertoire d’upload
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 📋 Logger
logging.basicConfig(level=logging.INFO)

# 🏠 Route racine
@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API d'automatisation de rapports financiers"}

# 📤 Upload de fichiers multiples avec suppression des anciens
@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    # 🔁 Suppression des anciens fichiers
    for f in os.listdir(UPLOAD_DIR):
        try:
            os.remove(os.path.join(UPLOAD_DIR, f))
            logging.info(f"✅ Fichier supprimé : {f}")
        except Exception as e:
            logging.warning(f"❌ Erreur suppression fichier {f} : {e}")

    extraits = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logging.info(f"Fichier uploadé : {file.filename}")

        if file.filename.endswith(".pdf"):
            extrait = extract_text_from_pdf(file_path)
        elif file.filename.endswith((".xlsx", ".xls")):
            extrait = {"texte": str(extract_data_from_excel(file_path))}
        elif file.filename.endswith(".docx"):
            extrait = {"texte": extract_text_from_word(file_path)}
        else:
            extrait = {"texte": f"Format non supporté : {file.filename}"}

        extrait["filename"] = file.filename
        extraits.append(extrait)

    return {
        "message": f"{len(extraits)} fichier(s) traité(s)",
        "extraits": extraits
    }

# 📊 Analyse du marché
@app.post("/analyze_market/")
async def analyze_market_endpoint():
    content = extract_all_uploaded_content()
    if not content:
        return {"error": "Aucun contenu valide à analyser."}
    result = await analyze_market(content)
    return {"message": "Analyse du marché effectuée", "result": result}

# 🏢 Analyse d'entreprise
@app.post("/analyze_company/")
async def analyze_company_endpoint():
    content = extract_all_uploaded_content()
    if not content:
        return {"error": "Aucun contenu valide à analyser."}
    result = await analyze_company(content)
    return {"message": "Présentation de l'entreprise générée avec succès", "company_analysis": result}

# ⚔️ Analyse concurrentielle
@app.post("/analyze_competition/")
async def analyze_competition_endpoint():
    content = extract_all_uploaded_content()
    if not content:
        return {"error": "Aucun contenu valide à analyser."}
    result = await analyze_competition(content)
    return {"message": "Analyse concurrentielle générée avec succès", "competition_analysis": result}

# 💬 Classe pour le chatbot
class ChatRequest(BaseModel):
    message: str

@app.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse financière."},
                {"role": "user", "content": request.message},
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        logging.error(f"Erreur OpenAI : {e}")
        return {"response": f"Erreur backend : {str(e)}"}

@app.post("/analyze_all/")
async def analyze_all_endpoint():
    try:
        content = extract_all_uploaded_content()
        if not content:
            return {"error": "Aucun contenu trouvé pour analyse."}

        # Appels aux 3 agents
        company_result = await analyze_company(content)
        market_result = analyze_market(content)
        competition_result = await analyze_competition(content)

        return {
            "message": "Analyse complète générée avec succès",
            "entreprise": company_result,
            "marche": market_result.get("market_analysis", ""),
            "concurrence": competition_result
        }

    except Exception as e:
        logging.error(f"Erreur analyse complète : {e}")
        return {"error": f"Erreur analyse complète : {str(e)}"}


# 📄 Rapport complet
def generate_report(content):
    try:
        logging.info("Génération du rapport avec OpenAI...")

        max_chars = 5000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n[Contenu tronqué...]"

        prompt = f"""
        Rédige un rapport structuré basé sur les informations suivantes :

        {content}

        Structure attendue :
        1. **Résumé Exécutif**
        2. **Présentation de l'Entreprise**
        3. **Analyse Financière**
        4. **Analyse du Marché**
        5. **Conclusion**

        Rédige de manière analytique et professionnelle.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un analyste financier."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Erreur génération rapport : {e}")
        return {"error": str(e)}

@app.post("/generate_report/")
async def generate_report_endpoint():
    content = extract_all_uploaded_content()
    if not content:
        return {"error": "Aucun contenu trouvé pour générer le rapport."}
    report = generate_report(content)
    return {"message": "Rapport généré avec succès", "report": report}










import fitz  # PyMuPDF pour PDF
import pandas as pd
import numpy as np
import docx
import logging
import os

logging.basicConfig(level=logging.INFO)

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        extracted_text = [page.get_text("text").strip() for page in doc]
        full_text = "\n\n".join(extracted_text)
        return {"texte": full_text[:5000]}  # limite pour éviter surcharge API
    except Exception as e:
        logging.error(f"Erreur d'extraction PDF : {e}")
        return {"error": str(e)}

def extract_data_from_excel(excel_path):
    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
        df = df.dropna(how="all", axis=1).dropna(how="all")
        df.columns = [str(c).strip() for c in df.columns]
        df.rename(columns={"Unnamed: 0": "Libellé"}, inplace=True, errors="ignore")
        df.drop(columns=["Unnamed: 1"], inplace=True, errors="ignore")
        df = df.replace({np.nan: "null", np.inf: "Infinity", -np.inf: "-Infinity"})
        if len(df.columns) > 1:
            df.rename(columns={df.columns[1]: "Valeur"}, inplace=True, errors="ignore")
        df = df[df["Libellé"] != "null"]
        return df.head().to_dict(orient="records")
    except Exception as e:
        logging.error(f"Erreur d'extraction Excel : {e}")
        return {"error": str(e)}

def extract_text_from_word(word_path):
    try:
        doc = docx.Document(word_path)
        full_text = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
        return full_text[:1000]
    except Exception as e:
        logging.error(f"Erreur d'extraction Word : {e}")
        return {"error": str(e)}

def extract_all_uploaded_content(upload_dir="uploaded_files"):
    all_content = ""
    for filename in os.listdir(upload_dir):
        path = os.path.join(upload_dir, filename)
        if filename.endswith(".pdf"):
            all_content += extract_text_from_pdf(path).get("texte", "") + "\n\n"
        elif filename.endswith((".xlsx", ".xls")):
            all_content += str(extract_data_from_excel(path)) + "\n\n"
        elif filename.endswith(".docx"):
            all_content += extract_text_from_word(path) + "\n\n"
    return all_content.strip()

import os
from datetime import datetime
from time import sleep
import requests
from PyPDF2 import PdfReader

TARGET_KEYWORDS = ["I-140", "Extraordinary Ability"]
DOWNLOAD_DIR = "./aao_docs"

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text
    except Exception:
        return ""

def download_and_parse_documents(links):
    documents = []
    for i, link in enumerate(links):
        filename = os.path.join(DOWNLOAD_DIR, f"doc_{i}.pdf")
        try:
            r = requests.get(link, timeout=10)
            r.raise_for_status()
            if r.headers.get("content-type") == "application/pdf":
                with open(filename, "wb") as f:
                    f.write(r.content)
                text = extract_text_from_pdf(filename)
                if text.strip() and any(kw.lower() in text.lower() for kw in TARGET_KEYWORDS):
                    documents.append({
                        "source": link,
                        "filename": filename,
                        "text": text,
                        "date": str(datetime.now().date())
                    })
        except requests.RequestException:
            pass
        sleep(1)
    return documents

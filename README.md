# Legal RAG System – USCIS I-140 AAO Decisions
This project is part of an AI internship homework to build a Retrieval-Augmented Generation (RAG) pipeline for processing USCIS Administrative Appeals Office (AAO) non-precedent decisions.

# Project Goal
Build a pipeline that:
-Crawls USCIS AAO non-precedent decisions published in February 2025
-Filters for I-140 Extraordinary Ability cases
-Extracts clean text from PDFs
-Stores them in a vector database
-Uses an LLM (Gemini) to answer legal research questions with source citations

# Technologies Used
-Python
-Selenium – Web crawling
-BeautifulSoup – HTML parsing
-PyPDF2 – PDF parsing
-SentenceTransformers – Embeddings
-FAISS or ChromaDB – Vector database
-Google Generative AI (Gemini) – LLM for answering questions

# How to Run
'''python 
pip install -r requirements.txt
'''
'''python
python main.py
'''
Make sure to:
-Replace the Gemini API key in the code.
-Run ChromeDriver compatible with your Chrome version.

# Example Query
"How is peer review service evaluated in recent AAO decisions?"


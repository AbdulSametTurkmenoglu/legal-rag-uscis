import os
import google.generativeai as genai
from vector_store import collection

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "test-api-key"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def answer_query(query):
    try:
        results = collection.query(query_texts=[query], n_results=3)
        context = "\n\n".join([doc for doc in results["documents"][0] if doc.strip()])
        if not context:
            return "[ANSWER] No relevant context found."

        prompt = f"""
You are a legal assistant. Use the context from the USCIS decisions below to answer the question. 
Ensure your answer is accurate, clear, and includes source links:

Context:
{context}

Question:
{query}
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "[ANSWER] Failed to process query."

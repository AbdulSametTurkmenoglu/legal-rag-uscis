import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()
model_name = "all-MiniLM-L6-v2"
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)

try:
    collection = chroma_client.create_collection(name="aao_legal", embedding_function=embedding_function)
except:
    collection = chroma_client.get_collection(name="aao_legal", embedding_function=embedding_function)

def index_documents(documents):
    for i, doc in enumerate(documents):
        try:
            chunks = [doc["text"][j:j + 512] for j in range(0, len(doc["text"]), 512)]
            for k, chunk in enumerate(chunks):
                if chunk.strip():
                    doc_id = f"doc_{i}_{k}"
                    collection.add(
                        documents=[chunk],
                        metadatas=[{"source": doc["source"], "date": doc["date"]}],
                        ids=[doc_id]
                    )
        except Exception:
            continue

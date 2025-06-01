from scraper import crawl_and_filter_links
from parser import download_and_parse_documents
from vector_store import index_documents
from rag_pipeline import answer_query

if __name__ == "__main__":
    links = crawl_and_filter_links()
    if links:
        docs = download_and_parse_documents(links)
        if docs:
            index_documents(docs)
            print(answer_query("How is peer review service evaluated in recent AAO decisions?"))

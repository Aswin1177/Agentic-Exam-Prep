from RAG.loader import load_printed_pdf
from RAG.splitter import doc_splitter
from RAG.embeddings import get_embeddings
import os
embeddings=get_embeddings()
file_path="qpaper_store/qpprs.txt"
def pyq_retriever(files):
    pages = load_printed_pdf(files)
    return "\n\n".join(pages)
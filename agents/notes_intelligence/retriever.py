from RAG.loader import load_pdf
from RAG.splitter import doc_splitter
from RAG.embeddings import get_embeddings
from RAG.vector_store import create_vectorstore,load_vectorstore,get_retriever
import os
embeddings=get_embeddings()
def notes_retriever():
    if not os.path.exists("faiss_index"):
        pages=load_pdf("notes.pdf")
        chunks=doc_splitter(pages)
        vector_store=create_vectorstore(chunks,embeddings)
        retriever=get_retriever(vector_store,k=3)
        return retriever
    else:
        vector_store=load_vectorstore("faiss_index",embeddings)
        retriever=get_retriever(vector_store,k=3)
        return retriever
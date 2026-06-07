from RAG.loader import load_printed_pdf
from RAG.splitter import doc_splitter
from RAG.embeddings import get_embeddings
from RAG.vector_store import create_vectorstore,save_vectorstore,load_vectorstore,get_retriever
import os
file_path="vectorstores/notes_index"
def notes_retriever(files, handwritten=False):
    embeddings = get_embeddings()
    if not os.path.exists(file_path):
        if handwritten:
            raise NotImplementedError("Handwritten notes not implemented yet")
        pages = load_printed_pdf(files)
        chunks = doc_splitter(pages)
        vector_store = create_vectorstore(chunks, embeddings)
        save_vectorstore(vector_store,file_path)
        return get_retriever(vector_store,k=5)
    else:
        vector_store = load_vectorstore(file_path,embeddings)
        return get_retriever(vector_store,k=5)

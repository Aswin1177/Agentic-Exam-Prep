from langchain_community.vectorstores import FAISS

def create_vectorstore(chunks,embeddings):
    vector_store=FAISS.from_documents(documents=chunks,embedding=embeddings)
    vector_store.save_local("faoss_index")
    print("Vector Store has been Created")
    return vector_store

def load_vectorstore(embeddings):
    return FAISS.load_local("faiss_index",embeddings)

def get_retriever(vector_store,k):
    return vector_store.as_retriever(search_kwargs={"k":k})
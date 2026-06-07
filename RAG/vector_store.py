from langchain_community.vectorstores import FAISS

def create_vectorstore(chunks,embeddings):
    vector_store=FAISS.from_documents(documents=chunks,embedding=embeddings)
    print("Vector Store has been Created")
    return vector_store

def save_vectorstore(vector_store,file_name):
     vector_store.save_local(file_name)

def load_vectorstore(file_path,embeddings):
    return FAISS.load_local(file_path,embeddings,allow_dangerous_deserialization=True)

def get_retriever(vector_store,k):
    return vector_store.as_retriever(search_kwargs={"k":k})

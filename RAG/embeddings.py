from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-miniLM-L6-V2")
    return embeddings
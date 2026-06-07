from langchain_text_splitters import RecursiveCharacterTextSplitter
def doc_splitter(pages):
    pages=[page for page in pages if page.strip()]
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    chunks=splitter.create_documents(pages)
    print("Splitted into chunks of length: 1000")
    return chunks
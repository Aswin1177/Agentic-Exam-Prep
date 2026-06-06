class RAGPipeline:
    def __init__(self,retriever,llm):
        self.retriever=retriever
        self.llm=llm
    
    def retrieve_context(self,query):
        docs=self.retriever.invoke(query)
        return "\n\n".join(doc.page_content for doc in docs)
    
    def answer(self, query):
            context = self.retrieve_context(query)
            prompt = f"""
            Answer using only the provided context.
            Context:
            {context}
            Question:
            {query}
            """
            response = self.llm.invoke(prompt)
            return response.content
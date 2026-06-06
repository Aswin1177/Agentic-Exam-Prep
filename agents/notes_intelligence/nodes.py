
def create_retrieve_node(retriever):
    def retrieve_node(state):
        docs = retriever.invoke(state["query"])
        context = "\n\n".join(doc.page_content for doc in docs)
        return {"context": context}
    return retrieve_node

def create_answer_node(llm):
    def answer_node(state):
        prompt=f"""
        Answer using only the provided context.

        Context:

        {state["context"]}

        Question:

        {state["query"]}

        """
        response=llm.invoke(prompt)
        return {
            "answer": f"Answering: {response.content}"
        }
    return answer_node
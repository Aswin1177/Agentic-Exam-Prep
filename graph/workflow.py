from langgraph.graph import StateGraph, START, END
from .state import ExamState
from agents.notes_intelligence.nodes import create_retrieve_node, create_answer_node
from agents.notes_intelligence.retriever import notes_retriever
from RAG.llm import get_llm
llm=get_llm()
retriever=notes_retriever()
retriever_node=create_retrieve_node(retriever)
answer_node=create_answer_node(llm)
graph_builder = StateGraph(ExamState)
graph_builder.add_node("retriever",retriever_node)
graph_builder.add_node("generate_answer", answer_node)

graph_builder.add_edge(START, "retriever")

graph_builder.add_edge("retriever","generate_answer")

graph_builder.add_edge("generate_answer", END)

graph = graph_builder.compile()

result = graph.invoke({"query": "What is an algorithm?"})

print(result["answer"])
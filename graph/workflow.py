from langgraph.graph import StateGraph, START, END
from .state import ExamState
from agents.notes_intelligence.nodes import create_retrieve_node, create_answer_node
from agents.notes_intelligence.retriever import notes_retriever
from agents.pyq_intelligence.nodes import create_pyq_load_node, create_question_expansion_node, create_topic_analysis_node
from agents.pyq_intelligence.extractor import pyq_retriever
from RAG.llm import get_llm

def run_workflow(qppr_files, notes_files, handwritten=False):

    llm = get_llm()

    pyq_content = pyq_retriever(qppr_files)
    pyq_retriever_node = create_pyq_load_node(pyq_content)
    q_expansion_node = create_question_expansion_node(llm)
    analysis_node = create_topic_analysis_node(llm)

    retriever_notes = notes_retriever(notes_files, handwritten)
    notes_retriever_node = create_retrieve_node(retriever_notes)

    answer_node = create_answer_node(llm)

    graph_builder = StateGraph(ExamState)

    graph_builder.add_node("pyq_retriever", pyq_retriever_node)
    graph_builder.add_node("q_expansion", q_expansion_node)
    graph_builder.add_node("topic_analysis", analysis_node)
    graph_builder.add_node("retriever_notes", notes_retriever_node)
    graph_builder.add_node("generate_answer", answer_node)

    graph_builder.add_edge(START, "pyq_retriever")
    graph_builder.add_edge("pyq_retriever", "q_expansion")
    graph_builder.add_edge("q_expansion", "topic_analysis")
    graph_builder.add_edge("topic_analysis", "retriever_notes")
    graph_builder.add_edge("retriever_notes", "generate_answer")
    graph_builder.add_edge("generate_answer", END)

    graph = graph_builder.compile()

    return graph.invoke({})
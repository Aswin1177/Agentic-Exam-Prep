from langgraph.graph import StateGraph,START,END
from .state import ExamState
from agents.pyq_analyzer_agent.nodes import create_topic_frequency_node,create_pyq_load_node,create_question_expansion_node,create_topic_analysis_node
from agents.pyq_analyzer_agent.extractor import pyq_retriever
from agents.notes_generator_agent.nodes import create_retrieve_node,create_answer_node
from agents.notes_generator_agent.retriever import notes_retriever
from RAG.llm import get_llm

def run_notes_workflow(qppr_files,notes_files,handwritten=False):

    llm=get_llm()

    pyq_content=pyq_retriever(qppr_files)

    graph_builder=StateGraph(ExamState)

    graph_builder.add_node("pyq_retriever",create_pyq_load_node(pyq_content))
    graph_builder.add_node("q_expansion",create_question_expansion_node(llm))
    graph_builder.add_node("frequency_analysis",create_topic_frequency_node())
    graph_builder.add_node("topic_analysis",create_topic_analysis_node(llm))
    graph_builder.add_node("retriever_notes",create_retrieve_node(notes_retriever(notes_files,handwritten)))
    graph_builder.add_node("generate_answer",create_answer_node(llm))

    graph_builder.add_edge(START,"pyq_retriever")
    graph_builder.add_edge("pyq_retriever","q_expansion")
    graph_builder.add_edge("q_expansion","frequency_analysis")
    graph_builder.add_edge("frequency_analysis","topic_analysis")
    graph_builder.add_edge("topic_analysis","retriever_notes")
    graph_builder.add_edge("retriever_notes","generate_answer")
    graph_builder.add_edge("generate_answer",END)

    graph=graph_builder.compile()

    return graph.invoke({})
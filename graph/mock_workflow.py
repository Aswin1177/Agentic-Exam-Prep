from langgraph.graph import StateGraph,START,END
from .state import ExamState
from agents.pyq_analyzer_agent.nodes import create_pyq_load_node,create_question_expansion_node,create_topic_analysis_node
from agents.pyq_analyzer_agent.extractor import pyq_retriever
from agents.mock_examiner_agent.nodes import create_pattern_analysis_node,create_mock_generator_node,create_mock_formatter_node
from RAG.loader import load_printed_pdf
from RAG.llm import get_llm

def run_mock_workflow(qppr_files):

    llm=get_llm()

    reference_paper="\n".join(load_printed_pdf(qppr_files[0]))

    pyq_content=pyq_retriever(qppr_files)

    graph_builder=StateGraph(ExamState)

    graph_builder.add_node("pyq_retriever",create_pyq_load_node(pyq_content))
    graph_builder.add_node("q_expansion",create_question_expansion_node(llm))
    graph_builder.add_node("topic_analysis",create_topic_analysis_node(llm))
    graph_builder.add_node("pattern_analysis",create_pattern_analysis_node(llm))
    graph_builder.add_node("mock_generator",create_mock_generator_node(llm))
    graph_builder.add_node("mock_formatter",create_mock_formatter_node(llm))

    graph_builder.add_edge(START,"pyq_retriever")
    graph_builder.add_edge("pyq_retriever","q_expansion")
    graph_builder.add_edge("q_expansion","topic_analysis")
    graph_builder.add_edge("topic_analysis","pattern_analysis")
    graph_builder.add_edge("pattern_analysis","mock_generator")
    graph_builder.add_edge("mock_generator","mock_formatter")
    graph_builder.add_edge("mock_formatter",END)

    graph=graph_builder.compile()

    return graph.invoke({
        "reference_paper":reference_paper
    })
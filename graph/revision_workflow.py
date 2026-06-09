from langgraph.graph import StateGraph,START,END
from .state import ExamState

from agents.pyq_analyzer_agent.nodes import (create_topic_frequency_node,create_pyq_load_node,
    create_question_expansion_node, create_topic_analysis_node)

from agents.pyq_analyzer_agent.extractor import pyq_retriever

from agents.revision_planner_agent.nodes import (create_syllabus_load_node,
    create_syllabus_analyzer_node, create_revision_planner_agent_node)

from RAG.llm import get_llm


def run_revision_workflow(qppr_files,syllabus_file,days_to_exam,hours_per_day):

    llm=get_llm()

    pyq_content=pyq_retriever(qppr_files)

    graph_builder=StateGraph(ExamState)

    graph_builder.add_node("pyq_retriever",create_pyq_load_node(pyq_content))
    graph_builder.add_node("q_expansion",create_question_expansion_node(llm))
    graph_builder.add_node("frequency_analysis",create_topic_frequency_node())
    graph_builder.add_node("topic_analysis",create_topic_analysis_node(llm))

    graph_builder.add_node("load_syllabus",create_syllabus_load_node())
    graph_builder.add_node("analyze_syllabus",create_syllabus_analyzer_node(llm))

    graph_builder.add_node(
        "revision_planner_agent",
        create_revision_planner_agent_node(llm)
    )

    graph_builder.add_edge(START,"pyq_retriever")
    graph_builder.add_edge("pyq_retriever","q_expansion")
    graph_builder.add_edge("q_expansion","frequency_analysis")
    graph_builder.add_edge("frequency_analysis","topic_analysis")
    graph_builder.add_edge("topic_analysis","load_syllabus")
    graph_builder.add_edge("load_syllabus","analyze_syllabus")
    graph_builder.add_edge("analyze_syllabus","revision_planner_agent")

    graph_builder.add_edge("revision_planner_agent",END)

    graph=graph_builder.compile()

    return graph.invoke({
        "syllabus_file":syllabus_file,
        "days_to_exam":days_to_exam,
        "hours_per_day":hours_per_day
    })
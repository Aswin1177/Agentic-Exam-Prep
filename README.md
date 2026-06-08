Exam Prep AI

Exam Prep AI is a multi-agent exam preparation platform built using LangGraph, Groq LLMs, Retrieval-Augmented Generation (RAG), and Streamlit.

The system analyzes Previous Year Question Papers (PYQs), study notes, and syllabus documents to generate focused study notes, personalized revision plans, and realistic mock examination papers.

Features

Focused Notes Generation

Inputs:
- Previous Year Question Papers (PDF)
- Notes PDFs

Capabilities:
- Extracts and analyzes exam questions
- Identifies important topics
- Retrieves relevant content using RAG
- Generates concise exam-oriented notes

Generated Notes Include:
- Definitions
- Key Points
- Important Features
- Advantages and Disadvantages
- Common Exam Questions
- 5-Mark Answers
- 10-Mark Answers
- Missing Important Topics
- Partially Covered Topics

Output:
Focused_Notes.pdf

Intelligent Revision Planner

Inputs:
- Previous Year Question Papers
- Syllabus PDF
- Days until exam
- Available study hours per day

Capabilities:
- Analyzes PYQ trends
- Identifies frequently asked topics
- Analyzes syllabus modules and course outcomes
- Determines topic priorities
- Creates a personalized revision schedule

Generated Revision Plan Includes:
- High Priority Topics
- Medium Priority Topics
- Low Priority Topics
- Day-wise Revision Schedule
- Final Revision Strategy

Output:
Revision_Plan.pdf

Mock Examiner

Inputs:
- Previous Year Question Papers

Capabilities:
- Learns question paper structure
- Identifies marks distribution
- Understands question patterns
- Analyzes difficulty progression
- Generates realistic mock examinations

Generated Mock Paper:
- Preserves exam structure
- Preserves marks distribution
- Preserves question style
- Generates entirely new questions

Output:
Mock_Test_Paper.pdf

Agent Architecture

PYQ Analyzer Agent

Responsibilities:
- Load question papers
- Expand and normalize questions
- Extract important topics

Nodes:
- PYQ Loader Node
- Question Expansion Node
- Topic Analysis Node

Outputs:
- Expanded Questions
- Important Topics

Notes Generator Agent

Responsibilities:
- Retrieve relevant content from notes
- Generate focused study notes

Nodes:
- Retrieval Node
- Notes Generation Node

Outputs:
- Focused Notes

Revision Planner Agent

Responsibilities:
- Analyze syllabus
- Prioritize topics
- Generate revision schedules

Nodes:
- Syllabus Loader Node
- Syllabus Analyzer Node
- Revision Planner Node

Outputs:
- Revision Plan

Mock Examiner Agent

Responsibilities:
- Learn paper patterns
- Generate mock examinations

Nodes:
- Pattern Analysis Node
- Mock Generator Node
- Mock Formatter Node

Outputs:
- Mock Question Paper

Workflows

Notes Workflow

PYQ Analysis → Topic Analysis → Notes Retrieval → Focused Notes Generation

Revision Workflow

PYQ Analysis → Topic Analysis → Syllabus Analysis → Revision Planning

Mock Test Workflow

PYQ Analysis → Topic Analysis → Pattern Analysis → Mock Question Generation → Paper Formatting

Guardrails

The project uses decorator-based guardrails to improve workflow reliability.

Implemented safeguards:
- Required state validation
- Output validation
- Automatic retry handling

Example decorators:
- require_keys()
- validate_output()
- retry()

Technology Stack

Languages and Frameworks:
- Python
- LangGraph
- Streamlit

LLM:
- Groq
- Llama 3.1

Retrieval:
- FAISS
- HuggingFace Embeddings

Document Generation:
- ReportLab

Project Structure

Exam_Prep_AI

agents
- pyq_analyzer_agent
- notes_generator_agent
- revision_planner_agent
- mock_examiner_agent

graph
- notes_workflow.py
- revision_workflow.py
- mock_workflow.py
- state.py

guardrails
- guardrails.py

RAG

uploads

vectorstores

pdf_generator.py

main.py

requirements.txt

Installation

git clone <repository-url>

cd Exam_Prep_AI

pip install -r requirements.txt

Run

streamlit run main.py

Future Enhancements

- Flashcard Generator Agent
- Viva Preparation Agent
- Difficulty Analyzer
- Spaced Repetition Planner
- LangSmith Integration
- Async Agent Execution
- Multi-Agent Collaboration

Author

Aswin Santhosh

B.Tech Computer Science and Engineering

Interests:
- Agentic AI
- Artificial Intelligence
- Machine Learning
- Python Development
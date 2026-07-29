from typing import TypedDict

class ExamState(TypedDict,total=False):

    pyq_text:str
    expanded_questions:str
    topic_frequency:str
    important_topics:str

    context:str
    focused_notes:str

    syllabus_file:str
    syllabus_text:str
    syllabus_summary:str

    days_to_exam:int
    hours_per_day:int

    revision_plan:str

    reference_paper:str
    paper_stats:str
    question_patterns:str
    draft_mock_test:str
    mock_validation_notes:str
    mock_test:str
from RAG.loader import load_printed_pdf
from guardrails.guardrails import require_keys,validate_output,retry

def create_syllabus_load_node():

    def syllabus_load_node(state):

        print("Executing Agent 3 - Revision Planner")

        pages=load_printed_pdf(state["syllabus_file"])

        return {
            "syllabus_text":"\n".join(pages)
        }

    return syllabus_load_node


def create_syllabus_analyzer_node(llm):

    @require_keys("syllabus_text")
    @validate_output("syllabus_summary")
    @retry()
    def syllabus_analyzer_node(state):

        prompt=f"""
        You are an academic syllabus analyzer.

        Syllabus:

        {state["syllabus_text"][:5000]}

        Extract:

        1. Modules
        2. Important Topics
        3. Course Outcomes
        4. Frequently emphasized concepts
        5. High weightage topics

        Return a concise study-oriented summary.

        Do not use markdown.
        """

        response=llm.invoke(prompt)

        summary=response.content

        if len(summary)<100:
            raise ValueError(
                "Syllabus summary appears incomplete"
            )

        return {
            "syllabus_summary":summary
        }

    return syllabus_analyzer_node


def create_revision_planner_agent_node(llm):

    @require_keys(
        "important_topics",
        "syllabus_summary",
        "days_to_exam",
        "hours_per_day"
    )
    @validate_output("revision_plan")
    @retry()
    def revision_planner_agent_node(state):

        prompt=f"""
        Important Topics From PYQs:

        {state["important_topics"]}

        Syllabus Summary:

        {state["syllabus_summary"]}

        Days Until Exam:

        {state["days_to_exam"]}

        Total Study Hours Per Day:

        {state["hours_per_day"]}

        Create:

        1. High Priority Topics
        2. Medium Priority Topics
        3. Low Priority Topics

        4. Day-wise hourly revision schedule

        5. Final revision phase

        Prioritize:
        - Topics appearing in PYQs
        - Topics emphasized in syllabus
        - High weightage modules

        Do not use markdown.
        """

        response=llm.invoke(prompt)

        plan=response.content

        if len(plan)<200:
            raise ValueError(
                "Revision plan appears incomplete"
            )

        return {
            "revision_plan":plan
        }

    return revision_planner_agent_node
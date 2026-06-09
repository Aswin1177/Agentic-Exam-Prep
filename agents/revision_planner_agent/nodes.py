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

        Available Study Hours Per Day:

        {state["hours_per_day"]}

        Task:

        Analyze the syllabus and PYQ trends and create a revision plan focused on maximizing exam performance.

        Create:

        1. HIGH PRIORITY TOPICS
        2. MEDIUM PRIORITY TOPICS
        3. LOW PRIORITY TOPICS

        For each topic provide:

        - Topic Name
        - Study Time
        - Why Important

        Prioritize:

        - Frequently appearing PYQ topics
        - High-weightage syllabus topics
        - Core concepts that support multiple topics
        - Topics that are likely to appear in the examination

        Rules:

        1. Do NOT create a timetable.
        2. Do NOT create day-wise schedules.
        3. Do NOT create hourly slots.
        4. Do NOT generate dates.
        5. Do NOT generate calendars.
        6. Do NOT use markdown.
        7. Do NOT use:
        *, **, #, ##, ###, +, bullet symbols.
        8. Do NOT write text in ALL CAPITAL LETTERS.
        9. Use normal sentence case.
        10. Keep explanations concise and exam-oriented.
        11. Allocate more study time to high-priority topics.
        12. Allocate less study time to low-priority topics.
        13. Total study time should be realistic based on:

            Days Until Exam × Available Study Hours Per Day

        14. Display study time only as:

            8 Hours
            5 Hours
            2 Hours

        15. Do NOT write:

            Recommended Study Hours
            Suggested Hours
            Estimated Hours

        16. Every topic must contain:
            - Topic Name
            - Study Time
            - Why Important

        Output Format Example:

        High Priority Topics:
        ...
        Medium Priority Topics
        ...
        Low Priority Topics
        ...
        
        Day 1
        Dynamic Programming - 8 Hours

        Why Important:
        Frequently asked in PYQs and carries high exam weightage.

        Greedy Algorithm - 5 Hours

        Why Important:
        Core algorithm design topic and commonly appears in university examinations.

        Day 2
        Backtracking - 3 Hours

        Why Important:
        Frequently used for problem-solving questions.

        Randomized Algorithms - 1 Hour

        Why Important:
        Less frequently asked but useful for conceptual understanding.

        After the priority lists create:

        Final Revision Phase

        Last Week Before Exam

        - Topics that must be revised during the final week.

        Last 3 Days Before Exam

        - Topics that must be revised during the final three days.

        Day Before Exam

        - Topics that should receive a quick revision.

        Focus on:
        - High-priority topics
        - Frequently repeated PYQ concepts
        - Formulae
        - Algorithms
        - Important definitions

        Return only the final revision plan.
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
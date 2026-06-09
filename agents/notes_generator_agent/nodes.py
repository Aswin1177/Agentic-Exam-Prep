from guardrails.guardrails import require_keys,validate_output,retry

def create_retrieve_node(retriever):

    @require_keys("important_topics")
    @validate_output("context")
    def retrieve_node(state):

        topics=state["important_topics"].split("\n")

        all_docs=[]

        for topic in topics:

            if topic.strip():

                docs=retriever.invoke(topic)

                all_docs.extend(docs)

        context="\n\n".join(
            doc.page_content
            for doc in all_docs
        )

        return {
            "context":context[:5000]
        }

    return retrieve_node


def create_answer_node(llm):

    @require_keys("important_topics","context")
    @validate_output("focused_notes")
    @retry()
    def answer_node(state):

        prompt=f"""
        You are an expert university exam preparation assistant.

        Important Topics Extracted from Previous Year Question Papers:

        {state["important_topics"]}

        Retrieved Notes:

        {state["context"]}

        Task:

        Generate concise, exam-focused revision notes.

        Rules:

        1. Cover only topics found in Important Topics.
        2. Prioritize frequently asked concepts.
        3. Use information from Retrieved Notes.
        4. Avoid generic textbook explanations.
        5. Avoid repetition.
        6. Do not generate filler content.
        7. Do not invent information not supported by the Retrieved Notes.
        8. Do not generate Advantages/Disadvantages unless explicitly present in the Retrieved Notes.
        9. Do not create decorative headings.
        10. Do not write headings or content in ALL CAPITAL LETTERS.
        11. Use normal sentence case.
        12. Use numbered lists for steps or algorithms.
        13. Use concise bullet points only where necessary.
        14. Do not repeat information across sections.
        15. If a concept is already explained in Definition, do not repeat it in Key Exam Points.
        16. If a concept is already explained in Key Exam Points, do not repeat it in Quick Revision Summary.
        17. Skip any section that is not applicable to the topic.
        18. Focus on what is most useful for scoring marks in university examinations.
        19. Keep answers concise and revision-oriented.
        20. Do not use markdown.

        For each topic provide:

        Topic Name

        1. Definition
        - 2 to 3 concise lines

        2. Key Exam Points
        - 3 to 8 important points commonly asked in exams

        3. Important Steps / Algorithm
        - Include only if the topic naturally contains a procedure, algorithm, workflow, or method
        - Use numbered steps
        - Do not create generic software development steps

        4. Frequently Asked Questions
        - Generate at most 2 to 3 realistic university exam questions based on PYQ patterns

        5. Quick Revision Summary
        - 3 to 5 concise revision points

        Important:

        - Do not force every topic to have an algorithm section.
        - Do not force every topic to have diagrams.
        - Do not generate generic points such as:
        "Understand the problem"
        "Develop an algorithm"
        "Write the program"
        unless they genuinely belong to the topic.
        - Every section must contain topic-specific content.

        After generating notes, compare:

        Important Topics:

        {state["important_topics"]}

        Against:

        Retrieved Notes:

        {state["context"]}

        Then create:

        MISSING IMPORTANT TOPICS

        List topics that appear in Important Topics but are missing from the Retrieved Notes.

        For each provide:

        - Topic Name
        - Why Important
        - What To Study

        If none exist, write:

        "No important topics are missing."

        Then create:

        PARTIALLY COVERED TOPICS

        List topics that are present in Retrieved Notes but lack sufficient detail for exam preparation.

        For each provide:

        - Topic Name
        - Missing Areas
        - Suggested Areas To Study

        If none exist, write:

        "No partially covered topics."

        Return only the final notes.
        """

        response=llm.invoke(prompt)

        notes=response.content

        if len(notes)<500:
            raise ValueError(
                "Generated notes appear incomplete"
            )

        return {
            "focused_notes":notes
        }

    return answer_node
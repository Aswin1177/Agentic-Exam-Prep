
def create_retrieve_node(retriever):

    def retrieve_node(state):

        topics = state["important_topics"].split("\n")
        all_docs = []
        for topic in topics:
            if topic.strip():
                docs = retriever.invoke(topic)
                all_docs.extend(docs)
        context = "\n\n".join(doc.page_content for doc in all_docs)
        return {"context": context[:5000]}
    return retrieve_node

def create_answer_node(llm):

    def answer_node(state):

        prompt = f"""
        You are an expert exam preparation assistant.

        Important Topics Identified from Previous Year Question Papers:

        {state["important_topics"]}

        Retrieved Notes Context:

        {state["context"]}

        Generate highly focused exam preparation notes.

        Requirements:

        1. Cover only the important topics identified from PYQs.
        2. Prioritize concepts that appear frequently in exams.
        3. Include:

        - Definitions
        - Key Points
        - Important Features / Characteristics
        - Advantages and Disadvantages (if applicable)
        - Important Diagrams (describe where a diagram should be drawn)
        - Common Exam Questions
        - 5-Mark Answer
        - 10-Mark Answer

        4. Compare the important topics from PYQs against the retrieved notes context.

        5. Create a dedicated section titled:

        MISSING IMPORTANT TOPICS

        List all important topics that appear in PYQs but are not adequately covered in the notes.

        6. Create a dedicated section titled:

        PARTIALLY COVERED TOPICS

        List important topics that appear in the notes but need additional study.

        7. For every missing topic provide:
        - Topic Name
        - Why it is important for exams
        - Suggested areas to study

        8. Keep the notes concise, revision-oriented, and exam-focused.

        9. Use proper headings and bullet points.

        10. Do not mention that the content was generated from context.

        Output Format:

        IMPORTANT TOPICS

        DEFINITIONS

        KEY POINTS

        IMPORTANT FEATURES

        COMMON EXAM QUESTIONS

        5-MARK ANSWERS

        10-MARK ANSWERS

        MISSING IMPORTANT TOPICS

        PARTIALLY COVERED TOPICS
        """

        response = llm.invoke(prompt)

        return {
            "focused_notes": response.content
        }

    return answer_node
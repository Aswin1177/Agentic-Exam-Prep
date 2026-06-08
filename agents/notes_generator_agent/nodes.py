
def create_retrieve_node(retriever):

    def retrieve_node(state):
        print("EXECUTING AGENT 2 - Notes Generation")
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

        Output Format Rules:

        1. Every topic MUST start on a new line.

        Example:

        TRIAL AND ERROR METHOD

        Definition:

        The trial and error method is a ...

        Key Points:

        - Involves a lot of trial and..
        - Can be Time-Consuming ...

        Important Features:

        - Iterqative aproach to finding ...

        Advantages:
        
        ...
        [small letters only first letter of first word can be capital]

        Disadvantages:
        
        ...
        [small letters only first letter of first word can be capital]

        Common Exam Questions:
        ...
        [small letters only first letter of first word can be capital]

        5-Mark Answer:
        ...
        [small letters only first letter of first word can be capital]

        10-Mark Answer:
        ...
        [small letters only first letter of first word can be capital]
        
        2. Do NOT write topic names as bullet points.

        WRONG:

        • Trial and Error Method

        RIGHT:

        TRIAL AND ERROR METHOD

        3. Leave one blank line before and after every topic heading.

        4. Every topic heading must be UPPERCASE.

        5. Use ONLY these section labels:

        Definition:
        Key Points:
        Important Features:
        Advantages:
        Disadvantages:
        Common Exam Questions:
        5-Mark Answer:
        10-Mark Answer:

        6. At the end create:

        MISSING IMPORTANT TOPICS

        ...

        PARTIALLY COVERED TOPICS

        ...

        7. Never merge multiple topics under one heading.

        8. Do not use markdown.
        """

        response = llm.invoke(prompt)

        return {
            "focused_notes": response.content
        }

    return answer_node


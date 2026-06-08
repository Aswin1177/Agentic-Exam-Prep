from guardrails.guardrails import require_keys,validate_output,retry

def create_retrieve_node(retriever):

    @require_keys("important_topics")
    @validate_output("context")
    def retrieve_node(state):

        print("EXECUTING AGENT 2 - Notes Generation")

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
        You are an expert exam preparation assistant.

        Important Topics Identified from Previous Year Question Papers:

        {state["important_topics"]}

        Retrieved Notes Context:

        {state["context"]}

        Generate highly focused exam preparation notes.

        Requirements:

        1. Cover only the important topics identified from PYQs.
        2. Prioritize concepts that appear frequently in exams.

        Include:

        - Definitions
        - Key Points
        - Important Features
        - Advantages and Disadvantages
        - Important Diagrams
        - Common Exam Questions
        - 5-Mark Answer
        - 10-Mark Answer

        Compare PYQ topics against notes.

        Create:

        MISSING IMPORTANT TOPICS

        PARTIALLY COVERED TOPICS

        For every missing topic provide:
        - Topic Name
        - Why Important
        - Suggested Areas To Study

        Do not use markdown.
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
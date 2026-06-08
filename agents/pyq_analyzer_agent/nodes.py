def create_pyq_load_node(pyq_content):

    def pyq_load_node(state):
        print("EXECUTING AGENT 1 - Previous Year QPaper Analyser")
        return {
            "pyq_text": pyq_content
        }

    return pyq_load_node

def create_question_expansion_node(llm):

    def question_expansion_node(state):

       prompt=f"""
        Extract all exam questions from:

        {state["pyq_text"]}

        Remove duplicates.
        Rewrite similar questions into standardized exam questions.

        Return only the questions.
        """
       response = llm.invoke(prompt)

       return {
            "expanded_questions":
                response.content
        }

    return question_expansion_node

def create_topic_analysis_node(llm):

    def topic_analysis_node(state):

        prompt = prompt=f"""
        From these questions:

        {state["expanded_questions"]}

        Extract:
        - Concepts
        - Algorithms
        - Techniques
        - Problem solving methods

        Add semantically related topics useful for retrieval.

        Return one topic per line.
        """

        response = llm.invoke(prompt)

        return {
            "important_topics": response.content
        }

    return topic_analysis_node
from guardrails.guardrails import require_keys,validate_output,retry
from collections import Counter
import re

def create_pyq_load_node(pyq_content):

    def pyq_load_node(state):
        return {
            "pyq_text":pyq_content
        }

    return pyq_load_node


def create_question_expansion_node(llm):

    @require_keys("pyq_text")
    @validate_output("expanded_questions")
    @retry()
    def question_expansion_node(state):

        prompt=f"""
        Extract all exam questions from:

        {state["pyq_text"]}

        Remove duplicates.
        Rewrite similar questions into standardized exam questions.

        Return only the questions.
        """

        response=llm.invoke(prompt)

        return {
            "expanded_questions":response.content
        }

    return question_expansion_node

def create_topic_frequency_node():

    def topic_frequency_node(state):

        questions=state["expanded_questions"]
        words=re.findall(r"[A-Za-z]+",questions)

        stopwords={"what","is","the","and","of",
            "for","with","explain","describe",
            "write","note","short"}
        
        topics=[w.lower() for w in words
                
        if len(w)>3 and w.lower() not in stopwords]

        freq=Counter(topics)
        top_topics="\n".join(f"{k}:{v}" for k,v in freq.most_common(30))

        return {"topic_frequency":top_topics}
    
    return topic_frequency_node

def create_topic_analysis_node(llm):

    @require_keys("expanded_questions")
    @validate_output("important_topics")
    @retry()
    def topic_analysis_node(state):

        prompt=f"""
        From these questions:

        {state["expanded_questions"]}

        Topic Frequency Analysis:

        {state["topic_frequency"]}

        Extract ONLY syllabus topics.

        Rules:

        1. Output only topic names.

        2. A topic name must be 1-5 words.

        3. Do NOT output complete sentences.

        4. Do NOT output questions.

        5. Do NOT output statements.

        6. Do NOT output:
        - Advantages
        - Disadvantages
        - Features
        - Characteristics
        - Definitions
        - Learning outcomes
        - Example questions

        Examples:

        What is Dynamic Programming?
        → Dynamic Programming

        How do you use Backtracking to solve a problem?
        → Backtracking

        Backtracking can be time consuming.
        → Backtracking

        Choose locally optimal solution.
        → Greedy Algorithm

        Break problem into smaller sub-problems.
        → Divide and Conquer

        Output one topic per line.
        """

        response=llm.invoke(prompt)

        topics = []

        for line in response.content.split("\n"):
            line = line.strip()

            if len(line.split()) > 5:
                continue

            if "?" in line:
                continue

            topics.append(line)
        topics="\n".join(topics)
        if len([t for t in topics.split("\n") if t.strip()])<5:
            raise ValueError("Too few topics extracted")

        return {"important_topics": topics}

    return topic_analysis_node
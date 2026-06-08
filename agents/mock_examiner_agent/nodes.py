from guardrails.guardrails import require_keys,validate_output,retry

def create_pattern_analysis_node(llm):

    @require_keys("reference_paper")
    @validate_output("question_patterns")
    @retry()
    def pattern_analysis_node(state):

        print("Executing Agent 4 - Mock Examiner")

        prompt=f"""
        Reference Question Paper:

        {state["reference_paper"]}

        Analyze and extract:

        - Sections
        - Marks distribution
        - Question ordering
        - Difficulty progression
        - Frequently used question styles
        - Frequently used action verbs

        Return a structured paper pattern.
        """

        response=llm.invoke(prompt)

        patterns=response.content

        if len(patterns)<100:
            raise ValueError(
                "Question pattern analysis appears incomplete"
            )

        return {
            "question_patterns":patterns
        }

    return pattern_analysis_node


def create_mock_generator_node(llm):

    @require_keys(
        "question_patterns",
        "important_topics",
        "expanded_questions"
    )
    @validate_output("draft_mock_test")
    @retry()
    def mock_generator_node(state):

        prompt=f"""
        You are an experienced university examiner.

        Reference Paper Pattern:

        {state["question_patterns"]}

        Important Topics:

        {state["important_topics"]}

        Expanded Questions:

        {state["expanded_questions"]}

        Generate a completely new mock question paper.

        Rules:

        1. Follow the exact structure of the reference paper.

        2. Preserve:
           - Sections
           - Marks distribution
           - Question ordering
           - Difficulty progression

        3. Generate new questions using the expanded questions.

        4. Do NOT copy questions.

        5. Preserve the original question style.

        Examples:

        Original:
        Find GCD recursively.

        New:
        Find LCM recursively.

        Original:
        Check palindrome.

        New:
        Check Armstrong number.

        Original:
        Trace output of the following code.

        New:
        Trace output of a modified code snippet.

        Return the paper in plain text.
        Do not use markdown.
        Do not explain anything.
        """

        response=llm.invoke(prompt)

        draft=response.content

        if len(draft)<300:
            raise ValueError(
                "Generated mock paper appears incomplete"
            )

        return {
            "draft_mock_test":draft
        }

    return mock_generator_node


def create_mock_formatter_node(llm):

    @require_keys(
        "reference_paper",
        "draft_mock_test"
    )
    @validate_output("mock_test")
    @retry()
    def mock_formatter_node(state):

        prompt=f"""
        You are an expert university examination paper formatter.

        Reference Question Paper:

        {state["reference_paper"]}

        Generated Questions:

        {state["draft_mock_test"]}

        Task:

        Reconstruct the generated questions into a complete
        university-style question paper.

        Requirements:

        1. Follow the EXACT structure of the reference paper.

        2. Preserve:
           - Title
           - Course code
           - Course name
           - Instructions
           - Section names
           - Marks distribution
           - Question numbering
           - Internal choices
           - Module grouping
           - Layout

        3. Replace ONLY the question content.

        4. Do NOT copy questions from the reference paper.

        5. Ensure the generated questions fit naturally into
           the same structure.

        6. Output must be directly suitable for PDF generation.

        7. Return ONLY the final formatted question paper.

        Do not use markdown.
        """

        response=llm.invoke(prompt)

        paper=response.content

        if len(paper)<500:
            raise ValueError(
                "Final mock paper appears incomplete"
            )

        return {
            "mock_test":paper
        }

    return mock_formatter_node
from guardrails.guardrails import require_keys,validate_output,retry
import re

def create_pattern_statistics_node():

    def pattern_statistics_node(state):

        paper=state["reference_paper"]

        questions=re.findall(r"\n\d+\.",paper)

        marks=re.findall(r"\((\d+)\)",paper)

        sections=len(re.findall(r"PART\s+[A-Z]",paper,re.I))

        stats=f"""
        Sections: {sections}
        Questions: {len(questions)}
        Marks Distribution:
        {", ".join(marks)}
        """

        return {"paper_stats":stats}

    return pattern_statistics_node

def create_pattern_analysis_node(llm):

    @require_keys("reference_paper")
    @validate_output("question_patterns")
    @retry()

    
    def pattern_analysis_node(state):

        prompt=f"""
        Reference Question Paper:

        {state["reference_paper"]}

        Reference Paper Statistics:

       {state["paper_stats"]}

        Analyze and extract:

        - Total number of Sections, Questions
        - Mark Distribution
        - Section
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

        return {"question_patterns":patterns}

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

        Important Topics:

        {state["important_topics"]}

        Expanded Questions:

        {state["expanded_questions"]}

        Task:

        Generate ONLY new examination questions.

        Requirements:

        1. Generate fresh questions inspired by the expanded questions.

        2. Do NOT copy any question directly.

        3. Maintain the same academic difficulty level.

        4. Preserve the style of university examination questions.

        5. Generate enough questions to cover:
        - Part A
        - Part B
        - All modules

        6. Include internal choice questions where appropriate.

        7. Return ONLY question content.

        IMPORTANT:

        Do NOT generate:
        - PART A
        - PART B
        - Module headings
        - Course code
        - Course name
        - Instructions
        - Marks
        - Page numbers
        - Section titles

        Return only a numbered question bank.

        Example:

        Q1. ...

        Q2. ...

        Q3. ...

        ...

        Do not use markdown.
        Do not explain anything.
        """

        response=llm.invoke(prompt)

        draft=response.content

        if len(draft)<300:
            raise ValueError(
                "Generated mock paper appears incomplete"
            )

        return {"draft_mock_test":draft}

    return mock_generator_node


def create_mock_validation_node(llm):

    @require_keys(
        "draft_mock_test",
        "question_patterns"
    )
    @validate_output("mock_validation_notes")
    @retry()
    def mock_validation_node(state):

        prompt=f"""
        You are reviewing a draft mock examination question bank.

        Extracted Question Pattern:

        {state["question_patterns"]}

        Draft Question Bank:

        {state["draft_mock_test"]}

        Review the draft and provide a concise validation report that covers:
        - Section coverage
        - Question balance
        - Difficulty consistency
        - Internal choice suitability

        Return only the validation notes.
        """

        response=llm.invoke(prompt)

        validation_notes=response.content.strip()

        if len(validation_notes)<50:
            raise ValueError(
                "Mock validation notes appear too short"
            )

        return {"mock_validation_notes":validation_notes}

    return mock_validation_node


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

        Extracted Question Pattern:

        {state["question_patterns"]}

        Generated Question Bank:

        {state["draft_mock_test"]}

        Task:

        Create ONE complete mock examination paper by inserting questions from the Generated Question Bank into the structure of the Reference Question Paper.

        STRICT RULES:

        1. Treat the Reference Question Paper as the master template.

        2. Preserve EXACTLY:
        - Course code
        - Course name
        - Examination title
        - Instructions
        - PART A
        - PART B
        - Module names
        - Marks distribution
        - Question numbering
        - Internal choices
        - Number of questions
        - Section order

        3. Replace ONLY the question text.

        4. Every question must come from the Generated Question Bank.

        5. Do NOT copy any question from the Reference Question Paper.

        6. Generate exactly ONE question paper.

        7. There must be:
        - One PART A
        - One PART B
        - One occurrence of each module
        - One occurrence of each instruction section

        8. Do NOT:
        - Reorder modules
        - Reorder sections
        - Change question numbering
        - Change marks
        - Add new sections
        - Add new modules
        - Add page numbers
        - Add page breaks
        - Add explanations
        - Add notes
        - Add formatting symbols

        9. Verify before returning:
        - No duplicate PART A
        - No duplicate PART B
        - No duplicate module headings
        - No duplicate instructions
        - No duplicate course information

        10. The final structure must match the extracted question pattern.

        11. Output plain text only.

        12. Do not use:
        - Markdown
        - *
        - #
        - Bullet points
        - Bold text
        - Page numbers
        - "Page X of Y"
        - Decorative formatting

        13. Return only the final university examination paper exactly as a student would receive it.

        Final Validation:

        Before returning, compare the generated paper against the Extracted Question Pattern and ensure:

        - Same number of sections
        - Same number of modules
        - Same number of questions
        - Same marks distribution
        - Same internal choice structure

        Return only the final paper.
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

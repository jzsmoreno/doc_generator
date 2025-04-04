system_prompt = "You are an AI designed to provide direct answers to questions. Please respond only with the most accurate and concise answer, without any additional explanations, clarifications, or phrases."


def prompt_for_documentation(combined_content, context, tables_info):
    prompt = """
    **Instructions**: Below is the content of a Jupyter Notebook in markdown and code format. Your task is to create clear and structured documentation that covers the purpose, methodology, analysis, results, and conclusions of the notebook. Organize it into the following sections:

        1. **Introduction**: Briefly describe the main goal of the notebook.
        2. **Methodology**: Summarize the key steps and processes followed.
        3. **Analysis and Results**: Outline the analysis and results obtained, including references to any tables. Include the tables exactly as they are in the `tables_info` section.
        4. **Conclusions**: Provide any applicable conclusions.

        **Considerations**:
        - Use clear, simple language and avoid excessive code details.
        - **Incorporate the provided tables exactly as they are** into the analysis and results section. Ensure the tables are clearly referenced and interpreted where necessary.
        - Structure the output in **Markdown** format, using appropriate headings, lists, and bold text for clarity.
        - Ensure the **`tables_info`** provided is included exactly as it appears, without altering their format or content.

        **Input**: Below is the markdown and code content of the Jupyter Notebook:

        {combined_content}

        Context for the notebook:

        {context}

        Below is the `tables_info` extracted from the code (these tables should be included exactly as they are):

        {tables_info}

        **Expected output**: A well-organized **Markdown** document explaining the notebook, ensuring that all tables mentioned in `tables_info` are included exactly as they are in the analysis and conclusions.
    """
    return prompt.format(
        combined_content=combined_content, context=context, tables_info=tables_info
    )


def prompt_for_add_comments(code):
    prompt = """
    Task: Add brief comment to the following Python code explaining its function.

        Replace unnecessary lines with a comment like:

        `# The functionality is explained above.`

        If any line is commented out, explain why concisely. Output only the code with comments no additional information.

        Here is the code to modify:

        {code}
    """
    return prompt.format(code=code)


def prompt_for_table_creation(code):
    prompt = (
        prompt
    ) = """
    Task: Analyze the following Python code and extract details about the **metrics validation** steps. Specifically, identify the following:

    - **Metric**: Metrics being evaluated (e.g., accuracy, F1 score, AUC).
    - **Threshold**: Thresholds or criteria (e.g., precision > 0.8, recall > 0.75).
    - **Outcome**: Expected result or performance (e.g., acceptable accuracy or precision).
    - **Notes**: Any relevant comments or explanations in the code.

    Return the extracted information in a markdown table with these columns:

    - Metric
    - Threshold
    - Outcome
    - Notes

    If no specific metrics (e.g., accuracy, F1 score) are found, return a summary instead of a the given information.

    Here is the Python code to analyze:

    {code}
    """
    return prompt.format(code=code)


def prompt_for_generation_resume(code):
    prompt = """
    Provide a summary of the Python code with the following structure:

        1. **Purpose**: Explain the main goal of the code. What problem does it solve or what task does it perform?
        2. **Key Functionalities**: Describe the main functions or processes the code executes. What are its core operations?
        3. **Components**: 
        - Libraries/Modules: Mention any important libraries or modules the code utilizes.
        - Inputs: What kind of data or parameters does the code require to function?
        - Outputs: What does the code return or produce after execution?
        4. **Steps/Process**: Outline the significant steps or processes the code follows to accomplish its task.
        5. **Additional Information**:
        - Performance Considerations: Are there any optimizations or efficiency factors to be aware of?
        - Use Cases: What scenarios or problems can the code be applied to?
        - Limitations: Mention any known limitations or constraints of the code.

        Avoid including any actual code. Focus on describing how the code operates and what it achieves.

        Here is the Python code you need to summarize:

        {code}
    """
    return prompt.format(code=code)


def prompt_for_review_format(markdown_text, translated_language):
    prompt = """**Task:** Corrects the following Markdown content to ensure it adheres to the required formatting standards.

    **Formatting Guidelines:**
    - Structure the content with appropriate headings for clear organization.
    - Use bullet points or numbered lists where relevant to improve readability.
    - Highlight important points using **bold** or *italic* formatting.
    - Format code snippets properly using backticks or code blocks.
    - Corrects spelling, grammatical or typographical errors.
    - Perform the translation if the content is not already in **{translated_language}**.

    **Markdown Text for Corrects:**
    {markdown_text}

    **Expected output:** The corrected Markdown content that follows the formatting guidelines.
    """
    return prompt.format(markdown_text=markdown_text, translated_language=translated_language)


def prompt_for_documentation_name(context):
    prompt = """Create a single, short, and descriptive file name for the Markdown documentation based on the following context. The file name should be concise, clearly represent the content, and be suitable for a .md file (avoid special characters that may affect formatting).

    Context: {context}

    File Name:
    """
    return prompt.format(context=context)

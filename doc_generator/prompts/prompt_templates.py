system_prompt = "You are an AI designed to provide direct answers to questions. Please respond only with the most accurate and concise answer, without any additional explanations, clarifications, or phrases."


def prompt_for_documentation(combined_content, context, tables_info):
    prompt = """**Instructions**: Below is the content of a Jupyter Notebook in markdown and code format. Your task is to create clear and structured documentation that covers the purpose, methodology, analysis, results, and conclusions of the notebook. Organize it into the following sections:

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
    Please follow these instructions for the provided Python code:

    1. Format the code according to the `black` Python code style, with a line length of 100 characters.
    2. Add comments explaining the functionality of each section of the code.
    3. For lines that are unnecessary or redundant, replace them with a descriptive comment such as:
       `# This line has been replaced because it is unnecessary. The functionality it provided was previously explained above.`
    4. Ensure that the code remains functional while improving readability with added commentary.
    5. If a line of code is commented out, please review the readability of the comment. Make sure the comment is clear, concise, and provides context for why the line is commented out or no longer needed.

    Here is the code you need to modify:

    {code}
    """
    return prompt.format(code=code)


def prompt_for_table_creation(code):
    prompt = """Analyze the following Python code and extract details about the **metrics validation** steps. Specifically, identify the following:

    - **Metric Names**: Metrics being evaluated (e.g., accuracy, F1 score, AUC).
    - **Validation Types**: Type of validation performed (e.g., classification, regression).
    - **Validation Methods**: Techniques used (e.g., confusion matrix, k-fold cross-validation).
    - **Thresholds/Criteria**: Thresholds or criteria used (e.g., precision > 0.8, recall > 0.75).
    - **Expected Outcome**: Expected result or performance (e.g., acceptable accuracy or precision).
    - **Comments/Explanations**: Any relevant comments or explanations in the code.

    Return the extracted information in a markdown table format with the following columns:

    - Metric Name
    - Validation Type
    - Validation Method
    - Threshold/Criterion
    - Expected Outcome
    - Notes/Comments

    Each row should represent a unique validation step. If multiple metrics or techniques are used, include a row for each.

    Only return the table, no extra explanations.

    Here is the Python code to analyze:

    {code}
    """
    return prompt.format(code=code)


def prompt_for_generation_resume(code):
    prompt = """Provide a detailed summary of the Python code with the following structure:

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

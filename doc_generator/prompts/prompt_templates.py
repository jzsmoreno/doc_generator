def prompt_for_documentation(combined_content, context, tables_info):
    prompt = """
    **Instructions**: Below is the content of a Jupyter Notebook in markdown and code format. Your task is to create clear documentation covering the purpose, methodology, analysis, results, and conclusions of the notebook. Organize it into the following sections:

    1. **Introduction**: Briefly describe the main goal of the notebook.
    2. **Methodology**: Summarize the key steps and processes followed.
    3. **Analysis and Results**: Outline the analysis and results obtained.
    4. **Conclusions**: Provide any applicable conclusions.

    **Considerations**:
    - Use clear, simple language and avoid excessive code details.
    - **Incorporate the provided context and tables** to enhance the explanation.
    - Structure the output in **Markdown** format, using headings, lists, and bold text for clarity.

    **Input**: Below is the markdown and code content of the Jupyter Notebook:

    {combined_content}

    Context for the notebook:

    {context}

    Details of the tables extracted from the code:

    {tables_info}

    **Expected output**: A well-organized **Markdown** document explaining the notebook, using the context and tables_info where relevant.
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
    prompt = """Please analyze the Python code and extract details about the **metrics validation** steps used. Specifically, look for information regarding:

    - Metric names
    - Validation types (e.g., accuracy, precision, recall, etc.)
    - Validation methods (e.g., confusion matrix, cross-validation)
    - Thresholds or criteria for validation
    - Expected output or results
    - Any comments explaining the validation steps

    Generate the relevant details as a table in **Markdown** format with the following columns:

    | Metric Name     | Validation Type | Validation Method  | Threshold/Criterion | Expected Outcome | Notes/Comments |
    |-----------------|-----------------|--------------------|---------------------|------------------|----------------|

    Include any rows that highlight different metric validation steps or results.

    Here is the code you need to analyze:

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
    prompt = """Review the following markdown content and ensure it adheres to the required formatting standards. 

    **Formatting Guidelines:**
    - Use appropriate headings to organize the content logically.
    - Incorporate bullet points or numbered lists where applicable for better readability.
    - Highlight key points using bold or italic formatting.
    - Ensure code snippets are formatted properly (e.g., using backticks or code blocks).
    - Check for any spelling, grammatical, or typographical errors.

    **Review the Markdown Text:**
    {markdown_text}

    Additionally, if necessary, translate the content into **{translated_language}** to broaden its accessibility.

    Provide detailed feedback on the formatting, readability, and overall quality of the markdown content. Make any necessary adjustments to improve clarity, structure, and presentation.
    """
    return prompt.format(markdown_text=markdown_text, translated_language=translated_language)


def prompt_for_documentation_name(context):
    prompt = """Create a concise, descriptive title for the documentation based on the context provided below. The title should accurately represent the content and be formatted appropriately for an MD (Markdown) document (e.g., no special characters that might break the formatting).

    **Context**: {context}

    **Title**:
        """
    return prompt.format(context=context)

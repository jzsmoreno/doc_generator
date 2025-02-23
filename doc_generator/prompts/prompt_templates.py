def prompt_for_documentation(combined_content):
    prompt = """
    **Instructions**: Below is the content of a Jupyter Notebook in markdown and code format. Your task is to generate a brief and clear documentation on the general purpose of the notebook, the main steps followed, the analysis performed, and the results obtained, if any. Organize the documentation into the following sections:

    1. **Introduction**: A brief description of the main goal of the notebook.
    2. **Methodology**: Explanation of the key steps or processes followed in the notebook.
    3. **Analysis and Results**: A summary of the analysis performed and the results obtained.
    4. **Conclusions**: A brief conclusion, if applicable.

    **Considerations**:
    - Make sure to use clear and simple language.
    - Do not include excessive details about the code; focus on describing the actions and the reasoning behind them.
    - If the notebook includes graphs or visualizations, mention their purpose and what insights they provide.
    - If specific tools or libraries are used (such as Pandas, Matplotlib, etc.), briefly mention their role in the analysis.
    - The output must be properly structured in **Markdown** format. Use headings, lists, and bold text appropriately to improve readability and organization.

    **Input**: Below is the markdown and code content of the Jupyter Notebook:

    {combined_content}

    **Expected output**: The output should be a structured text in **Markdown** format that explains the notebook concisely yet comprehensively, covering the mentioned sections, and following the given considerations.
    """
    return prompt.format(combined_content=combined_content)

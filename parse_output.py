import ast

def parse_output(output: str, filename: str) -> dict:
    """
    Parses the LLM output string into a Python dictionary.
    Attaches the source filename for traceability.
    
    Args:
        output (str): Output from the LLM, expected to be a Python dict in string form.
        filename (str): Name of the image file associated with this output.

    Returns:
        dict: Parsed data with filename added.
    """
    try:
        # Safely evaluate the string to a Python dictionary
        parsed = ast.literal_eval(output)

        if not isinstance(parsed, dict):
            raise ValueError("Parsed output is not a dictionary.")

        # Attach the filename for traceability
        parsed['filename'] = filename

        return parsed

    except (SyntaxError, ValueError) as e:
        print(f"Failed to parse output for {filename}: {e}")
        return {
            "filename": filename,
            "error": str(e),
            "raw_output": output
        }
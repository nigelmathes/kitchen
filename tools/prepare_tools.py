"""
Function to resolve which tool to use based on the YAML files:
ingredients.yaml, and full_course.yaml
"""
from importlib import import_module
from typing import Callable


def prepare_tools(python_format: str, file_format: str) -> Callable:
    """
    Find the right class to take the ingredients from their raw form
    to their prepared form

    Args:
        python_format (str): The Python data type to read the data into, such
                               as 'pandas'
        file_format (str): The raw data format, such as 'csv'

    Returns:
        (Callable): The function to Extract the data
    """
    # Create the string to import the module needed to load the data
    file_to_import_from = f"tools.{python_format}.{file_format}"

    # Cast to CamelCase for class name
    tool_to_import = "".join(word.title() for word in file_format.split("_"))

    # Import class
    tool_to_use = getattr(import_module(file_to_import_from), tool_to_import)

    return tool_to_use

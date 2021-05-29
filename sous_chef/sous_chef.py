"""
The Sous Chef Prepares the Ingredients
I.e. the extract stage of your ETL process.
"""
from importlib import import_module
from pathlib import Path
from typing import Dict, Any, Callable

import anyconfig

from server.data_models import Ingredient


class SousChef:
    """
    Prepare ingredients for the Chef

    i.e. Extract data and prepare it for processing
    """

    def __init__(
        self, ingredients: Path = Path("/app/sous_chef/ingredients.yaml")
    ) -> None:
        """
        Give the Sous Chef the instruction needed to prepare the data for the Chef

        i.e. Initialize the following from a YAML configuration file:
             data location (source)
             type of data (source_type)
             the type of the output data (prepared_foramed)

        Args:
            ingredients (Path): A YAML file within the sous_chef directory containing
                               the ingredients to prepare
        """
        self.ingredients = dict()

        # Load from ingredients.yaml
        for key, value in anyconfig.load(ingredients).items():
            self.ingredients[key] = Ingredient(**value)

    def prepare_ingredients(self) -> Dict[str, Any]:
        """
        Loop over all ingredients loaded in from ingredients.yaml and prepare them

        i.e. Extract each data source, going from raw input file to Python
             data structure, such as a Pandas DataFrame

        Returns:
            (Dict): Key:value store of data, labeled according to the names in
                    ingredients.yaml. E.g.
                    {"training_data": pd.DataFrame([[0, ...]])}
        """
        ingredients_to_deliver = dict()

        for name, ingredient in self.ingredients.items():
            ingredients_to_deliver[name] = self.prepare_one_ingredient(
                ingredient=ingredient, name=name
            )

        return ingredients_to_deliver

    def prepare_one_ingredient(self, ingredient: Ingredient, name: str) -> Any:
        """
        Prepare one ingredient by using Ingredient.raw_format and
        Ingredient.prepared_format to identify the correct function to read
        the input data

        Args:
            ingredient (Ingredient): One ingredient, which is the dataclass Ingredient
            name (str): The name of the ingredient

        Returns:
            (Any) Data loaded into a Python data structure, such as a Pandas DataFrame
        """
        # Find the right tool for the job (data loading)
        tool = self.prepare_tools(python_format=ingredient.python_format,
                                  file_format=ingredient.file_format)

        # Instantiate object
        data_load_tool = tool(filepath=ingredient.location)

        # Load data
        loaded_data = data_load_tool.load()

        return loaded_data

    @staticmethod
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
        tool_to_import = ''.join(word.title() for word in file_format.split('_'))

        # Import class
        tool_to_use = getattr(import_module(file_to_import_from), tool_to_import)

        return tool_to_use


if __name__ == "__main__":
    sous_chef = SousChef()
    test_ingredients = sous_chef.prepare_ingredients()

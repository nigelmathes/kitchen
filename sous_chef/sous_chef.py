"""
The Sous Chef Prepares the Ingredients
I.e. the extract stage of your ETL process.
"""
from pathlib import Path
from typing import Dict, Any, Callable

import anyconfig
import fsspec
import pandas as pd

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
             the type of the output data (output_type)

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
                ingredient=ingredient
            )

        return ingredients_to_deliver

    def prepare_one_ingredient(self, ingredient: Ingredient) -> Any:
        """
        Prepare one ingredient by using Ingredient.raw_format and
        Ingredient.prepared_format to identify the correct function to read
        the input data

        Args:
            ingredient (Ingredient): One ingredient, which is the dataclass Ingredient

        Returns:
            (Any) Data loaded into a Python data structure, such as a Pandas DataFrame
        """
        with fsspec.open(ingredient.location) as input_file:
            extract_function = self.prepare_tools(
                input_type=ingredient.raw_format,
                output_type=ingredient.prepared_format
            )
            loaded_data = extract_function(input_file)

        return loaded_data

    @staticmethod
    def prepare_tools(input_type: str, output_type: str) -> Callable:
        """
        Find the right load function to take the ingredients from their raw form
        to their prepared form

        Returns:
            (Callable): The function to Extract the data
        """
        if input_type == "csv" and output_type == "pandas.DataFrame":
            return pd.read_csv
        if input_type == "json" and output_type == "pandas.DataFrame":
            return pd.read_json


if __name__ == '__main__':
    sous_chef = SousChef()
    test_ingredients = sous_chef.prepare_ingredients()
    print(test_ingredients)

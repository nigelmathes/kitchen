"""
The Head Chef Cooks the Final Dish
I.e. the transform stage of your ETL process.
"""
from typing import Any

from sous_chef.sous_chef import SousChef


class HeadChef:
    """
    The Chef who does the cooking with the prepared ingredients from the SousChef

    i.e. The Transform stage - take data served by the SousChef, which is already
         in a Python data structure, and process it
    """
    def __init__(self) -> None:
        """
        Take some inputs?
        """
        sous_chef = SousChef()
        self.ingredients = sous_chef.prepare_ingredients()

    def cook(self) -> Any:
        """
        Cook the ingredients

        i.e. Perform all transformation tasks to create the desired output data

        This can be anything from training a machine learning model, adding
        columns to a DataFrame, performing inference with an ML model, or anything
        really that creates the desired output data that this Head Chef is going to
        create and serve.

        Returns:
            (Any): The Dish to serve, i.e. the output data
        """
        # Train the model, output the model, and then use the model on the test data
        # Return the model and the results of inference on the test data
        pass

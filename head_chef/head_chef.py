"""
The Head Chef Cooks the Final Dish
I.e. the transform & load stages of your ETL process.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import anyconfig

from sous_chef.sous_chef import SousChef
from wait_staff.data_models import FullCourse
from tools.prepare_tools import prepare_tools


class HeadChef(ABC):
    """
    The Chef who does the cooking with the prepared ingredients from the SousChef

    i.e. The Transform stage - take data served by the SousChef, which is already
         in a Python data structure, and process it
    """

    def __init__(
        self, full_course: Path = Path("/app/head_chef/full_course.yaml")
    ) -> None:
        """
        Give the Head Chef the instructions needed to prepare the full course

        i.e. Initialize the following from a YAML configuration file:
                - location (where to output the file)
                - python_format (the Python data type after processing)
                - file_format (the file format with which to save the data)

        Args:
            full_course (Path): A YAML file within the head_chef directory containing
                                the ingredients to prepare
        """
        sous_chef = SousChef()
        self.ingredients = sous_chef.prepare_ingredients()

        self.full_course = dict()
        self.tools = dict()

        # Load from full_course.yaml
        for key, value in anyconfig.load(full_course).items():
            self.full_course[key] = FullCourse(**value)

            # Find the right tool for the job (data saving)
            self.tools[key] = prepare_tools(
                python_format=self.full_course[key].python_format,
                file_format=self.full_course[key].file_format,
            )

    @abstractmethod
    def cook(self) -> Any:
        """
        Cook the ingredients

        i.e. Perform all transformation tasks to create the desired output data

        This can be anything from training a machine learning model, adding
        columns to a DataFrame, performing inference with an ML model, etc. Anything
        really that creates the desired output data that this Head Chef is going to
        create and serve.

        Returns:
            (Any): The Dish to serve, i.e. the output data
        """
        raise NotImplementedError(
            "You are using the HeadChef base class and must implement a cook() method"
        )

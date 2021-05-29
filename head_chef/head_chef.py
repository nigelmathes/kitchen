"""
The Head Chef Cooks the Final Dish
I.e. the transform stage of your ETL process.
"""
from importlib import import_module
from pathlib import Path
from typing import Any, Callable

import anyconfig
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from sous_chef.sous_chef import SousChef
from server.data_models import FullCourse
from window_display.auto_display import create_window_display


class HeadChef:
    """
    The Chef who does the cooking with the prepared ingredients from the SousChef

    i.e. The Transform stage - take data served by the SousChef, which is already
         in a Python data structure, and process it
    """

    def __init__(
        self, full_course: Path = Path("/app/head_chef/full_course.yaml")
    ) -> None:
        """
        Give the Head Chef the instruction needed to prepare the full course for
        serving

        i.e. Initialize the following from a YAML configuration file:
             data location (where to output the file)

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
            self.tools[key] = self.prepare_tools(
                python_format=self.full_course[key].python_format,
                file_format=self.full_course[key].file_format,
            )

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
        training_data = self.clean(self.ingredients["titanic_train_data"])
        test_data = self.clean(self.ingredients["titanic_test_data"])

        # Remove label column
        features = training_data.drop("Survived", axis=1)
        labels = training_data["Survived"]

        # Train
        random_forest_classifier = RandomForestClassifier(
            n_estimators=500, random_state=42
        )
        random_forest_classifier.fit(features, labels)

        # Save the trained model
        model_tool = self.tools["classifier_model"](filepath=self.full_course[
            "classifier_model"].location)
        model_tool.save(data=random_forest_classifier)

        # Evaluate the trained model and save results
        eval_results = pd.DataFrame(
            random_forest_classifier.predict(test_data), columns=["model_predictions"]
        )

        test_data["model_predictions"] = eval_results

        # Save the evaluation results
        results_tool = self.tools["model_results"](filepath=self.full_course[
            "model_results"].location)
        results_tool.save(data=test_data)

        # Create a window display with the results
        create_window_display(
            data_to_display=test_data,
            display_name="model_results",
        )

    @staticmethod
    def clean(data_to_clean: pd.DataFrame) -> pd.DataFrame:
        """
        An example of doing data cleaning. This will be a step in self.cook()

        Args:
            data_to_clean (pd.DataFrame): A dirty Pandas DataFrame

        Returns:
            pd.DataFrame: A cleaned Pandas Dataframe
        """
        # Mapping Sex
        data_to_clean["Sex"] = (
            data_to_clean["Sex"].map({"female": 0, "male": 1}).astype(int)
        )

        # Mapping Embarked
        data_to_clean["Embarked"] = data_to_clean["Embarked"].fillna("S")
        data_to_clean["Embarked"] = (
            data_to_clean["Embarked"].map({"S": 0, "C": 1, "Q": 2}).astype(int)
        )

        # Mapping Fare
        data_to_clean["Fare"] = data_to_clean["Fare"].fillna(
            data_to_clean["Fare"].median()
        )
        data_to_clean.loc[data_to_clean["Fare"] <= 7.91, "Fare"] = 0
        data_to_clean.loc[
            (data_to_clean["Fare"] > 7.91) & (data_to_clean["Fare"] <= 14.454), "Fare"
        ] = 1
        data_to_clean.loc[
            (data_to_clean["Fare"] > 14.454) & (data_to_clean["Fare"] <= 31), "Fare"
        ] = 2
        data_to_clean.loc[data_to_clean["Fare"] > 31, "Fare"] = 3
        data_to_clean["Fare"] = data_to_clean["Fare"].astype(int)

        # Mapping Age
        data_to_clean.loc[data_to_clean["Age"] <= 16, "Age"] = 0
        data_to_clean.loc[
            (data_to_clean["Age"] > 16) & (data_to_clean["Age"] <= 32), "Age"
        ] = 1
        data_to_clean.loc[
            (data_to_clean["Age"] > 32) & (data_to_clean["Age"] <= 48), "Age"
        ] = 2
        data_to_clean.loc[
            (data_to_clean["Age"] > 48) & (data_to_clean["Age"] <= 64), "Age"
        ] = 3
        data_to_clean.loc[data_to_clean["Age"] > 64, "Age"] = 4

        # Feature Selection
        drop_elements = ["Name", "Ticket", "Cabin", "SibSp", "Parch", "PassengerId"]
        data_to_clean.drop(drop_elements, axis=1, inplace=True)

        # Fill any remaining NaN
        data_to_clean.fillna(0, inplace=True)

        return data_to_clean

    @staticmethod
    def prepare_tools(python_format: str, file_format: str) -> Callable:
        """
        Find the right class to take the ingredients from their raw (file) format
        to their prepared (python) format

        Args:
            python_format (str): The Python data type to read the data into, such
                                 as 'pandas'
            file_format (str): The format of the file to read, such as 'csv'

        Returns:
            (Callable): The function to extract the data
        """
        # Create the string to import the module needed to load the data
        file_to_import_from = f"tools.{python_format}.{file_format}"

        # Cast to CamelCase for class name
        tool_to_import = ''.join(word.title() for word in file_format.split('_'))

        # Import class
        tool_to_use = getattr(import_module(file_to_import_from), tool_to_import)

        return tool_to_use


if __name__ == "__main__":
    head_chef = HeadChef()
    test_ingredients = head_chef.cook()

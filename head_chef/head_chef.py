"""
The Head Chef Cooks the Final Dish
I.e. the transform stage of your ETL process.
"""
import tempfile

from pathlib import Path
from typing import Any

import anyconfig
import fsspec
import joblib
import pandas as pd

from fsspec.utils import infer_storage_options
from sklearn.ensemble import RandomForestClassifier

from sous_chef.sous_chef import SousChef
from server.data_models import FullCourse
from window_display.create_display import create_window_display


class HeadChef:
    """
    The Chef who does the cooking with the prepared ingredients from the SousChef

    i.e. The Transform stage - take data served by the SousChef, which is already
         in a Python data structure, and process it
    """

    def __init__(self, full_course: Path = Path("/app/head_chef/full_course.yaml")) -> None:
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

        # Load from full_course.yaml
        for key, value in anyconfig.load(full_course).items():
            self.full_course[key] = FullCourse(**value)

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
        training_data = self.clean(self.ingredients['titanic_train_data'])
        test_data = self.clean(self.ingredients['titanic_test_data'])

        # Remove label column
        features = training_data.drop('Survived', axis=1)
        labels = training_data['Survived']

        # Train
        random_forest_classifier = RandomForestClassifier(n_estimators=500,
                                                          random_state=42)
        random_forest_classifier.fit(features, labels)

        # Save the trained model
        self.save_model(model_to_save=random_forest_classifier)

        # Evaluate the trained model and save results
        eval_results = pd.DataFrame(random_forest_classifier.predict(test_data),
                                    columns=['model_predictions'])

        test_data['model_predictions'] = eval_results

        # Save the evaluation results
        self.save_results(results_to_save=test_data)

        # Create a window display with the results
        create_window_display(data_to_display=test_data, display_name="model_results",
                              display_type="dataprep")

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
        data_to_clean['Embarked'] = data_to_clean['Embarked'].fillna('S')
        data_to_clean["Embarked"] = (
            data_to_clean["Embarked"].map({"S": 0, "C": 1, "Q": 2}).astype(int)
        )

        # Mapping Fare
        data_to_clean['Fare'] = data_to_clean['Fare'].fillna(data_to_clean['Fare'].median())
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
        drop_elements = [
            "Name",
            "Ticket",
            "Cabin",
            "SibSp",
            "Parch",
            "PassengerId"
        ]
        data_to_clean.drop(drop_elements, axis=1, inplace=True)

        # Fill any remaining NaN
        data_to_clean.fillna(0, inplace=True)

        return data_to_clean

    def save_model(self, model_to_save: RandomForestClassifier) -> None:
        """
        Save a trained model

        Args:
            model_to_save (RandomForestClassifier): A trained random forest model

        Returns:
            None: But, saves a sklearn model using joblib
        """
        # Get the save path for the model and extract the file system protocol
        save_parameters = infer_storage_options(self.full_course['classifier_model'].location)
        protocol = save_parameters["protocol"]
        model_output_path = save_parameters["path"]

        # Get only the file name
        model_name = Path(model_output_path).name

        # Save to /tmp/ before using fssspec to move it to its final destination
        with tempfile.TemporaryDirectory() as temp_directory:
            temporary_save_path = Path(temp_directory) / model_name
            joblib.dump(value=model_to_save, filename=temporary_save_path)

            file_system = fsspec.filesystem(protocol=protocol)
            file_system.put_file(lpath=temporary_save_path, rpath=model_output_path)

        return None

    def save_results(self, results_to_save: pd.DataFrame) -> None:
        """
        Save model results

        Args:
            results_to_save (pd.DataFrame): Prediction results from a trained model

        Returns:
            None: But, saves a CSV containing model prediction results
        """
        save_location = self.full_course["model_results"].location

        with fsspec.open(save_location, mode='w') as fs_file:
            results_to_save.to_csv(path_or_buf=fs_file, index=False)


if __name__ == '__main__':
    head_chef = HeadChef()
    test_ingredients = head_chef.cook()

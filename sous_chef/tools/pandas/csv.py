import pandas as pd

from sous_chef.tools.tool import Tool


class Csv(Tool):
    """
    Loads/saves CSV data as a Pandas DataFrame from/to a text file
    on any ``fsspec``-supported file-like system
    """
    def load(self) -> pd.DataFrame:
        """
        Load text data from a CSV file into a Pandas DataFrame

        Returns:
            pd.DataFrame: Loaded CSV data
        """
        with self.filesystem.open(self.filepath) as fs_file:
            csv_data = pd.read_csv(fs_file)

        return csv_data

    def save(self, data: pd.DataFrame) -> None:
        """
        Save a Pandas DataFrame as a CSV file

        Args:
            data (pd.DataFrame): A Pandas DataFrame containing data to save

        Returns:
            None
        """
        with self.filesystem.open(self.filepath) as fs_file:
            data.to_csv(fs_file, index=False)

        return None

    def exists(self) -> bool:
        """
        Check if a text file exists

        Returns:
            bool: True if the file exists, otherwise False
        """
        return self.filesystem.exists(self.filepath)

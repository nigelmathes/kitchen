import pandas as pd

from tools.tool import Tool


class CsvFile(Tool):
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
        with self.filesystem.open(path=self.filepath) as fs_file:
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
        with self.filesystem.open(path=self.filepath, mode='w') as fs_file:
            data.to_csv(path_or_buf=fs_file, index=False)

        return None

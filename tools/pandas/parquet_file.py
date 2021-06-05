import pandas as pd

from pyarrow.dataset import dataset
from tools.tool import Tool


class ParquetFile(Tool):
    """
    Loads/saves data as a Pandas DataFrame from/to a parquet file
    on any ``fsspec``-supported file-like system
    """

    def load(self) -> pd.DataFrame:
        """
        Load text data from a parquet file into a Pandas DataFrame

        Returns:
            pd.DataFrame: Loaded parquet data
        """
        parquet_data = (
            dataset(source=self.filepath, format="parquet", filesystem=self.filesystem)
            .to_table()
            .to_pandas(
                date_as_object=True,
                use_threads=False,
                split_blocks=True,
                self_destruct=True,
            )
        )

        return parquet_data

    def save(self, data: pd.DataFrame) -> None:
        """
        Save a Pandas DataFrame as a parquet file

        Args:
            data (pd.DataFrame): A Pandas DataFrame containing data to save

        Returns:
            None
        """
        with self.filesystem.open(path=self.filepath, mode="w") as file:
            data.to_parquet(file, index=False)

        return None

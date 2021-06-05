import tempfile

from pathlib import Path
from typing import List, Any

import joblib

from tools.tool import Tool


class JoblibFile(Tool):
    """
    Loads/saves text data as a Python list from/to a text file
    on any ``fsspec``-supported file-like system
    """

    def load(self) -> List[str]:
        """
        Load a scikit-learn model from a joblib file

        Returns:
            Any: A scikit-learn model of the appropriate class
        """
        # TODO: Do this
        raise NotImplementedError

    def save(self, data: Any) -> None:
        """
        Save a list of strings to a text file

        Args:
            data (Any): A scikit-learn model, such as RandomForestClassifier

        Returns:
            None
        """
        # Save to /tmp/ before using fsspec to move it to its final destination
        with tempfile.TemporaryDirectory() as temp_directory:
            temporary_save_path = Path(temp_directory) / Path(self.filepath).name
            joblib.dump(value=data, filename=temporary_save_path)

            self.filesystem.put_file(lpath=temporary_save_path, rpath=self.filepath)

        return None

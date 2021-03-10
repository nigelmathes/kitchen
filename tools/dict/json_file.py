import json

from typing import Dict

from tools.tool import Tool


class JsonFile(Tool):
    """
    Loads/saves data as a Python dict from/to a JSON file
    on any ``fsspec``-supported file-like system
    """
    def load(self) -> Dict:
        """
        Load data from a JSON file into a Python dictionary

        Returns:
            Dict: Loaded JSON data
        """
        with self.filesystem.open(path=self.filepath) as file:
            return json.load(file)

    def save(self, data: Dict) -> None:
        """
        Save a dict to a JSON file

        Args:
            data (Dict): A dict containing data

        Returns:
            None
        """
        with self.filesystem.open(path=self.filepath, mode='w') as file:
            json.dump(data, file)

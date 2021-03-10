import yaml

from typing import Dict

from tools.tool import Tool


class YamlFile(Tool):
    """
    Loads/saves data as a Python dict from/to a Yaml file
    on any ``fsspec``-supported file-like system
    """
    def load(self) -> Dict:
        """
        Load data from a Yaml file into a Python dictionary

        Returns:
            Dict: Loaded Yaml data
        """
        with self.filesystem.open(path=self.filepath) as file:
            return yaml.safe_load(file)

    def save(self, data: Dict) -> None:
        """
        Save a dict to a Yaml file

        Args:
            data (Dict): A dict containing data

        Returns:
            None
        """
        with self.filesystem.open(path=self.filepath, mode='w') as file:
            yaml.dump(data, file)

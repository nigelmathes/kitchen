from typing import List

from tools.tool import Tool


class TextFile(Tool):
    """
    Loads/saves text data as a Python list from/to a text file
    on any ``fsspec``-supported file-like system
    """
    def load(self) -> List[str]:
        """
        Load text data from a text file split on new line characters

        Returns:
            List[str]: Loaded text data
        """
        with self.filesystem.open(path=self.filepath) as file:
            text_data = file.read().split('\n')

        return list(filter(None, text_data))

    def save(self, data: List[str]) -> None:
        """
        Save a list of strings to a text file

        Args:
            data (List[str]): A list of strings

        Returns:
            None
        """
        with self.filesystem.open(path=self.filepath, mode='wb') as file:
            for entry in data:
                file.write(entry)

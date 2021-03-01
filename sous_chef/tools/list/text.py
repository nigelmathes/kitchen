from typing import List

from sous_chef.tools.tool import Tool


class Text(Tool):
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
        with self.filesystem.open(self.filepath) as fs_file:
            text_data = fs_file.read().split('\n')

        return list(filter(None, text_data))

    def save(self, data: List[str]) -> None:
        """
        Save a list of strings to a text file

        Args:
            data (List[str]): A list of strings

        Returns:
            None
        """
        with self.filesystem.open(self.filepath) as fs_file:
            for entry in data:
                fs_file.write(entry)

    def exists(self) -> bool:
        """
        Check if a text file exists

        Returns:
            bool: True if the file exists, otherwise False
        """
        return self.filesystem.exists(self.filepath)

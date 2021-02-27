from typing import Any, Dict, List

import fsspec
from fsspec.utils import infer_storage_options


class Text:
    """
    Loads/saves text data as a Python list from/to a text file
    on any ``fsspec``-supported file-like system
    """

    def __init__(
        self,
        filepath: str,
        credentials: Dict[str, Any] = None,
    ) -> None:
        """
        Instantiate a ``Text`` object referencing a text file

        Args:
            filepath (Path): Filepath to a text file. May include protocol prefix,
                             e.g. `s3://`. With no prefix, assumes local filesystem.
                             Prefixes can include any protocol supported by ``fsspec``
            credentials (Dict[str, Any]): Credentials required to access to the
                                          filesystem as keys and values.
                                          e.g. {"my_token": "ABCD1234"}
        """
        self.protocol, self.filepath = infer_storage_options(filepath)

        self.filesystem = fsspec.filesystem(protocol=self.protocol, **credentials)

    def _load(self) -> List[str]:
        """
        Load text data from a text file split on new line characters

        Returns:
            List[str]: Loaded text data
        """
        with self.filesystem.open(self.filepath) as fs_file:
            text_data = fs_file.read().split('\n')

            return list(filter(None, text_data))

    def _save(self, data: List[str]) -> None:
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

    def _exists(self) -> bool:
        """
        Check if a text file exists

        Returns:
            bool: True if the file exists, otherwise False
        """
        return self.filesystem.exists(self.filepath)

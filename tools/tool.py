import abc

from typing import Any, Dict

import fsspec
from fsspec.utils import infer_storage_options


class Tool(abc.ABC):
    """
    Base class for other classes that load data into Python objects from/to a file
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
        storage_options = infer_storage_options(filepath)
        self.protocol = storage_options["protocol"]
        self.filepath = storage_options["path"]

        if not credentials:
            credentials = {}

        self.filesystem = fsspec.filesystem(protocol=self.protocol, **credentials)

    @abc.abstractmethod
    def load(self) -> Any:
        """
        Load data
        """
        raise NotImplementedError("You are using the Tool base class and must "
                                  "implement a load() method")

    @abc.abstractmethod
    def save(self, data: Any) -> None:
        """
        Save data
        """
        raise NotImplementedError("You are using the Tool base class and must "
                                  "implement a save() method")

    def exists(self) -> bool:
        """
        Check if a text file exists

        Returns:
            bool: True if the file exists, otherwise False
        """
        return self.filesystem.exists(self.filepath)

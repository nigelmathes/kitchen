from abc import ABC, abstractmethod
from typing import Any, Dict

import fsspec
from fsspec.utils import infer_storage_options

from wait_staff.data_models import SourceTraceability


class Tool(ABC):
    """
    Base class for other classes that load data into Python objects from/to a file
    on any ``fsspec``-supported file-like system
    """

    def __init__(self, filepath: str, credentials: Dict[str, Any] = None,) -> None:
        """
        Instantiate a ``Tool`` object, meant to save and load data

        Args:
            filepath (Path): Filepath to a file. May include protocol prefix,
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

    @abstractmethod
    def load(self) -> Any:
        """
        Load data
        """
        raise NotImplementedError(
            "You are using the Tool base class and must " "implement a load() method"
        )

    @abstractmethod
    def save(self, data: Any) -> None:
        """
        Save data
        """
        raise NotImplementedError(
            "You are using the Tool base class and must " "implement a save() method"
        )

    def exists(self) -> bool:
        """
        Check if a file exists

        Returns:
            bool: True if the file exists, otherwise False
        """
        return self.filesystem.exists(self.filepath)

    def source(self) -> SourceTraceability:
        """
        Detail the data lineage/provenance for the source data,
        and prepare to output it as a file in self.save()

        Returns:
            Dict: Keys and values containing data lineage/provenance information
        """
        source_information = SourceTraceability(lineage=self.filepath)

        return source_information

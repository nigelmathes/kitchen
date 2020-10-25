"""
Pydantic Data Classes storing data inputs and outputs for this pod
"""
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class InputData(BaseModel):
    """ Contains input data to the pod """

    data_source_path: Path


class OutputData(BaseModel):
    """ Contains output data being served by the pod """

    data: Any

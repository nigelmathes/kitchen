"""
Pydantic Data Classes storing data inputs and outputs for this pod
"""
from datetime import datetime
from pathlib import Path
from typing import Any, Union, Optional, List

from pydantic import BaseModel


class Ingredient(BaseModel):
    """
    Contains input data that will be used to create this dish.
    """

    # Required parameters
    location: Union[str, Path]
    file_format: str
    python_format: str

    # Optional parameters
    date_accessed: Optional[datetime] = None

    git_hash: Optional[str] = None
    dvc_hash: Optional[str] = None


class FullCourse(BaseModel):
    """
    Contains the full set of data produced by this chef for this dish.

    This is the data that will be sent if a patron orders the full course.
    """

    # Required parameters
    location: Union[str, Path]
    file_format: str
    python_format: str

    # Optional parameters
    date_generated: Optional[datetime] = None
    ingredients_used: Optional[List[Ingredient]] = None

    dvc_hash: Optional[str] = None
    git_hash: Optional[str] = None


class Appetizer(BaseModel):
    """
    Contains a small preview or snapshot of the data produced by this chef for this dish.

    This may just be the FullCourse, should the data be small enough to preview quickly.

    This is the data that will appear in HTML data reports and will be sent if a
    patron orders the appetizer.
    """

    data_source: Any


class SourceTraceability(BaseModel):
    """
    Maintains the set of parameters to keep track of data lineage.

    Source - S3 bucket, file location, node API endpoint, etc.
    Date Generated
    Git branch/commit which generated it
    DVC branch/commit which generated it
    Prior node's data lineage
    """

    lineage: Any = None

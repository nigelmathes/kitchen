"""
Pydantic Data Classes storing data inputs and outputs for this pod
"""
from datetime import datetime
from pathlib import Path
from typing import Any, Union, Dict

from pydantic import BaseModel


class Ingredients(BaseModel):
    """
    Contains input data that will be used to create this dish.

    Source - S3 bucket, file location, node API endpoint, etc.
    Date Generated
    Git branch/commit which generated it
    DVC branch/commit which generated it
    Prior node's data lineage
    """

    data_source: Union[str, Path]
    date_generated: datetime.time
    git_hash: str
    dvc_hash: str
    lineage: Dict


class FullCourse(BaseModel):
    """
    Contains the full set of data produced by this chef for this dish.

    This is the data that will be sent if a patron orders the full course.
    """

    data_source: Union[str, Path]
    date_generated: datetime.time
    git_hash: str
    dvc_hash: str
    lineage: Dict


class Appetizer(BaseModel):
    """
    Contains a small preview or snapshot of the data produced by this chef for this dish.

    This may just be the FullCourseData, should your data set be small enough to
    preview quickly.

    This is the data that will appear in HTML data reports and will be sent if a
    patron orders the appetizer.
    """

    data_source: Any

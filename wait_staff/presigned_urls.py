"""
Generates pre-signed URL links to download data served through the server APIs
"""
import fsspec
from fsspec.utils import infer_storage_options


def create_presigned_url(filepath: str, expiration: int = 120) -> str:
    """
    Generate a pre-signed URL to share an S3 object

    Args:
        filepath (str): Path to the file to create a pre-signed URL to download
        expiration (int): Time in seconds before the link expires. Default 2 minutes.

    Returns:
        str: Pre-signed URL pointing to the file to be downloaded
    """

    # Generate a pre-signed URL for the S3 object
    storage_options = infer_storage_options(filepath)
    protocol = storage_options["protocol"]
    filepath = storage_options["path"]

    filesystem = fsspec.filesystem(protocol=protocol)

    # The response contains the pre-signed URL
    return filesystem.url(path=filepath, expires=expiration)

"""
The MaitreD is responsible for showing patrons a fully customized menu of the
HeadChef's offering for this Dish

i.e. Display a web page detailing the processed data. This is the place to distill
important information based on your processed data set, and describe what it contains

Could include plots, figures, images, videos, etc.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path("/data")

st.title("US Census Data")


@st.cache
def load_data(path_to_data: Path) -> pd.DataFrame:
    """
    Load data from the /data directory

    Note:
        Streamlit caching does not play nicely with Modin[Dask] or Modin[Ray],
        so we use vanilla Pandas for now.

    Args:
        path_to_data (Path): Full path to data file

    Returns:
        pd.DataFrame: Pandas DataFrame containing data
    """
    return pd.read_csv(path_to_data)


# Load data
data = load_data(DATA_DIR / "census.csv")

st.subheader("Raw data")
st.write(data)

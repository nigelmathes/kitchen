"""
The MaitreD is responsible for showing patrons a fully customized menu of the
HeadChef's offering for this Dish

i.e. Display a web page detailing the processed data. This is the place to distill
important information based on your processed data set, and describe what it contains

Could include plots, figures, images, videos, etc.
"""
from typing import Dict

import pandas as pd
import streamlit as st

from sous_chef.sous_chef import SousChef

st.title("Demo Data")


@st.cache
def load_data() -> Dict[str, pd.DataFrame]:
    """
    Load the Dishes prepared by the HeadChef

    i.e. Load the data produced by this repository

    Note:
        Streamlit caching does not play nicely with Modin[Dask] or Modin[Ray],
        so we use vanilla Pandas for now.

    Returns:
        Dict[str, pd.DataFrame]: Dictionary of keys defined in
                                 head_chef/full_course.yaml, mapping to a
                                 Pandas DataFrame
    """
    sous_chef = SousChef()
    data_sources = sous_chef.prepare_ingredients()

    return data_sources


# Load data
all_data = load_data()
for data_name, data in all_data.items():
    st.subheader(f"{data_name}")
    st.write(data)

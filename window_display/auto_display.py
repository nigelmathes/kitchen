"""
This is the window display, showing off data making up this Dish.

i.e. A series of static HTML reports can be generated which will be served
     through the API served at this Restaurant
"""
from pathlib import Path

import pandas as pd

from dataprep.eda import create_report

STATIC_DIR = Path("/app/static_reports")


def create_window_display(
    data_to_display: pd.DataFrame, display_name: str
) -> None:
    """
    Create a window display from a table of data to advertise your dish

    i.e. Create an automatic EDA report for table data which will be viewable
         through the web API using dataprep

    Args:
        data_to_display (pd.DataFrame): The data to display in the EDA report
        display_name (str): Name of the data to display

    Returns:
        None, but saves an HTML report in the STATIC_DIR
    """
    dataprep_report = create_report(data_to_display, title="Window Display")
    dataprep_report.save(filename=f"{display_name}", to=str(STATIC_DIR))
    del dataprep_report

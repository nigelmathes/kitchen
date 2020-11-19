"""
This is the window display, showing off the input ingredients for this Dish.

i.e. A series of static HTML reports are generated which can be viewed through the
     API's served at this Restaurant
"""
from pathlib import Path

import pandas as pd
import sweetviz as sv

from dataprep.eda import create_report

STATIC_DIR = Path("/app/static_reports")
AVAILABLE_DISPLAY_TYPES = ["dataprep", "sweetviz"]


def create_window_display(
    data_to_display: pd.DataFrame, display_name: str, display_type: str = "dataprep",
) -> None:
    """
    Create a window display to advertise your dish

    i.e. Create an automatic EDA report for your data which will be viewable
         through the web API using one of the following auto-EDA tools:
             "sweetviz", "dataprep"

    Args:
        data_to_display (pd.DataFrame): The data to display in the EDA report
        display_name (str): Name of the data to display
        display_type (str): One of the above auto-EDA tools, defaults to "dataprep"

    Returns:
        None, but saves an HTML report in the STATIC_DIR
    """
    if display_type not in AVAILABLE_DISPLAY_TYPES:
        print(f"Invalid input report type {display_type}, defaulting to dataprep.")

        dataprep_report = create_report(data_to_display, title="dataprep Report")
        dataprep_report.save(filename="dataprep", to=STATIC_DIR)
        del dataprep_report

    elif display_type == "sweetviz":
        print(f"Generating {display_type} report for {display_name}")
        sweetviz_report = sv.analyze(data_to_display)
        sweetviz_report.show_html(filepath=STATIC_DIR / f"{display_name}.html",
                                  open_browser=False)
        del sweetviz_report

    else:
        print(f"Generating {display_type} report for {display_name}")
        dataprep_report = create_report(data_to_display, title="dataprep Report")
        dataprep_report.save(filename=f"{display_name}", to=STATIC_DIR)
        del dataprep_report

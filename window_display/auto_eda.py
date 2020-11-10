"""
These are the wait staff responsible for keeping patrons happy.

i.e. A series of static HTML reports are generated which can be viewed through the
     API's served at this Restaurant
"""
from pathlib import Path
import sweetviz as sv
import pandas as pd

from dataprep.eda import create_report

DATA_DIR = Path("/data")
STATIC_DIR = Path("/app/static_reports")

data = pd.read_csv(DATA_DIR / "census.csv")

# SweetViz report
print("Generating SweetViz Report")
sweetviz_report = sv.analyze(data)
sweetviz_report.show_html(filepath=STATIC_DIR / "sweetviz.html", open_browser=False)
del sweetviz_report

# dataprep reports
print("Generating dataprep Report")
dataprep_report = create_report(data, title='dataprep Report')
dataprep_report.save(filename='dataprep', to=STATIC_DIR)
del dataprep_report

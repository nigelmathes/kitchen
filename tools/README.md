# The Sous Chef's Tools
A series of data connectors for saving and loading data.
 
## Architecture
Every directory in `tools` corresponds to a Python-native data format, and 
within those directories the individual files correspond to the input data format.

For example: `pandas/csv_file.py` loads a CSV file into a Pandas DataFrame.
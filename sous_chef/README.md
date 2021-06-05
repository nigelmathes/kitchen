# The Sous Chef Prepares the Ingredients
I.e. the extract stage of your ETL process.

## The Sous Chef
In `sous_chef.py` is the `SousChef` class, which does all the prep work for the
 `HeadChef` (`head_chef/head_chef.py`). This class converts data sources into 
python-native objects.
 
The `SousChef` is in charge of reading the ingredients list in `ingredients.yaml`
, which you should edit with your input data. Specifically, you need to include the
following information in your ingredients list:

```yaml
# name_of_data is a name you choose, this can be anything
name_of_data:
  # location is the full path/URL to the data you want to read (extract)
  location: "s3://demo-supplier-data/titanic_train.csv"
  # raw_format is the file type of the data you want to read (extract), often
  # the file extension (e.g. for train.json, raw_format is "json")
  raw_format: "csv_file"
  # prepared_format is the Python data structure you want to load your data
  # into (e.g. for a Pandas DataFrame, this is "pandas.DataFrame")
  prepared_format: "pandas.DataFrame"
```

### Types available for `raw_format`:
`csv_file`, `json_file`, `yaml_file`, `text_file`, `joblib_file`, `parquet_file`

_More coming soon!_

### Types available for `prepared_format`:
`pandas`, `scikit`, `list`, `dict`

_More coming soon!_

# To run:
```bash
python -m sous_chef.sous_chef
```
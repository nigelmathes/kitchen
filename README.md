# Kitchen
A containerized kitchen to transform data processing into servable, discoverable, and
 understandable data products.
 
Combine the best open source utilities for Data Science & Engineering.

Start it up, and navigate to the following URL's to access information about your data:

```
localhost:81/docs      # Browsable API endpoints
localhost:81/dataprep  # dataprep dashboard (Auto-EDA)
localhost:81/sweetviz  # SweetViz dashboard (Auto-EDA)
localhost:80           # Streamlit dashboard (Customizable EDA)
```

## Installation
Clone repo, then:

```bash
docker-compose up --build kitchen
```

`TODO: Make as simple as possible.`

## Why did I choose ____ when I could have chosen ____?

### Streamlit vs. ???
- Streamlit is just great
- Best utility to build customizable dashboards in Python

https://github.com/streamlit/streamlit

### Automatic EDA: Dataprep vs. SweetViz vs. Pandas-Profiling
#### dataprep
- Generates HTML quickly
- HTML in browser loads slowly
- Generated reports contain all EDA I would want, except they don't show variable
 correlations in the variable sub-tabs. That said, the correlation plot does this.
- Plots generated have mouse-over capabilities

https://github.com/sfu-db/dataprep

#### SweetViz
- Generates HTML slowly
- HTML in browser loads quickly
- Generated reports contain most of the EDA I would want
- Plots do not have mouse-over
- Web page aspect ratios do not display well on non-1080p displays

https://github.com/fbdesignpro/sweetviz

#### Pandas-Profiliing
- Generates HTML slowly (unless minimal used)
- HTML in browser loads slowly (but faster than Dataprep)
- Generated reports lack many EDA features, such as correlations
- Plots do not have mouse-over 

https://github.com/pandas-profiling/pandas-profiling
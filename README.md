# Kitchen
A containerized kitchen to transform data processing into servable, discoverable, and
 understandable data products.
 
Combine the best open source utilities for Data Science & Engineering.

Start it up, and navigate to the following URL's to access information about your data:

```
localhost:81/docs      # Browsable API endpoints
localhost:8443         # Visual Studio Code IDE
localhost:8888         # Jupyter Lab Instance
localhost:80           # Streamlit dashboard (Customizable EDA)
```

## Installation
To start the development server with all the included utilities, clone the repo and then:

```bash
docker-compose up --build kitchen-dev
```

This will start the API server, the Visual Studio Code server, the Jupyter Lab server,
and the Streamlit server.

`TODO: Make as simple as possible.`
`TODO: Make local development as easy as cloud development.`

## What's Included?

### Custom EDA: Streamlit
- Build customizable dashboards in Python

https://github.com/streamlit/streamlit

### Automatic EDA: Dataprep
- Generates HTML reports with exhaustive, mouse-over-able plots

https://github.com/sfu-db/dataprep

### Visual Studio Code In Browser
- Run an IDE in browser 

https://github.com/cdr/code-server

### Jupyter Lab
- Run interactive Python notebooks in browser

https://github.com/jupyterlab/jupyterlab
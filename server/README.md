# The Server Serves the Dish from the Head Chef
I.e. Provide a series of API endpoints that let one inspect and download data produced
for this Dish

## The Server
A set of FastAPI endpoints serving data and web-viewable pages to inspect the data.
 
# To run:
```bash
hypercorn server.server:app --bind 0.0.0.0:81
```

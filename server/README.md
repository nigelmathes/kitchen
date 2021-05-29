# The Server Serves the Dish from the Head Chef
I.e. Provide a series of API endpoints that let one inspect and download data produced
by this Kitchen.

## The Server
A set of FastAPI endpoints serving data and web-viewable pages to inspect data served 
here.
 
# To run:
```bash
hypercorn server.server:app --bind 0.0.0.0:81
```

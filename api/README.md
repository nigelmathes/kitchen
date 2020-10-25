# Standalone API-Serving Utility
Should stand on its own to serve a set of FastAPI endpoints, which means this
 directory can be copied into any project and work. 
 
# To run:
```bash
hypercorn api.rest_endpoints:app --bind 0.0.0.0:81
```

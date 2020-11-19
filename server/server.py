"""
REST endpoints to discover, inspect, and acquire data produced in the data pod
"""
from pathlib import Path
from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount(
    "/reports", StaticFiles(directory="static_reports", html=True), name="reports"
)
templates = Jinja2Templates(directory="static_reports")


@app.get("/data_products")
async def get_data_products() -> JSONResponse:
    """
    Gets available data products

    Returns:
        JSONResponse: JSON serialized dictionary listing data sources as keys, with
                      schema as values
    """
    return JSONResponse("Not Implemented")


@app.get("/reports", response_class=HTMLResponse)
async def get_reports(request: Request) -> Jinja2Templates.TemplateResponse:
    """
    Display an index page which links to all generated reports

    Returns:
        Jinja2Templates.TemplateResponse: HTML page linking to data reports
    """
    path_to_html_reports = Path("/app") / "static_reports"

    available_reports = list(path_to_html_reports.glob("*.html"))

    reports = list()
    for report in sorted(available_reports):
        if "index.html" not in str(report):
            reports.append((f"{str(report.stem)}", f"reports/{str(report.name)}"))

    return templates.TemplateResponse(
        "index.html", {"request": request, "reports": reports}
    )

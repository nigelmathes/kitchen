"""
REST endpoints to discover, inspect, and acquire data produced in the kitchen
"""
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from head_chef.head_chef import HeadChef
from wait_staff.presigned_urls import create_presigned_url

app = FastAPI()

app.mount(
    "/reports", StaticFiles(directory="static_reports", html=True), name="reports"
)
templates = Jinja2Templates(directory="static_reports")


@app.get("/full_course")
async def get_full_course() -> JSONResponse:
    """
    Gets the full course served by the Head Chef
    i.e. Get pre-signed URLs to download all of the data products from this node

    Returns:
        JSONResponse: JSON serialized dictionary listing names of data sources as
                      keys and pre-signed URLs to these sources as values
    """
    head_chef = HeadChef()

    urls_to_deliver = {}
    for dish_name, dish in head_chef.full_course.items():
        urls_to_deliver[dish_name] = create_presigned_url(filepath=dish.location)

    return JSONResponse(content=urls_to_deliver)


@app.get("/reports", response_class=HTMLResponse)
async def get_reports(request: Request) -> Jinja2Templates.TemplateResponse:
    """
    Display an index page which links to all generated reports

    Returns:
        Jinja2Templates.TemplateResponse: HTML page linking to data reports
    """
    path_to_html_reports = Path("/app") / "static_reports"

    # Find static HTML reports files
    available_reports = list(path_to_html_reports.glob("*.html"))

    reports = list()
    for report in sorted(available_reports):
        if "index.html" not in str(report):
            reports.append((f"{str(report.stem)}", f"reports/{str(report.name)}"))

    # Link to the custom report as well
    reports.append(("Custom Report", "http://localhost:80"))

    return templates.TemplateResponse(
        "index.html", {"request": request, "reports": reports}
    )

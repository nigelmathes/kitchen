"""
REST endpoints to discover, inspect, and acquire data produced in the data pod
"""
from pathlib import Path
from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse

app = FastAPI()


@app.get("/data_products")
async def data_products() -> JSONResponse:
    """
    Gets available data products

    Returns:
        JSONResponse: JSON serialized dictionary listing data sources as keys, with
                      schema as values
    """
    return JSONResponse("Not Implemented")


@app.get("/sweetviz")
async def sweetviz_report() -> Union[HTMLResponse, PlainTextResponse]:
    """
    Shows the SweetViz report

    Returns:
        HTMLResponse: HTML in ../static_reports/sweetviz.html
    """
    # encoding='utf-8'
    path_to_html = Path("/app") / "static_reports" / "sweetviz.html"

    try:
        with open(path_to_html) as html_file:
            html_content = html_file.read()
    except FileNotFoundError:
        return PlainTextResponse(
            content="Your report hasn't been made yet! Check back later.",
            status_code=200
        )

    return HTMLResponse(content=html_content, status_code=200)


@app.get("/dataprep")
async def dataprep_report() -> Union[HTMLResponse, PlainTextResponse]:
    """
    Shows the DataPrep report

    Returns:
        HTMLResponse: HTML in ../static_reports/dataprep.html
    """
    # encoding='utf-8'
    path_to_html = Path("/app") / "static_reports" / "dataprep.html"

    try:
        with open(path_to_html) as html_file:
            html_content = html_file.read()
    except FileNotFoundError:
        return PlainTextResponse(
            content="Your report hasn't been made yet! Check back later.",
            status_code=200
        )

    return HTMLResponse(content=html_content, status_code=200)

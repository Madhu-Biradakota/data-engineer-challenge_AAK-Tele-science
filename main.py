from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import json
from world_bank_country_scraper import scrape_countries
from country_data_extractor import scrape_all_panels_selenium
from country_data_transformer import (
    parse_overview_data,
    parse_theme_data,
    parse_sdg_data
)

# Initialize the FastAPI app
app = FastAPI()

# Store country data in memory after first scraping
countries_data = scrape_countries()  # Scrape country names and URLs


@app.get("/")
def root():
    return {"message": "World Bank Country Data API. Use /country/{country_name} to fetch data."}


@app.get("/country/{country_name}")
def get_country_data(country_name: str):
    if country_name not in countries_data:
        raise HTTPException(status_code=404, detail="Country not found")

    country_url = countries_data[country_name]

    # Scrape the country data
    panel_data = scrape_all_panels_selenium(country_url)

    # Access the overview, theme, and SDG HTML panels from the dictionary
    overview_html = panel_data.get("overview_html")
    theme_html = panel_data.get("theme_panel_html")
    sdg_html = panel_data.get("sdg_panel_html")

    # Apply transformations
    overview_data = parse_overview_data(overview_html)
    theme_data = parse_theme_data(theme_html)
    sdg_data = parse_sdg_data(sdg_html)

    # Combine the final data
    response_data = {
        "country_name": country_name,
        "overview": overview_data,
        "by_theme": theme_data,
        "by_sdg_goal": sdg_data
    }

    # Use json.dumps with indent=4 for pretty-printed JSON
    formatted_json = json.dumps(response_data, indent=4)

    # HTML template with JavaScript for beautifying
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Country Data</title>
        <style>
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <h1>Country Data for {country_name}</h1>
        <pre>{formatted_json}</pre>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)
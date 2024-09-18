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
from fastapi.responses import JSONResponse
import json

# Initialize the FastAPI app
app = FastAPI()

# Store country data in memory after first scraping
countries_data = scrape_countries()  # Scrape country names and URLs


@app.get("/")
def root():
    return {"message": "World Bank Country Data API. Use /country/{country_name} to fetch data."}



@app.get("/countries", response_class=HTMLResponse)
def get_all_countries():
    total_countries = len(countries_data)
    country_list_html = ""

    # Build the HTML to mimic a JSON structure
    for country, link in countries_data.items():
        country_list_html += f'''
        <div style="margin-left: 20px;">
            "{country}": <a href="{link}" target="_blank">"{link}"</a>,
        </div>'''

    # Create the full HTML content with JSON-like styling
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Countries and Links</title>
        <style>
            body {{
                font-family: monospace;
                margin: 20px;
                background-color: #f4f4f4;
            }}
            h1 {{
                font-family: Arial, sans-serif;
                text-align: center;
            }}
            .json-block {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                margin-top: 20px;
            }}
            a {{
                text-decoration: none;
                color: #007bff;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .json-brace {{
                font-weight: bold;
            }}
            .json-key {{
                color: #d73a49;
            }}
            .json-string {{
                color: #032f62;
            }}
        </style>
    </head>
    <body>
        <h1>Total Countries: {total_countries}</h1>
        <div class="json-block">
            <div class="json-brace">{"{"}</div>
            {country_list_html.rstrip(",")}
            <div class="json-brace">{"}"}</div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
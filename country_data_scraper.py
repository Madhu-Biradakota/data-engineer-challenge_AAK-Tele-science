import requests
from bs4 import BeautifulSoup
from world_bank_country_scraper import scrape_countries  # Import the function
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_overview_data(country_url):
    # Fetch the HTML content of the country page
    response = requests.get(country_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Initialize a dictionary to store the overview data
    overview_data = []
    try:
        # Find the overview panel content (assuming react-tabs-1 holds the overview section)
        overview_panel = soup.find('div', {'id': 'react-tabs-1'})  # Adjust based on the panel ID for "Overview"
        #print(overview_panel)
        if overview_panel:
            # Find all indicators (each with a class 'indicator-item')
            indicators = overview_panel.find_all('div', class_='indicator-item')
            for indicator in indicators:
                indicator_data = {}

                # Extract the title of the indicator (e.g., "Social", "Economic", etc.)
                title = indicator.find('h1')
                if title:
                    indicator_data['Topic'] = title.text.strip()

                # Extract individual indicator data within each section
                indicator_items = indicator.find_all('div', class_='indicator-item__wrapper')
                for item in indicator_items:
                    item_data = {}

                    # Extract the title of the individual indicator (e.g., Poverty headcount ratio)
                    title = item.find('div', class_='indicator-item__title')
                    if title:
                        item_data['Indicator'] = title.text.strip()

                    # Extract the most recent value (check if there is a span with data or "No data available")
                    data_info = item.find('div', class_='indicator-item__col--middle')
                    #print(data_info)
                    if data_info:
                        # Check if there is actual data or if it says "No data available"
                        no_data = item.find('p', class_='indicator-item__data-info-empty')
                        if no_data:
                            item_data['Most recent value'] = no_data.find('span').text.strip()
                        else:
                            # Find the correct span tag that contains the actual value
                            recent_value = data_info.find('div', class_='indicator-item__data-info')
                            if recent_value:
                                value_span = recent_value.find('span')
                                if value_span:
                                    item_data['Most recent value'] = value_span.text.strip()

                                # Extract the year for the data (if available)
                                year_info = item.find('p', class_='indicator-item__data-info-year')
                                if year_info:
                                    item_data['Year'] = year_info.text.strip()

                    # Add individual indicator data to the indicator_data dictionary
                    if 'Indicators' not in indicator_data:
                        indicator_data['Indicators'] = []
                    indicator_data['Indicators'].append(item_data)

                # Add the section and its indicators to the overview data list
                overview_data.append(indicator_data)
        else:
            overview_data.append({"error": "No Overview data found"})

    except Exception as e:
        print(f"Error while scraping overview data: {e}")
        overview_data.append({"error": "Error occurred"})

    return overview_data



# Example usage with a country URL
if __name__ == "__main__":
    # Replace this with the actual country URL you want to scrape
    country_url = "https://data.worldbank.org/country/india?view=chart"

    # Call the function to scrape "By Theme" data for the country
    theme_data = scrape_by_theme_data_selenium(country_url)

    # Print the scraped data
    print(theme_data)

# Function to scrape all data for a country
def scrape_country_data(country):
    print(f"Scraping data for {country['name']}...")

    # Scrape data from all tabs
    overview_data = scrape_overview_data(country['url'])
    #theme_data = scrape_by_theme_data_selenium(country['url'])
    #sdg_data = scrape_by_sdg_goal_data(country['url'])

    return {
        "overview": overview_data,
        #"by_theme": theme_data,
        #"by_sdg_goal": sdg_data
    }


# Main function to scrape all countries
def scrape_all_countries():
    # Get country URLs from world_bank_country_scraper.py
    countries = scrape_countries()

    all_country_data = {}
    limit = 5
    for country_name, country_url in countries.items():
        if limit > 0:
            country = {"name": country_name, "url": country_url}
            country_data = scrape_country_data(country)
            all_country_data[country_name] = country_data
            limit = limit - 1

    return all_country_data


if __name__ == "__main__":
    # Scrape data for all countries
    all_data = scrape_all_countries()

    # Optionally, you can print or save the data
    for country, data in all_data.items():
        print(f"Data for {country}:")
        print(data)
import requests
from bs4 import BeautifulSoup

def scrape_countries(url="https://data.worldbank.org/country"):
    # Fetch the HTML content of the page
    response = requests.get(url)
    html_code = response.content  # This now contains the live HTML data from the webpage
    # Create BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_code, 'html.parser')
    # Locate all sections with class 'nav-item' that contain countries
    country_sections = soup.find_all('section', class_='nav-item')

    # Dictionary to store country names and URLs
    countries_data = {}

    # Loop through each section and extract the countries and URLs
    for section in country_sections:
        country_items = section.find_all('li')
        # Loop through each country item and extract the data
        for item in country_items:
            if item.a:  # Ensure the <a> tag exists
                country_name = item.a.text.strip()  # Extract the country name
                country_url = f"https://data.worldbank.org{item.a['href']}"  # Construct the full URL
                countries_data[country_name] = country_url

    return countries_data
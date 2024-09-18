from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


# Function to scrape all content (Overview, By Theme, By SDG Goal) in one shot
def scrape_all_panels_selenium(country_url):
    # Set up WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Navigate to the country's page
        driver.get(country_url)

        # 1. Extract the Overview HTML immediately (no need to click anything)
        overview_panel = driver.find_element(By.ID, "react-tabs-1")
        overview_panel_html = overview_panel.get_attribute('innerHTML')

        # 2. Click on the "By Theme" tab to load and extract its content
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[span[text()='By Theme']]"))
        )

        theme_tab = driver.find_element(By.XPATH, "//li[span[text()='By Theme']]")
        driver.execute_script("arguments[0].scrollIntoView(true);", theme_tab)
        driver.execute_script("arguments[0].click();", theme_tab)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "react-tabs-3"))
        )
        theme_panel = driver.find_element(By.ID, "react-tabs-3")
        theme_panel_html = theme_panel.get_attribute('innerHTML')

        # 3. Click on the "By SDG Goal" tab and extract its content
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[span[text()='By SDG Goal']]"))
        )

        sdg_tab = driver.find_element(By.XPATH, "//li[span[text()='By SDG Goal']]")
        driver.execute_script("arguments[0].scrollIntoView(true);", sdg_tab)
        driver.execute_script("arguments[0].click();", sdg_tab)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "react-tabs-5"))
        )
        sdg_panel = driver.find_element(By.ID, "react-tabs-5")
        sdg_panel_html = sdg_panel.get_attribute('innerHTML')

    except Exception as e:
        print(f"Error while scraping panels: {e}")
        overview_panel_html = theme_panel_html = sdg_panel_html = None

    finally:
        driver.quit()

    return {
        "overview_html": overview_panel_html,
        "theme_panel_html": theme_panel_html,
        "sdg_panel_html": sdg_panel_html
    }



# Test for a specific country (e.g., Afghanistan)
#country_url = "https://data.worldbank.org/country/afghanistan"
#country_data = scrape_all_panels_selenium(country_url)

#parse_overview_data(country_data['overview_html'])
#parse_sdg_data(country_data['theme_panel_html'])
#parse_theme_data(country_data['theme_panel_html'])


# Output the extracted content
#print(country_data['overview_html'])
#print(country_data['theme_panel_html'])
#print(country_data['sdg_panel_html'])


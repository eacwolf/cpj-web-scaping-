
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up ChromeDriver (Correct path for EC2)
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# URL to scrape
url = "https://cpj.org/data/missing/?status=Missing&start_year=2025&end_year=2025&group_by=location"
driver.get(url)

def scrape_page():
    """Scrapes data from the current page."""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-report-builder-table"))
        )
        table = driver.find_element(By.CLASS_NAME, "js-report-builder-table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        missing_journalists = []
        for row in rows[1:]:  # Skip header row
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) >= 4:
                name = columns[0].text.strip()
                organization = columns[1].text.strip()
                date = columns[2].text.strip()
                location = columns[3].text.strip()
                profile_link = columns[0].find_element(By.TAG_NAME, "a").get_attribute("href")

                missing_journalists.append({
                    "Name": name,
                    "Organization": organization,
                    "Date": date,
                    "Location": location,
                    "Profile Link": profile_link
                })
        return missing_journalists

    except Exception as e:
        print(f"Error scraping page: {e}")
        return []

def click_next_page():
    """Clicks the 'Next' button if available and loads the next page."""
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next')]"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)

        if "disabled" in next_button.get_attribute("class"):
            print("Reached the last page.")
            return False

        driver.execute_script("arguments[0].click();", next_button)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".js-report-builder-table tr:nth-child(2) td:nth-child(1)"))
        )
        time.sleep(2)

        return True

    except TimeoutException:
        print("Timeout waiting for the next page to load. Assuming we're on the last page.")
        return False
    except Exception as e:
        print(f"Error clicking 'Next': {e}")
        return False

# Scrape multiple pages
all_missing_journalists = []
page_number = 1
max_pages = 4  # Set the max number of pages to scrape

while page_number <= max_pages:
    print(f"Scraping page {page_number}...")
    journalists = scrape_page()
    all_missing_journalists.extend(journalists)

    if page_number < max_pages:
        if not click_next_page():
            break
    page_number += 1

# Debugging: Print scraped data before saving
print("Scraped Data:", all_missing_journalists)

# Save data to CSV
csv_file_path = "missing_journalists.csv"
field_names = ["Name", "Organization", "Date", "Location", "Profile Link"]

with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    for journalist in all_missing_journalists:
        writer.writerow(journalist)

print(f"Data saved to {csv_file_path}")

# Close the browser
driver.quit()

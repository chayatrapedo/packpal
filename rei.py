"""
#1
import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://www.target.com/c/adult-backpacks-luggage/-/N-55ks5"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the links to the backpacks
backpack_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if '/p/' in href:  # Assuming product links contain '/p/'
        full_url = "https://www.target.com" + href  # Construct the full URL
        backpack_links.append(full_url)

# Display the backpack links
for link in backpack_links:
    print(link)

"""
"""
#2
import requests
from bs4 import BeautifulSoup

# Function to get backpack links from a single page
def get_backpack_links(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    soup = BeautifulSoup(response.text, 'html.parser')
    backpack_links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/p/' in href:  # Assuming product links contain '/p/'
            full_url = "https://www.target.com" + href  # Construct the full URL
            backpack_links.append(full_url)
    
    return backpack_links

# Function to find the URL of the next page
def find_next_page_url(soup):
    next_button = soup.find('a', {'aria-label': 'next page'})  # Find the "Next" button/link
    if next_button and 'href' in next_button.attrs:
        return "https://www.target.com" + next_button['href']
    return None

# Starting URL (first page)
start_url = "https://www.target.com/c/adult-backpacks-luggage/-/N-55ks5"

all_backpack_links = []
current_url = start_url

i = 1
while current_url:
    print(f"\n CUR PAGE URL {i}: {current_url}\n")
    response = requests.get(current_url)
    response.raise_for_status()  # Check if the request was successful
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get links from the current page
    backpack_links = get_backpack_links(current_url)
    all_backpack_links.extend(backpack_links)

    # Find the next page URL
    current_url = find_next_page_url(soup)
    i += 1

# Display the backpack links
for link in all_backpack_links:
    print(link)
    
print(len(all_backpack_links))
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium using Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless mode if needed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to get backpack links from a specific nested div using Selenium
def get_backpack_links(driver):
    backpack_links = []
    # Wait until the product grid is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test='productGrid']"))
    )
    
    # Find all anchor tags within the product grid
    product_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'styles__StyledListProduct')]//a[contains(@href, '/p/')]")
    for element in product_elements:
        href = element.get_attribute('href')
        if href not in backpack_links:  # Check for duplicates
            backpack_links.append(href)
    return backpack_links

# Function to find and click the "Next" button
def find_and_click_next_page(driver):
    try:
        # Wait until the "Next" button is present and clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next page']"))
        )
        next_button.click()  # Click the "Next" button
        return True
    except:
        return False

# Starting URL (first page)
start_url = "https://www.target.com/c/adult-backpacks-luggage/-/N-55ks5"

all_backpack_links = []
driver.get(start_url)

while True:
    # Get links from the current page
    backpack_links = get_backpack_links(driver)
    all_backpack_links.extend(backpack_links)

    # Attempt to go to the next page
    if not find_and_click_next_page(driver):
        break  # Exit loop if no next page is found

    # Optional: Add a delay to mimic human browsing and prevent being blocked
    time.sleep(2)

# Remove duplicate links
all_backpack_links = list(set(all_backpack_links))

# Close the browser
driver.quit()

# Display the backpack links
for link in all_backpack_links:
    print(link)

print(f"Total backpacks found: {len(all_backpack_links)}")


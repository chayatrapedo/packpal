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
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium using Chrome WebDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment this line to run in headless mode if needed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to get backpack links using staged search
def get_backpack_links(driver):
    backpack_links = []
    try:
        # Wait for the main container that includes all product sections
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test='product-grid-container']"))
        )
        
        # Find the main product grid container
        product_grid = driver.find_element(By.CSS_SELECTOR, "div[data-test='product-grid-container']")

        # Find all product links within the product grid
        product_elements = product_grid.find_elements(By.CSS_SELECTOR, "a[data-test='product-title']")
        
        for element in product_elements:
            href = element.get_attribute('href')
            if href not in backpack_links:  # Check for duplicates
                backpack_links.append(href)
        
    except TimeoutException:
        print("TimeoutException: Product elements could not be found within the given time.")
    return backpack_links

# Starting URL (first page)
start_url = "https://www.target.com/c/adult-backpacks-luggage/-/N-55ks5"

all_backpack_links = []
driver.get(start_url)

# Debug: Print current URL
print(f"Current URL: {driver.current_url}")

# Wait for page to fully load (useful for dynamic content)
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test='product-grid-container']"))
)

# Debug: Execute JS to check if product grid is loaded
is_product_grid_present = driver.execute_script("return document.querySelector('div[data-test=\"product-grid-container\"]') !== null;")
print(f"Is product grid present: {is_product_grid_present}")

# Get links from the current page
backpack_links = get_backpack_links(driver)
all_backpack_links.extend(backpack_links)

# Debug: Print the number of links found
print(f"Number of backpack links found: {len(backpack_links)}")

# Remove duplicate links
all_backpack_links = list(set(all_backpack_links))

# Close the browser
driver.quit()

# Display the backpack links
for link in all_backpack_links:
    print(link)

print(f"Total backpacks found: {len(all_backpack_links)}")

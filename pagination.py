import requests
from bs4 import BeautifulSoup

def get_next_page_links(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the pagination container
        pagination = soup.find('div', {'data-test': 'pagination'})

        # If pagination container exists, find all page links
        if pagination:
            next_page_links = []
            for a in pagination.find_all('a', href=True):
                link = "https://www.target.com" + a['href']
                next_page_links.append(link)
            return next_page_links
        else:
            print("Pagination not found on the page.")
            return []
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

# The URL of the Target backpacks page
initial_url = "https://www.target.com/c/adult-backpacks-luggage/-/N-55ks5Zxyok5Zqvwd2Zmfp85?moveTo=product-list-grid&Nao=0"

# Call the function to get the next page links
next_page_links = get_next_page_links(initial_url)

# Print the links to the next pages
for link in next_page_links:
    print(link)

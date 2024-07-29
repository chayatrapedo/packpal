# GET TARGET DATA FROM THE BACKEND
from playwright.sync_api import sync_playwright
import requests

def get_cookie_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.target.com/c/adult-backpacks-luggage/-/N-55ks5")
        # Ensure this is the correct index or method to retrieve the cookie
        cookies = context.cookies()
        # Example to find the specific cookie; adjust as necessary
        cookie_for_requests = next(cookie['value'] for cookie in cookies if cookie['name'] == 'TealeafAkaSid')
        browser.close()
    return cookie_for_requests

def req_with_cookie(cookie_for_requests):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    cookies = {
        'TealeafAkaSid': cookie_for_requests
    }
    response = requests.get(
        "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2",
        headers=headers,
        cookies=cookies,
        params={
            'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
            'category': '55ks5',
            'channel': 'WEB',
            'count': '24',
            'default_purchasability_filter': 'true',
            'include_dmc_dmr': 'true',
            'include_sponsored': 'true',
            'new_search': 'false',
            'offset': '0',
            'page': '%2Fc%2F55ks5',
            'platform': 'desktop',
            'pricing_store_id': '1330',
            'spellcheck': 'true',
            'store_ids': '1330,2381,1865,1263,3329',
            'useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'visitor_id': '018F144760790201A80190502CD73ED4',
            'zip': '07601'
        }
    )
    return response

if __name__ == '__main__':
    try:
        data = req_with_cookie(get_cookie_playwright())
        print(data.text)  # Print response text for debugging
    except Exception as e:
        print(f"An error occurred: {e}")

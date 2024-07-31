# Get information from shopfiy

import requests
import json
import pandas as pd
import re
import xml.etree.ElementTree as ET


def clean_html(body):
    ans = re.sub(r'<[^>]+>', '', body)
    print(ans)
    return ans

def get_json(url): # split by " | " to brand, url, producttype
    
    r = requests.get(url)
    data = r.json()
    
    all_backpacks = []
    
    # picking the categories that I want
    for item in data["products"]:
        title = item["title"]
        product_type = item["product_type"]
        tags = item["tags"]
        body = item["body_html"]
        try:
            imagesrc = item["images"][0]["src"]
        except:
            imagesrc = "None"
                
        num_colors = len(item["variants"])
        colors = []
        for variant in item["variants"]:
            colors += [variant["title"]]
            price = variant["price"]
            available = variant["available"]
            
        if "pack" in product_type.lower():
            
            product = {
                "brand": "Tomtoc",
                "title": title,
                "image_link": imagesrc,
                "num_colors": num_colors,
                "colors": colors,
                "dimensions": "",
                "capacity": "",
                "laptop": 0, # will change to a number
                "carry on": 0,
                "weight": 0,
                "price": price,
                # will delete these later, but get info from them initially
                "tags": tags,
                "desc": clean_html(body),
            }
            
            all_backpacks.append(product)
            
    df = pd.DataFrame(all_backpacks)
    df.to_csv("tomtoc.csv")
    print(f"saved {len(all_backpacks)}")          
    
if __name__ == "__main__":
    url = "https://tomtoc.com/products.json?limit=250"
    get_json(url)
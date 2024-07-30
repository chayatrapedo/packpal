import json

def findData():
    
    with open("output.json", "r") as file:
        data = json.load(file)
        
    all_products = data["data"]["search"]["products"]
    print(len(all_products))
    #for product in all_products:
        #print(product, "\n\n")
    
    
findData()
import pandas as pd
import re

# Load the CSV file
file_path = '/Users/chayatrapedo/Desktop/Git Repositories/packpal/backpacks.csv'
df = pd.read_csv(file_path)

# Improved function to extract dimensions, capacity, and laptop size
def extract_info_v4(desc):
    # Regex patterns for dimensions, capacity, and laptop size
    dim_pattern = re.compile(r'\b(\d{1,2}\s*[xX*]\s*\d{1,2}\s*[xX*]\s*\d{1,2})\s*(inches|inch|in)\b', re.IGNORECASE)
    cap_pattern = re.compile(r'(\d{1,2})\s*(liters|l)\b', re.IGNORECASE)
    laptop_pattern = re.compile(r'(\d{1,2})\s*(inch|inches|in)\s*(laptop|screen|display)?\b', re.IGNORECASE)
    
    dimensions = None
    capacity = None
    laptop_size = None
    
    # Search for dimensions
    dim_match = dim_pattern.search(desc)
    if dim_match:
        dimensions = dim_match.group(1).replace(' ', '')  # Remove any spaces around 'x' or '*'
    
    # Search for capacity
    cap_match = cap_pattern.search(desc)
    if cap_match:
        capacity = cap_match.group(1) + ' liters'
    
    # Search for laptop size
    laptop_match = laptop_pattern.search(desc)
    if laptop_match:
        laptop_size = laptop_match.group(1) + ' inches'
    
    return dimensions, capacity, laptop_size

# Apply the improved extraction function to the 'desc' column
df[['dimensions', 'capacity', 'laptop']] = df['desc'].apply(lambda x: pd.Series(extract_info_v4(str(x))))

# Save the updated dataframe to a new CSV file
df.to_csv('/Users/chayatrapedo/Desktop/Git Repositories/packpal/updated_backpacks.csv', index=False)

# Display the updated dataframe
print(df[['desc', 'dimensions', 'capacity', 'laptop']].head())

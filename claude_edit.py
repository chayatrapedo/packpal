import pandas as pd
import re

def extract_info_v5(desc):
    # Regex patterns for dimensions, capacity, and laptop size
    dim_pattern = re.compile(r'\b(\d{1,2}(?:\.\d{1,2})?)\s*[xX*]\s*(\d{1,2}(?:\.\d{1,2})?)\s*[xX*]\s*(\d{1,2}(?:\.\d{1,2})?)\s*(inches|inch|in|cm)\b', re.IGNORECASE)
    cap_pattern = re.compile(r'(\d{1,2}(?:\.\d{1,2})?)\s*(liters?|l)\b', re.IGNORECASE)
    laptop_pattern = re.compile(r'(\d{1,2}(?:\.\d{1,2})?)\s*(inch|inches|in)?\s*(laptop|screen|display)?\b', re.IGNORECASE)
    
    dimensions = None
    capacity = None
    laptop_size = None
    
    # Search for dimensions
    dim_match = dim_pattern.search(desc)
    if dim_match:
        unit = 'in' if dim_match.group(4).lower().startswith('in') else 'cm'
        dimensions = f"{dim_match.group(1)}x{dim_match.group(2)}x{dim_match.group(3)} {unit}"
    
    # Search for capacity
    cap_match = cap_pattern.search(desc)
    if cap_match:
        capacity = f"{cap_match.group(1)} L"
    
    # Search for laptop size
    laptop_match = laptop_pattern.search(desc)
    if laptop_match:
        laptop_size = f"{laptop_match.group(1)}\""
    
    return dimensions, capacity, laptop_size

# Load the CSV file
file_path = '/Users/chayatrapedo/Desktop/Git Repositories/packpal/backpacks.csv'
df = pd.read_csv(file_path)

# Apply the improved extraction function to the 'desc' column
df[['dimensions', 'capacity', 'laptop']] = df['desc'].apply(lambda x: pd.Series(extract_info_v5(str(x))))

# Save the updated dataframe to a new CSV file
df.to_csv('/Users/chayatrapedo/Desktop/Git Repositories/packpal/updated_backpacks_c.csv', index=False)

# Display the updated dataframe
print(df[['desc', 'dimensions', 'capacity', 'laptop']].head())
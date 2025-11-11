import requests
import os
import json
import time

# -----------------------------------------------------------
# Script: extract_data.py
# Description: Extracts product data from the Open Food Facts API 
#              and saves it locally as a JSON file.
# -----------------------------------------------------------

# Base API endpoint for Open Food Facts search
base_url = 'https://world.openfoodfacts.org/api/v2/search'

# List of fields to be extracted from the API
fields = [
    'code', 'product_name', 'brands', 'categories',
    'ingredients_text', 'nutriments', 'labels', 'countries',
    'nutrition_grade_fr', 'nova_group'
]




def get_data(base_url, fields):
    """
    Fetches product data from the Open Food Facts API in multiple pages.
    
    Args:
        base_url (str): The base URL of the API endpoint.
        fields (list): List of fields for the API request.
    
    Returns:
        list: A list of product dictionaries fetched from the API.
    
    Raises:
        requests.exceptions.RequestException: If an API request fails.
    """
    # Default request parameters
    params = {
    'fields': ','.join(fields),  # Join fields into a comma-separated string
    'page': 1,
    'page_size': 100
    }

    result_set = []
    counter = 0

    # Iterate through 100 pages (10,000 products if each page = 100)
    for page in range(1, 101):
        params['page'] = page
        try:
            # Send GET request
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise error for failed requests

            # Parse JSON response
            result = response.json()
            result_set.extend(result['products'])  # Add products to the main list
            
            # Log progress every 10 pages and pause for rate-limiting
            if page % 10 == 0:
                counter += 10
                print(f"✔️ {counter} pages pulled")
                time.sleep(60)
                
        except requests.exceptions.RequestException as e:
            # Re-raise any HTTP/network error to stop execution
            raise e
        
    # Return results summary
    if result_set:
        print(f"✔️ Successfully pulled {len(result_set)} products")
        return result_set
    

def save_to_json(data, path):
    """
    Saves extracted data to a JSON file in a specified path.
    
    Args:
        data (list or dict): The data to be saved as JSON.
        path (str): File path for saving the JSON data.
    
    Returns:
        None
    """
    print("🔃 Data is being saved to JSON file")

    # Ensure directory exists before saving
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
        
    # Save data to file using UTF-8 encoding
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    
    print(f"✔️ File successfully saved to {path}")


# ----------------------------------------------------------------
# Main script execution
# ----------------------------------------------------------------
if __name__ == "__main__":
    # Fetch and save data only when executed directly (not imported)
    result_data = get_data(base_url, fields)
    save_to_json(result_data, './data/raw_data.json')


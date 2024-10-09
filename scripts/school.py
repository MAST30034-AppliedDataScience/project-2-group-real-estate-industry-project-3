import os
import pandas as pd
import requests
from io import StringIO

# URL for the school dataset
url_school = "https://www.education.vic.gov.au/Documents/about/research/datavic/dv346-schoollocations2023.csv"

# Define the file path where the dataset will be saved
file_path_school = "../data/landing/dv346-schoollocations2023.csv"

# Create the directories if they don't exist
os.makedirs(os.path.dirname(file_path_school), exist_ok=True)

try:
    # Downloading the dataset with SSL verification disabled
    response = requests.get(url_school, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Reading the content into a pandas DataFrame
        school_locations_df = pd.read_csv(StringIO(response.text), encoding='ISO-8859-1')
        
        # Saving the dataset to the specified location
        school_locations_df.to_csv(file_path_school, index=False)
        
        print(f"Dataset successfully downloaded and saved to {file_path_school}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")

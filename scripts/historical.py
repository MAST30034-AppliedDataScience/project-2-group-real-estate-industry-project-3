# Written by Daksh Agrawal

# Download excel files from the web and save them to the local directory
import requests
import os


def download_file(url, local_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Write the content to the local file
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved to {local_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")


url = 'https://www.dffh.vic.gov.au/moving-annual-rents-suburb-march-quarter-2023-excel'
local_path = '../data/landing/historical_data.xlsx'
download_file(url, local_path)

url = "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/development-activity-monitor/exports/csv?delimiter=%2C"
local_path = '../data/landing/development_activity.csv'
download_file(url, local_path)

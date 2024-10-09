# written by: Hanshi Tang
# Description: This script downloads an income file from the Australian Bureau of Statistics (ABS) website and saves it to the data/landing directory.
import os
import requests
import pandas as pd

# Direct download link to the Excel file (ensure the link is valid)
direct_file_link = "https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2020-21-financial-year/Table%203%20-%20Employee%20income%2C%20earners%20and%20summary%20statistics%20by%20geography%2C%202016-17%20to%202020-21.xlsx"

# Downloading the Excel file
response = requests.get(direct_file_link)

# Define the file path to save the downloaded file
file_path = "../data/landing/Table 2 - Total income distribution by geography, 2020-21.xlsx"

# Ensure the directory exists, create it if necessary
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Save the file to the specified location
with open(file_path, 'wb') as file:
    file.write(response.content)

print(f"File downloaded successfully and saved to {file_path}")

# Now load the Excel file into a pandas DataFrame
personal_income_df = pd.read_excel(file_path)

# Optional: Saving it again without modification
personal_income_df.to_excel(file_path, index=False)

print("File processed and saved as Excel.")

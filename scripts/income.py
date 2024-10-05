import os
import requests
import pandas as pd
from io import BytesIO

# Directory to save the Excel file
output_relative_dir = '../data/landing'

# Corrected file URL for downloading the Excel file
url = 'https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2020-21-financial-year/Table%202%20-%20Total%20income%20distribution%20by%20geography%2C%202020-21.xlsx'

# Download the Excel file content directly into memory
response = requests.get(url)

if response.status_code == 200:
    # Load the Excel content into a pandas ExcelFile object directly from memory
    xls = pd.ExcelFile(BytesIO(response.content))

    # Get all sheet names (table names)
    table_names = xls.sheet_names
    print("Sheet names (tables and other data):", table_names)

    # Define the output Excel file path
    excel_output_path = os.path.join(output_relative_dir, 'Table 2 - Total income distribution by geography, 2020-21.xlsx')

    # Use ExcelWriter to save all sheets into a single Excel file (default engine: openpyxl)
    with pd.ExcelWriter(excel_output_path, engine='openpyxl') as writer:
        # Iterate over each sheet and write it to the same Excel file
        for sheet in table_names:
            # Read the sheet into a DataFrame
            df = pd.read_excel(xls, sheet_name=sheet)
            
            # Write the DataFrame to the Excel file with its sheet name
            df.to_excel(writer, sheet_name=sheet, index=False)

    print(f"All sheets saved successfully into {excel_output_path}")

else:
    print(f"Failed to download the file. Status code: {response.status_code}")

import pandas as pd

# Downloading the dataset into a pandas DataFrame
# Replace 'direct_csv_link' with the actual link to the CSV file from the ABS page
direct_csv_link = "https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/latest-release#data-downloads"
personal_income_df = pd.read_csv(direct_csv_link, encoding='ISO-8859-1')

# Saving the dataset to the specified location
file_path = "../data/landing/Table 2 - Total income distribution by geography, 2020-21.xlsx"
personal_income_df.to_excel(file_path, index=False)


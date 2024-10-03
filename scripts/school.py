import pandas as pd

# URL for the dataset
url_school = "https://www.education.vic.gov.au/Documents/about/research/datavic/dv346-schoollocations2023.csv"

# Downloading the dataset into a pandas DataFrame
school_locations_df = pd.read_csv(url_school, encoding='ISO-8859-1')

# Saving the dataset to the specified location
file_path_school = "../data/landing/dv346-schoollocations2023.csv"
school_locations_df.to_csv(file_path_school, index=False)


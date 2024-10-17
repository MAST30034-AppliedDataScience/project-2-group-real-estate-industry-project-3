# Generic Real Estate Consulting Project

**Team Members:**
- Anushka Pathak (1230592)
- Elaine Zhang (1355970)
- Koquiun Li Lin (1319881)
- Hanshi Tang (1266337)
- Daksh Agrawal (1340113)

See the `scrape.py` file in the `scripts` directory to get started scraping data. 

**Research Goal:** 

Our primary research goal is to answer the following questions:
1. What are the most important internal and external features in predicting rental prices? (This
can be at the granularity of the groups’ choosing)
2. What are the top 10 suburbs with the highest predicted growth rate?
3. What are the most liveable and affordable suburbs according to your chosen metrics?

## Setup

Python 3 dependencies:

* Pyspark
* Pandas, Numpy
* Seaborn, matplotlib.pyplot
* Scikit Learn
* Beautiful Soup
* statsmodels

We provide a requirement.txt including all of the libraries used. Set up the environment by running:
```
pip install -r requirements.txt
```

## Pipeline
To Scrape the data off of https://www.domain.com.au/, run the `domain_scrape.py` script. This will create a `scraped_data` directory in the `data` directory. The script will scrape the data for all properties in Victoria and store the data in the `scrape_data` directory containing JSON files, postcode wise. To make the data interpretable, run these notebooks in the following order:
1. `preprocess_domain_1.ipynb`: This notebook extracts the prices and other details, does basic imputation and attaches the SA2 area to each property and stores the data in `data/raw/domain.csv`.
2. `preprocess_domain_2.ipynb`: This notebook does some type conversion and further imputation, outlier removal and stores the data in `data/curated/domain_data.csv`.
3. `eda_domain.ipynb`: This notebook provides an exploratory data analysis of the domain dataset, including visualizations of the distribution of rental prices, the number of bedrooms, bathrooms, parking etc.

In terms of the **parks and reservation** external dataset, please navigate to the `notebooks` directory and run the `data_download_parkres_&_property_lost.ipynb` notebook to obtain all of related datasets.

After downloading the data, remain in the `notebooks` directory and run the notebooks in the specified order:
1. `sa2_district_boundaries.ipynb`: This notebook displays the SA2 boundaries of each district in Victoria, provides visualizations of those areas, and stores all shape data in the `data/landing/boundaries/Victoria` directory.
2. `parkres_sa2_matching.ipynb`: This notebook finds the corresponding sa2_name and postcode for each park and reservation as required, implements geospatial analysis, and stores the CSV data in the `data/curated/parkres` directory.
3. `parkres_domain_merge.ipynb`: This notebook merges two datasets: the parks and reservations dataset and the domain rental dataset, then stores the merged dataset in the `data/curated/parkres` directory.
4. `parkres_domain_analysis.ipynb`: This notebook calculates the distance between each property and the nearest park and reservation. It performs statistical analysis on the merged dataset to assess the significance of the distance of parks and reservations on rental prices, primarily focusing on correlation.

In terms of the **crimes: property lost** external dataset, please navigate to the `notebooks` directory and also run the `data_download_parkres_&_property_lost.ipynb` notebook to obtain all of related datasets.

After downloading the data, remain in the `notebooks` directory and run the notebooks in the specified order:
1. `property_lost_sa2_matching.ipynb`: This notebook finds the corresponding sa2_name for each property lost incident, and shows the top sa2 areas where property lost frequency is the top and the least. The matching dataset is stored in the `data/curated/property_data` directory.
2. `property_lost_further_analysis.ipynb`: This notebook conducts a detailed analysis of the relationship between the frequency of property loss and the SA2 area in which the property is located. It also explores the correlation between these variables. The top SA2 areas with high crime frequency rates are identified.

In terms of the **schools** external dataset, please navigate to the `notebooks` directory and also run the `school_download.ipynb` script to obtain all of related datasets. 

After downloading the data, please navigate to the `notebooks` directory and run the notebooks in the specified order: 
1. `school_zone.ipynb`: This notebook processes the school zone data. 

2. `school_distance.ipynb`: This notebook calculates the distance between each property and the nearest school. It also visualizes the distribution of the distances and stores the processed data in the `data/curated/school_data.csv` file.


In terms of the **income** external dataset, please navigate to the `notebook` directory and also run the `income_download.ipynb` to obtain all of related datasets.

After downloading the data, please navigate to the `notebooks` directory and run the notebooks in the specified order: 

1. `income.ipynb`: This notebook preprocesses the income data and stores the processed data in the `../data/curated/income.parquet` file.


In terms of the **population & shopping centres & recreation** external dataset, please navigate to the `notebooks` directory and also run the `Data_download_pop_shopping_recreation` notebook to obtain all of related datasets.

After downloading the data, remain in the `notebooks` directory and run the notebook:
1. `SA2_EDA_pop_shopping_recreation`: This notebook processes the datasets as mentioned above and finds the relationships between rent and population, as well as shopping centres and recreations in a SA2 district. All processed external datasets are then stored in `data/curated/`.

In terms of the **public transport & hospitals** external dataset, please navigate to the `notebooks` directory and also run the `Data_Download_PTV_Hospitals` notebook to obtain all of related datasets.

After downloading the data, remain in the `notebooks` directory and run the notebook:
1. `Distance_Calculation_Train_Hosp_CBD.ipynb`: This notebook processes the datasets mentioned about and calculates the driviing distances of each property from the nearest train station and Melbourne CBD using the Open Route Services API. It also calculates the haversine distance of each property from its nearest hospital. We obtain the domain dataset with distances added and it is saved to `data/curated/final_train_hospital_cbd_dist_data`.

To answer the first question, **What are the Most Important Internal and External Factors?**, the following notebooks have been created and should be run in the specified order:
1. `combining_datasets.ipynb`: In this notebook we combine all our internal and external features to obtain the final dataset to test for feature importance.
2. `Random_Forest_Regressor_Feature_Imp.ipynb`: In this notebook we implement a Random Forest Regression Model to find the feature importance metrics for each feature in order to determine the top 10.
3. `XGBoost_Feature_Imp.ipynb`: In this notebook we implement an XGBoost model to find the feature importance metrics for each feature in order to determine the top 10.
4. `Top_10_Features.ipynb`: In this notebook we find the averages of the importances for each feature and select the top 10 based on highest average importance across both the models.

To answer the second question **"Where are the most liveable and affordable suburbs in Victoria?"**, the following notebooks have been created and should be run in the specified order:
1. `livability.ipynb`: In this notebook, we identify the most liveable suburbs in Victoria based on our livability metrics. The livable metric's index of the suburbs is stored in the `data/curated` directory.
2. `affordability.ipynb`: This notebook identifies the most affordable suburbs in Victoria based on our affordability metrics. The affordability metric's index of the suburbs is stored in the `data/curated` directory.
3. `metropolitan_victoria`: This notebooks finds the postcode for each sa2 area in Victoria and select the suburbs that are metropolitan, which are used in `livability_affordability.ipynb` notebook for further area selection. The chosen sa2 areas are stored in the `data/curated` directory.
4. `livability_affordability.ipynb`: This notebook combines both livability and affordability metrics with different weights assigned to each metric. A new index is generated to determine the most liveable and affordable suburbs in Victoria. The distribution of the livability, affordability, and combined index is also illustrated using geospatial visualizations.

To answer the third question **"What are the top 10 suburbs with the highest predicted growth rate?"**, the following notebooks and scripts have been created and should be run in the specified order:
1. `historical.py`: This script downloads the historical data from the DFFH website and stores it in the `data/landing/historical` directory.
2. `preprocess_historical.ipynb`: This notebook preprocesses the historical data and stores it in `data/raw/historical_data.csv`.
3. `eda_historical.ipynb`: This notebook provides an exploratory data analysis of the historical data, including visualizations of the distribution of rental prices over time, slope calculation, and correlation analysis.
4. `time_series_rental_price.ipynb`: This notebook performs time series analysis on the historical data on a particular suburb to predict the future rental prices using ARIMA and SARIMA models, mainly to infer the appropriate parameters for the models for all suburbs.
5. `time_series_rental_price_2.ipynb`: This notebook predicts the future rental prices for all suburbs in Victoria using ARIMA and SARIMA models. The predicted rental prices are stored in `data/curated/forecast_data.csv`.
6. `time_series_rental_price_3.ipynb`: This notebook analyzes the predicted rental prices for all suburbs in Victoria and calculates the growth rate for each suburb. The top 10 suburbs with the highest predicted growth rate are identified and their behavior is visualized.
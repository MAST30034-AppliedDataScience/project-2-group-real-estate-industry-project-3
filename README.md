# Generic Real Estate Consulting Project

See the `scrape.py` file in the `scripts` directory to get started scraping data. 

**Research Goal:** 

**Timeline:** 

## Setup

Python 3 dependencies:

* Pyspark
* Pandas, Numpy
* Seaborn, matplotlib.pyplot
* Scikit Learning

We provide a requirement.txt including all of the libraries used. Set up the environment by running:
```
pip install -r requirements.txt
```

## Pipeline
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

To answer the question **"Where are the most liveable and affordable suburbs in Victoria?"**, the following notebooks have been created and should be run in the specified order:
1. `livability.ipynb`: In this notebook, we identify the most liveable suburbs in Victoria based on our livability metrics. The livable metric's index of the suburbs is stored in the `data/curated` directory.
2. `affordability.ipynb`:
3. `metropolitan_victoria`: This notebooks finds the postcode for each sa2 area in Victoria and select the suburbs that are metropolitan, which are used in `livability_affordability.ipynb` notebook for further area selection. The chosen sa2 areas are stored in the `data/curated` directory.
4. `livability_affordability.ipynb`: This notebook combines both livability and affordability metrics with different weights assigned to each metric. A new index is generated to determine the most liveable and affordable suburbs in Victoria. The distribution of the livability, affordability, and combined index is also illustrated using geospatial visualizations.
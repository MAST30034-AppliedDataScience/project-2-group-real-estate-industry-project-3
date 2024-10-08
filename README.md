# Generic Real Estate Consulting Project
Groups should generate their own suitable `README.md`.

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
In terms of the `parks and reservation` external dataset, please navigate to the `notebooks` directory and run the `data_download_parkres_&_property_lost.ipynb` notebook to get all of the datasets related to it.

After downloading the data, stay in the `notebooks` directory and run the notebooks in the specified order:
1. `sa2_district_boundaries.ipynb`: This notebook shows the SA2 boundaries of each district in Victoria, shows some visualizations of those areas, and stores all shape data in the `data/landing/boundaries/Victoria` directory.
2. `parkres_sa2_matching.ipynb`: This notebook finds the corresponding sa2_name and postcode for each park and reservation as required, implements geospatial analysis, and stores the csv data in the `data/curated/parkres` directory.
3. `parkres_domain_merge.ipynb`: This notebook merges two datasets: the parks and reservations dataset and the domain rental dataset, then stores the merged dataset in the `data/curated/parkres` directory.
4. `parkres_domain_analysis.ipynb`: This notebook performs some statistical analysis on the merged dataset to see the significance of the parks/reservations on the rental price.
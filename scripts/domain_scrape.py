# Written by Daksh Agrawal

import json
import re
from urllib.error import URLError, HTTPError
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen, Request
from tqdm import tqdm
from bs4 import BeautifulSoup
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

DOMAIN_BASE_URL = 'https://www.domain.com.au'
DOMAIN_PAGE_LIMIT = 51
MELBOURNE_POSTCODES = list(range(3000, 3200)) + [3800, 3801]
DATA_DIR = "../scrape_data"
LOG_FILE = "../scrape_data/scraped_postcodes.txt"
LOG_LOCK = threading.Lock()

MAX_THREADS = 5  # Adjust the number of threads based on your rate limit


def get_properties_for_postcode(postcode):
    urls = []

    for page_i in range(1, DOMAIN_PAGE_LIMIT):
        relative_url = DOMAIN_BASE_URL + f'/rent/?sort=dateupdated-desc&postcode={postcode}&page={page_i}'

        try:
            # Attempt to fetch the page
            req = Request(relative_url, headers={'User-Agent': "PostmanRuntime/7.6.0"})
            html = urlopen(req).read()
            soup = BeautifulSoup(html, "lxml")
        except (URLError, HTTPError) as e:
            # If the request fails for any page, skip to the next one
            continue

        try:
            # Find all links with the 'address' class and matching href pattern
            index_links = soup.findAll(
                "a",
                {"class": "address"},
                href=re.compile(f"{DOMAIN_BASE_URL}/.*")
            )
            # Add the found URLs to the list
            urls.extend([link['href'] for link in index_links])
        except AttributeError:
            # If no links are found, move to the next page
            continue

    return urls


def scrape_property(property_url):
    data = {}

    try:
        # Attempt to fetch the webpage
        req = Request(property_url, headers={'User-Agent': "PostmanRuntime/7.6.0"})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, "lxml")
    except Exception as e:
        print(f"Failed to scrape {property_url}: {e}")
        # If the request fails, return an empty dictionary
        return {}

    data["url"] = property_url

    # Use try-except to avoid breaking when elements are missing
    try:
        data["price"] = soup.find("div", {"data-testid": "listing-details__summary-title"}).text
    except AttributeError:
        data["price"] = None

    try:
        data["address"] = soup.find("h1").text
    except AttributeError:
        data["address"] = None

    try:
        data["property_type"] = soup.find("div", {"data-testid": "listing-summary-property-type"}).text
    except AttributeError:
        data["property_type"] = None

    # Scrape features, handle missing wrapper or features
    data["features"] = []
    try:
        features_wrapper = soup.find("div", {'data-testid': "property-features-wrapper"})
        if features_wrapper:
            for feature in features_wrapper.findAll("span", {"data-testid": "property-features-feature"}):
                data["features"].append(feature.text)
    except AttributeError:
        pass

    # Scrape summary
    data["summary"] = []
    try:
        summary_strip = soup.find("ul", {"data-testid": "listing-summary-strip"})
        if summary_strip:
            for s in summary_strip.findAll("li"):
                data["summary"].append(s.text)
    except AttributeError:
        pass

    # Scrape latitude and longitude from Google Maps link
    try:
        google_maps = soup.find("a", href=re.compile(r"https://www.google.com/maps/dir/*"))['href']
        coords = parse_qs(urlparse(google_maps).query)["destination"][0].split(",")
        data["latitude"] = float(coords[0])
        data["longitude"] = float(coords[1])
    except (AttributeError, KeyError, ValueError):
        data["latitude"] = None
        data["longitude"] = None

    return data


def read_scraped_postcodes():
    """Reads the list of already scraped postcodes from a log file."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log_file:
            return set(line.strip() for line in log_file)
    return set()


def log_scraped_postcode(postcode):
    """Logs a completed postcode to the log file, thread-safe."""
    with LOG_LOCK:
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"{postcode}\n")


def scrape_and_save_postcode_data(postcode):
    filename = os.path.join(DATA_DIR, f'properties_{postcode}.json')

    # Skip if the file already exists
    if os.path.exists(filename):
        print(f"Skipping {postcode}, data already exists.")
        return

    property_urls = get_properties_for_postcode(postcode)
    property_data = []

    # Scrape each property URL and collect data
    for url in tqdm(property_urls, desc=f"Scraping postcode {postcode}"):
        property_data.append(scrape_property(url))

    # Save the data for the postcode
    with open(filename, 'w') as jsonfile:
        json.dump(property_data, jsonfile)
    print(f"Data for postcode {postcode} saved to {filename}")

    # Log the postcode as scraped
    log_scraped_postcode(postcode)


def scrape_all_postcodes_parallel():
    scraped_postcodes = read_scraped_postcodes()

    postcodes_to_scrape = [postcode for postcode in MELBOURNE_POSTCODES if str(postcode) not in scraped_postcodes]

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Submit tasks to the executor for each postcode
        futures = {executor.submit(scrape_and_save_postcode_data, postcode): postcode for postcode in
                   postcodes_to_scrape}

        for future in as_completed(futures):
            postcode = futures[future]
            try:
                future.result()  # Raises any exceptions if they occurred
            except Exception as e:
                print(f"Error scraping postcode {postcode}: {e}")


# Start parallel scraping, ensuring no postcode is scraped more than once
scrape_all_postcodes_parallel()

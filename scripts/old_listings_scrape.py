# NO LONGER USED

BASE_URL = 'https://www.oldlistings.com.au'
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urlencode
import re
from tqdm import tqdm
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://google.com.au',
}


def scrape_sitemap():
    s_urls = []
    sitemap_url = BASE_URL + '/site-map'
    params = urlencode({
        'state': 'VIC',
    })
    home_page_vic = BeautifulSoup(urlopen(Request(f"{sitemap_url}?{params}", headers=headers)), "lxml")
    last_page_url = home_page_vic.find("a", {"title": "Go to last page"})['href']
    last_page = int(re.search(r'(?<=page=)\d+', last_page_url).group())
    print(f"Last page: {last_page}")

    for page in range(0, last_page):
        print(f"Scraping page {page}")
        page_url = f"{sitemap_url}?{params}&page={page}"
        page_vic = BeautifulSoup(urlopen(Request(page_url, headers=headers)), "lxml")
        for link in tqdm(page_vic.find_all("a", href=re.compile(r'^/real-estate/VIC/[^/]+/\d+/rent/$'))):
            num_pages = scrape_suburb(link['href'])
            if num_pages:
                s_urls.append((link['href'], num_pages))
    return s_urls


def scrape_suburb(url):
    home_page_url = BASE_URL + url
    try:
        suburb_home_page = BeautifulSoup(urlopen(Request(home_page_url, headers=headers)), "lxml")
        pagination = suburb_home_page.find("ul", {"class": "pagination"})
        if pagination:
            last_page = int(pagination.find_all("li")[-2].text)
        else:
            last_page = 1
        return last_page
    except Exception as e:
        return None

# Ask user for scraping or loading data`
if input("Scrape Sitemap? (y/n): ").lower() == 'y':
    suburb_urls = scrape_sitemap()
    # save data as csv
    with open("../scrape_data/suburbs.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Writing the rows
        csvwriter.writerows(suburb_urls)

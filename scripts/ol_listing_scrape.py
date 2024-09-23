from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from tqdm import tqdm
from json import dump

urls = [
    ("https://www.oldlistings.com.au/real-estate/VIC/Carlton+South/3000/rent/", 3)
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://google.com.au',
}


def get_specific_prop(element, c):
    try:
        return element.find("p", {"class": c}).text
    except:
        return None


def scrape_suburb(url):
    url, last_page = url
    print(f"Scraping {url}")
    property_metadata = []

    for page in tqdm(range(1, last_page + 1)):
        page_url = f"{url}{page}"
        page_vic = BeautifulSoup(urlopen(Request(page_url, headers=headers)), "lxml")
        for prop in page_vic.find_all("div", {"class": "property"}):
            try:
                prop_details = {
                    "address": prop.find("h2").text,
                    "lat": prop['data-lat'],
                    "lng": prop['data-lng'],
                    "bed": get_specific_prop(prop, "bed"),
                    "bath": get_specific_prop(prop, "bath"),
                    "car": get_specific_prop(prop, "car"),
                    "type": get_specific_prop(prop, "type"),
                }
                property_metadata.append(list(prop_details.values()))
            except Exception as e:
                print(f"Error: {e}")
    return property_metadata


print("Scraping Suburbs")
property_metadata = []
for url in urls:
    property_metadata += scrape_suburb(url)
print("Saving Data")
# save data as json
with open('../scrape_data/example.json', 'w') as f:
    dump(property_metadata, f)

import requests
from bs4 import BeautifulSoup
import time

base = "https://www.shl.com"
url = "https://www.shl.com/products/product-catalog/"

# r = requests.get(url)
# # print(r.text)
# with open("file.html","w", encoding="utf-8") as f:
#     f.write(r.text)

all_links = set()
i = 0

while True:
    print(f"Scraping start={i}")
    params= {
        "start" : i,
        "type" : 1  #type = 1 means individual test solutions and no pre-packcaged job solutions

    }

    r = requests.get(url, params=params)
    if r.status_code != 200:
        print("Request failed.")
        break

    soup = BeautifulSoup(r.text, "html.parser")

    page_links = 0

    for a in soup.find_all("a", href = True):
        href = a["href"]

        if href.startswith("/products/product-catalog/view/"):
            full_url = base + href
            if full_url not in all_links:
                all_links.add(full_url)
                page_links += 1

    print(f"Found {page_links} links on this page.")

    if page_links == 0:
        print("No more assessments found.")
        break

    i += 12
    time.sleep(1)  

print("Total Test Solutions:", len(all_links))

with open("links.txt", "w", encoding="utf-8") as f:
    for link in sorted(all_links):
        f.write(link+ "\n")
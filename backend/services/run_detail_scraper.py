# getting all the individual test details from detail_scraper and storing them into assessments.json, in json format.
# assessments.json
from detail_scraper import scrape_detail
import time
import json
import os

os.makedirs("data", exist_ok=True)

results = []  # empty list to store all assessments details.

with open("links.txt") as f:
    links = [line.strip() for line in f.readlines()]

for i, url in enumerate(links):
    print(f"[{i+1}/{len(links)}] Scraping {url}")
    try:
        data = scrape_detail(url)
        results.append(data)
    except Exception as e:
        print("Error:", e)

    time.sleep(1)

with open("data/assessments.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

import requests
from bs4 import BeautifulSoup

Headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_detail(url):
    r = requests.get(url, headers=Headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    data = {
        "name": None,
        "url": url,
        "description": None,
        "job_levels": None,
        "languages": None,
        "assessment_length": None,
        "test_type" : None
    }

    h1 = soup.find("h1")
    if h1:
        data["name"] = h1.get_text(strip=True)

    sections = soup.find_all("div", class_="product-catalogue-training-calendar__row") # accessing other details through 'product-catalogue-training-calendar__row' class div

    for sec in sections:
        title = sec.find("h4") #this represents the key, i.e h4 is the heading
        value = sec.find("p") # and this is the value, means p is the content of the heading.

        if not title or not value:
            continue

        key = title.get_text(strip=True).lower()
        val = value.get_text(strip=True)

        if "description" in key:
            data["description"] = val
        elif "job level" in key:
            data["job_levels"] = val
        elif "language" in key:
            data["languages"] = val
        elif "assessment length" in key:
            data["assessment_length"] = val

            test_type_span = sec.find("span", class_="product-catalogue__key")
            if test_type_span:
                data["test_type"] = test_type_span.get_text(strip=True)
    return data


        



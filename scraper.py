
#-------------------------------------------------------------------------
# AUTHOR: Craig Chan
# FILENAME: scraper.py
# SPECIFICATION: Crawl the link sections of this seed URL
# using breadth-first search, printing page headings and discovered URLs.
# FOR: CS 4250 - Assignment #2
# TIME SPENT: About 1 hour 30 minutes
#-------------------------------------------------------------------------

# Importing Python libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
import re

# Defining the seed URL
seed = "https://testingurl.dev/scraping/links/circular"

# Creating the frontier and seen collections
frontier = deque([seed])
seen = {seed}

# Sort discovered links by their numeric page ID
def page_id(url):
    numbers = re.findall(r"\d+", url)
    return int(numbers[-1]) if numbers else -1

# Crawling until the frontier is empty
while frontier:

    # Removing the first URL from the frontier
    url = frontier.popleft()

    # Retrieving and parsing the Web page
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Printing the text contained in the <h1> element
    h1 = soup.find("h1")
    if h1:
        print(h1.get_text(strip=True))

    # Extracting and processing hyperlinks
    links = []

    for a in soup.find_all("a", href=True):
        link = urljoin(url, a["href"])

        # Only follow links within the Circular Links section
        if link.startswith(seed):
            links.append(link)

    # Sorting links by page ID
    links.sort(key=lambda link: (page_id(link), link))

    # Adding URLs that have not already been seen
    for link in links:
        if link not in seen:
            seen.add(link)
            frontier.append(link)

# Printing all URLs
print("\nAll URLs in seen:")
for url in sorted(seen, key=lambda link: (page_id(link), link)):
    print(url)

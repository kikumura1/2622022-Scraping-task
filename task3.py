import time
import csv
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

START_URL = "https://musashino-u.ac.jp" 
DOMAIN = urlparse(START_URL).netloc

web_sitemap = {}
visited_urls = set()

def crawl_page(url):
    if url in visited_urls or urlparse(url).netloc != DOMAIN:
        return
    
    print(f"アクセス中: {url}")
    visited_urls.add(url)
    time.sleep(1.0)
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200 or "text/html" not in response.headers.get("Content-Type", ""):
            return
            
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip() if soup.title else "No Title"
        web_sitemap[url] = title
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            full_url = urlparse(full_url)._replace(fragment="").geturl()
            crawl_page(full_url)
            
    except Exception as e:
        pass

def main():
    crawl_page(START_URL)
    csv_filename = "musashino_sitemap.csv"
    with open(csv_filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Title"])
        for url, title in web_sitemap.items():
            writer.writerow([url, title])

if __name__ == "__main__":
    main()

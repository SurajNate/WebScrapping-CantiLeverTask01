import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def clean_price(raw_price):
    
    # Remove non-breaking space or garbage like Â, ₹, etc.
    cleaned = raw_price.replace("Â", "").replace("₹", "").strip()
    
    # Ensure it starts with £
    if not cleaned.startswith('£'):
        cleaned = '£' + cleaned.strip('£₹')

    return cleaned

def scrape_books(base_url, num_pages=1):
    all_books = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}/catalogue/page-{page}.html"
        print(f"Scraping {url}...")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        for book in books:
            title = book.h3.a['title']
            raw_price = book.find('p', class_='price_color').text.strip()
            price = clean_price(raw_price)

            rating_class = book.p['class'][1]  # e.g., 'Three', 'Four'

            all_books.append({
                'Title': title,
                'Price': price,
                'Rating': rating_class
            })

    df = pd.DataFrame(all_books)
    df.to_csv('products.csv', index=False, encoding='utf-8-sig')
    print(f"✅ Scraping completed and saved {len(df)} records to products.csv")

# Run the scraper
if __name__ == "__main__":
    scrape_books("https://books.toscrape.com", num_pages=3)

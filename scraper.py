import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

BASE_URL = "https://books.toscrape.com/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def scrape_one_page(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for article in soup.find_all("article", class_="product_pod"):
        title = article.find("h3").find("a")["title"]
        price_text = article.find("p", class_="price_color").text.strip()
        price = float(price_text.replace("Â£", "").replace("£", "").replace("€", ""))
        rating_class = article.find("p", class_="star-rating")["class"][1]
        rating = RATING_MAP.get(rating_class, 0)
        availability = article.find("p", class_="availability").text.strip()
        books.append({
            "title": title,
            "price_gbp": price,
            "rating": rating,
            "availability": availability
        })
    return books, soup

def get_next_url(soup):
    next_li = soup.find("li", class_="next")
    if not next_li:
        return None
    next_href = next_li.find("a")["href"]
    if "catalogue/" not in next_href:
        next_href = "catalogue/" + next_href
    return BASE_URL + next_href

def scrape_books(max_pages=5):
    all_books = []
    current_url = START_URL
    print(f"Mulai scraping {max_pages} halaman...")

    for page_num in tqdm(range(1, max_pages + 1), desc="Halaman"):
        try:
            books, soup = scrape_one_page(current_url)
            all_books.extend(books)
            next_url = get_next_url(soup)
            if not next_url:
                break
            current_url = next_url
            time.sleep(0.5)
        except Exception as e:
            print(f"\nError di halaman {page_num}: {e}")
            break

    return pd.DataFrame(all_books)

if __name__ == "__main__":
    df = scrape_books(max_pages=5)
    print(f"\n✅ Total buku: {len(df)}")
    print(f"   Harga rata-rata: £{df['price_gbp'].mean():.2f}")
    print(f"   Rating rata-rata: {df['rating'].mean():.1f}/5")
    df.to_csv("books_raw.csv", index=False)
    print("💾 Disimpan ke books_raw.csv")
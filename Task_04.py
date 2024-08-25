import requests
from bs4 import BeautifulSoup
import csv

def extract_product_info(soup):
    products = []

    # Adjust these selectors based on the actual HTML structure
    for product in soup.find_all('div', {'data-component-type': 's-search-result'}):
        name = product.find('span', class_='a-size-medium a-color-base a-text-normal')
        price = product.find('span', class_='a-price-whole')
        rating = product.find('span', class_='a-icon-alt')

        if name and price and rating:
            products.append([
                name.get_text(strip=True),
                price.get_text(strip=True),
                rating.get_text(strip=True)
            ])

    return products

def save_to_csv(products, filename='products.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Price', 'Rating'])  # CSV header
        writer.writerows(products)

def scrape_ecommerce(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = extract_product_info(soup)
    return products

if __name__ == "__main__":
    url = "https://www.amazon.in/s?k=soup&crid=S35MP5OGEJGX&sprefix=soup%2Caps%2C317&ref=nb_sb_noss_1"
    products = scrape_ecommerce(url)
    if products:
        save_to_csv(products)
        print(f"Data saved to products.csv")
    else:
        print("No products found.")

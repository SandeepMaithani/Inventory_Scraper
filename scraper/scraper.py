import os
import requests
import time
from bs4 import BeautifulSoup
from typing import Optional
from .models import Product
from .decorators import retry


class Scraper(object):
    def __init__(self, base_url: str, image_dir: str, proxy: Optional[str] = None):
        self.base_url = base_url
        self.proxy = proxy
        self.image_dir = image_dir
        os.makedirs(name=image_dir, exist_ok=True)


    def save_image(self, url: str):
        response = requests.get(url=url)
        image_tag = int(time.time()* 1000)
        image_path = os.path.join(self.image_dir, f"{image_tag}.jpg")
        
        with open(image_path, 'wb') as file_instance:
            file_instance.write(response.content)
        
        return image_path

    @retry(retries=3, delay=5)
    def scrape_page(self, page_number: int):
        # url example with pagination:- https://dentalstall.com/shop/page/3/
        # website having issue with pagination args for page 1
        # so handling case here
        if page_number in [0, 1]:
            url = f"{self.base_url}/"
        else:
            url = f"{self.base_url}/page/{page_number}"
        proxies = {
            "http": self.proxy,
            "https": self.proxy
        } if self.proxy else None

        response = requests.get(url=url, proxies=proxies)
        response.raise_for_status()

        
        soup = BeautifulSoup(response.content, 'html.parser')
        product_cards = soup.find_all('li', class_='product')

        products = []

        for product in product_cards:
            try:
                # Find the div with class "mf-product-thumbnail"
                product_thumbnail_div = product.find('div', class_='mf-product-thumbnail')
                
                # Extract the title attribute from the img tag
                img_tag = product_thumbnail_div.find('img')
                title = img_tag.get('title')

                # Extract the .jpg URL from the data-lazy-srcset attribute
                image_url = img_tag.get('data-lazy-src')

                # Extract the product price (current price inside <ins> tag)
                price_tag = product.find('span', class_='woocommerce-Price-amount')
                price = price_tag.get_text(strip=True) if price_tag else 'No price'
                path_to_image = self.save_image(url=image_url)

                product_instance = Product(
                    product_title=title,
                    product_price=float(price[1:]),
                    path_to_image=path_to_image
                )
            except Exception as e:
                print(f"Failed to scrape product due to exception: {e}")
                continue

            products.append(product_instance)

        return products
    

    def scrape(self, max_pages: int):
        all_products = []

        for page in range(1, max_pages + 1):
            products = self.scrape_page(page_number=page)
            all_products.extend(products)
        
        return all_products

import json
import sqlite3
from typing import List

from scraper.cache import CacheStrategy
from .models import Product


class StorageStrategy(object):
    def save(self, data: List[Product]):
        raise NotImplementedError
    
    def load(self):
        raise NotImplementedError


class JSONStorage(StorageStrategy):
    def __init__(self, file_path: str, cache_strategy: CacheStrategy):
        self.file_path = file_path
        self.cache_strategy = cache_strategy

    def save(self, data: List[Product]):
        existing_data = self.load()
        updated_data = []

        for product in data:
            cached_price = self.cache_strategy.get(product.product_title)

            if cached_price is None or float(cached_price) != product.product_price:
                self.cache_strategy.set(product.product_title, product.product_price)
                updated_data.append(
                    {
                        "product_title": product.product_title,
                        "product_price": product.product_price,
                        "path_to_image": product.path_to_image
                    }
                )
        
        # Merge updated data with exisitng data
        product_titles = {product['product_title'] for product in updated_data}

        for product in existing_data:
            if product['product_title'] not in product_titles:
                updated_data.append(product)

        with open(self.file_path, 'w') as file_instance:
            json.dump(
                updated_data,
                file_instance,
                indent=4
            )
    

    def load(self):
        try:
            with open(self.file_path, 'r') as file_instance:
                data = json.load(file_instance)
                return [Product(**item) for item in data]
        except FileNotFoundError:
            return []


class SQLiteStorage(StorageStrategy):
    def __init__(self, db_path: str, cache_strategy: CacheStrategy):
        self.db_path = db_path
        self.cache_strategy = cache_strategy
        self._create_table()

    
    def _create_table(self):
        with sqlite3.connect(self.db_path) as connection_instance:
            db_cursor = connection_instance.cursor()
            db_cursor.execute(
                """CREATE TABLE IF NOT EXISTS products (
                product_title TEXT PRIMARY KEY,
                product_price REAL,
                path_to_image TEXT)"""
            )

            connection_instance.commit()
    
    def save(self, data: List[Product]):
        with sqlite3.connect(self.db_path) as connection_instance:
            db_cursor = connection_instance.cursor()

            for product in data:
                cached_price = self.cache_strategy.get(product.product_title)

                if cached_price is None or float(cached_price) != product.product_price:
                    self.cache_strategy.set(product.product_title, product.product_price)
                    db_cursor.execute(
                        """INSERT OR REPLACE INTO products (
                        product_title, product_price, path_to_image) 
                        VALUES (?, ?, ?)""",
                        (product.product_title,
                        product.product_price,
                        product.path_to_image)
                    )
            
            connection_instance.commit()
    
    def load(self):
        with sqlite3.connect(self.db_path) as connection_instance:
            db_cursor = connection_instance.cursor()
            db_cursor.execute(
                """SELECT product_title, product_price, path_to_image FROM products"""
            )
            rows = db_cursor.fetchall()

            return [Product(product_title=row[0], product_price=row[1], path_to_image=row[2]) for row in rows]

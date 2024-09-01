from pydantic import BaseModel, HttpUrl
from typing import List


class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str


class ScrapeResult(BaseModel):
    products: List[Product]
    total_scraped: int
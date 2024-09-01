import os

from fastapi import FastAPI, Query, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from scraper.factory import Factory
from scraper.models import ScrapeResult


app = FastAPI()
security = HTTPBearer()


# env variable for the token
API_TOKEN = os.getenv("API_TOKEN", "test_user_token")


def get_current_user(credentails: HTTPAuthorizationCredentials = Depends(security)):
    if credentails.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
    
    return credentails.credentials


@app.get("/scrape", response_model=ScrapeResult)
def scrape(max_pages: int = Query(5, alias="maxPages"),
           proxy: str = Query(None), token: str = Depends(get_current_user)):
    base_url = "https://dentalstall.com/shop"
    scraper = Factory.create_scraper(base_url=base_url, img_storage_path="scraper/data/images/", proxy=proxy)
    products = scraper.scrape(max_pages=max_pages)

    # choose the cache strategy
    cache_strategy = Factory.create_in_memory_cache()
    #cache_strategy = Factory.create_redis_cache()

    # choose the storage strategy
    storage = Factory.create_json_storage(file_path="scraper/data/products.json", cache_strategy=cache_strategy)
    storage.save(data=products)

    # choose the notification strategy
    notifier = Factory.create_console_notifier()
    notifier.notify(f"Scraped {len(products)} products and saved to database.")

    return ScrapeResult(products=products, total_scraped=len(products))

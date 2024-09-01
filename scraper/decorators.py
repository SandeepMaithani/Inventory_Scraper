import time
import requests


def retry(retries: int=5, delay: int=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    print(f"Error: {e}. Retrying in {delay} seconds....")
                    time.sleep(delay)
            return []
        return wrapper
    return decorator
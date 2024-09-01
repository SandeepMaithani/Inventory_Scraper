from .cache import CacheStrategy, RedisCache, InMemoryCache
from .notifier import ConsoleNotifier, FileNotifier
from .scraper import Scraper
from .storage import JSONStorage, SQLiteStorage


class Factory(object):
    @staticmethod
    def create_scraper(base_url: str, img_storage_path: str, proxy: str =  None):
        return Scraper(base_url, img_storage_path, proxy)
    
    # cache
    @staticmethod
    def create_redis_cache(redis_host: str = 'localhost', redis_port: int = 6379):
        return RedisCache(host=redis_host, port=redis_port)
    
    @staticmethod
    def create_in_memory_cache():
        return InMemoryCache()
    
    # Storage
    @staticmethod
    def create_json_storage(file_path: str, cache_strategy: CacheStrategy):
        return JSONStorage(file_path, cache_strategy)
    
    @staticmethod
    def create_sqlite_storage(db_path: str, cache_strategy: CacheStrategy):
        return SQLiteStorage(db_path, cache_strategy)
    
    # Notification
    @staticmethod
    def create_console_notifier():
        return ConsoleNotifier()
    
    @staticmethod
    def create_file_notifier(file_path: str):
        return FileNotifier(file_path)
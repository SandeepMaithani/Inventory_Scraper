from abc import ABC, abstractmethod
import redis


class CacheStrategy(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass


class RedisCache(CacheStrategy):

    _redis_instance = None


    def __new__(cls, *args, **kwargs):
        if not cls._redis_instance:
            cls._redis_instance = super(RedisCache, cls).__new__(cls, *args, **kwargs)
            cls._redis_instance.client = redis.Redis(host='localhost', port=6379, db=0)
        
        return cls._redis_instance

    def get(self, key):
        return self.client.get(key)
    
    def set(self, key, value):
        self.client.set(key, value)


class InMemoryCache(CacheStrategy):
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value

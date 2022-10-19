import redis, os

class RedisHelper: 

    def __init__(self):
        self._redis_host = os.environ.get("REDIS_HOST", "localhost")
        self._redis_port = 6379
        self._redis_instance = redis.Redis(host=self._redis_host, port=self._redis_port, password="")

    def set_key(self, key, value): 
        return self._redis_instance.set(key, value)
        
    def delete_key(self, key):
        self._redis_instance.delete(key)

    def get_key(self, key):
        return self._redis_instance.get(key)


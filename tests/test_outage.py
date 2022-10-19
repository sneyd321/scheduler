from models.redis import RedisHelper
from models.monad import RedisMaybeMonad

async def test_Scheduler_returns_error_when_unable_to_connect_to_redis():
    redis = RedisHelper()
    redis._redis_host = "localhost"
    monad = RedisMaybeMonad("TEST", b"test") \
        .bind(redis.set_key)
    assert monad.error_status == {"status": 502, "reason": "Failed to connect to Redis"}
    

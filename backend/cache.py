import redis

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

def get_cached_tasks(user):
    return redis_client.get(f"tasks_{user}")

def set_cached_tasks(user, tasks):
    redis_client.set(f"tasks_{user}", tasks)

def invalidate_cache(user):
    redis_client.delete(f"tasks_{user}")

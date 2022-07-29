from typing import Any

from redis import Redis, exceptions
from she_logging import logger

import dhosredis
from dhosredis.stub_redis import RedisStub


class DhosRedis:

    _redis = None

    @classmethod
    def _init_redis(cls) -> None:
        if dhosredis.config["REDIS_INSTALLED"]:
            cls._redis = Redis(
                host=dhosredis.config["REDIS_HOST"],
                port=dhosredis.config["REDIS_PORT"],
                password=dhosredis.config["REDIS_PASSWORD"],
                db=0,
                socket_timeout=dhosredis.config["REDIS_TIMEOUT"],
                decode_responses=True,
                ssl=dhosredis.config["REDIS_USE_SSL"],
            )
            logger.info("Created instance of Redis client")
        else:
            cls._redis = RedisStub()
            logger.info("Redis disabled")

    @classmethod
    def get_value(cls, key: str) -> Any:
        logger.debug("Getting value with key '%s' from redis", key)
        if cls._redis is None:
            cls._init_redis()
            if cls._redis is None:
                raise EnvironmentError("Failed to initialise redis")
        try:
            return cls._redis.get(key)
        except exceptions.AuthenticationError:
            logger.exception("Authentication error connecting to redis")
            return None
        except (exceptions.ConnectionError, exceptions.TimeoutError):
            logger.warning("Couldn't connect to redis")
            return None

    @classmethod
    def set_value(cls, key: str, value: Any) -> bool:
        logger.debug("Setting value with key '%s' in redis", key)
        if cls._redis is None:
            cls._init_redis()
            if cls._redis is None:
                raise EnvironmentError("Failed to initialise redis")
        try:
            cls._redis.set(key, value)
        except exceptions.AuthenticationError:
            logger.exception("Authentication error connecting to redis")
            return False
        except (exceptions.ConnectionError, exceptions.TimeoutError):
            logger.exception("Couldn't connect to redis")
            return False
        return True

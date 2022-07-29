from typing import Any, TypedDict

from environs import Env
from she_logging import logger

from dhosredis.redis import DhosRedis


class RedisConfig(TypedDict):
    REDIS_INSTALLED: bool
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    REDIS_TIMEOUT: int
    REDIS_USE_SSL: bool


_env = Env()

config: RedisConfig = {
    "REDIS_INSTALLED": _env.bool("REDIS_INSTALLED", True),
    "REDIS_HOST": _env.str("REDIS_HOST", ""),
    "REDIS_PORT": _env.str("REDIS_PORT", ""),
    "REDIS_PASSWORD": _env.str("REDIS_PASSWORD", ""),
    "REDIS_TIMEOUT": _env.int("REDIS_TIMEOUT", 2),  # Default to 2 seconds.
    "REDIS_USE_SSL": _env.bool("REDIS_USE_SSL", False),
}


def get_value(key: str, default: Any = None) -> Any:
    """
    Retrieves a value from DHOS's instance of redis, or a default if the value could not be retrieved.
    :param key: The key for which to retrieve a value
    :param default: The default value to return if the key could not be retrieved
    :return: The value from redis
    """
    value: Any = DhosRedis.get_value(key=key)
    if value is None:
        logger.warning("No value in redis, falling back to default")
        logger.debug("Default value: '%s'", default)
        value = default
    return value


def set_value(key: str, value: str) -> None:
    """
    Sets a value in DHOS's instance of redis.
    :param key: The key for which to set a value
    :param value: The value to set
    """
    success: bool = DhosRedis.set_value(key=key, value=value)
    if not success:
        logger.warning("Failed to set key %s in redis", key, extra={"value": value})

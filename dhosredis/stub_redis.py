"""
Stub class that implements the redis interface.
Used in non-production environments when redis is not installed.
"""
from typing import Any


class RedisStub:
    def get(self, key: str) -> Any:
        return None

    def set(self, key: str, value: str) -> None:
        pass

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockFixture

import dhosredis
from dhosredis import DhosRedis, RedisConfig, redis


class TestRedis:
    @pytest.fixture
    def reset_redis(self, monkeypatch: MonkeyPatch) -> None:
        """Forces the DhosRedis class to create a new connection to redis for this test"""
        monkeypatch.setattr(DhosRedis, "_redis", None)

    def test_get_value_success(self, mocker: MockFixture) -> None:
        DhosRedis._redis = None
        mock_redis = mocker.patch.object(redis, "Redis").return_value
        mock_redis.get.return_value = "VALUE"
        result = DhosRedis.get_value("KEY")
        assert result == "VALUE"

    @pytest.mark.parametrize(
        "error",
        {
            redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError,
            redis.exceptions.AuthenticationError,
        },
    )
    def test_get_value_failure(
        self, mocker: MockFixture, error: Exception, reset_redis: None
    ) -> None:
        mock_redis = mocker.patch.object(redis, "Redis").return_value
        mock_redis.get.side_effect = error
        result = DhosRedis.get_value("KEY")
        assert result is None

    def test_set_value_success(self, mocker: MockFixture, reset_redis: None) -> None:
        mock_redis = mocker.patch.object(redis, "Redis").return_value
        DhosRedis.set_value("KEY", "VALUE")
        assert mock_redis.set.call_count == 1
        assert mock_redis.set.call_args == (("KEY", "VALUE"), {})

    @pytest.mark.parametrize(
        "error",
        {
            redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError,
            redis.exceptions.AuthenticationError,
        },
    )
    def test_set_value_failure(
        self, mocker: MockFixture, reset_redis: None, error: Exception
    ) -> None:
        mock_redis = mocker.patch.object(redis, "Redis").return_value
        mock_redis.set.side_effect = error
        DhosRedis.set_value("KEY", "VALUE")
        assert mock_redis.set.call_count == 1
        assert mock_redis.set.call_args == (("KEY", "VALUE"), {})

    def test_redis_installed(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(
            dhosredis,
            "config",
            RedisConfig(
                REDIS_INSTALLED=True,
                REDIS_HOST="http://redis",
                REDIS_PORT="6379",
                REDIS_PASSWORD="secret",
                REDIS_TIMEOUT=2,
                REDIS_USE_SSL=False,
            ),
        )

    def test_redis_not_installed(
        self, monkeypatch: MonkeyPatch, reset_redis: None
    ) -> None:
        monkeypatch.setattr(
            dhosredis,
            "config",
            RedisConfig(
                REDIS_INSTALLED=False,
                REDIS_HOST="",
                REDIS_PORT="",
                REDIS_PASSWORD="",
                REDIS_TIMEOUT=2,
                REDIS_USE_SSL=False,
            ),
        )

        # set_value/get_value should appear to work now, but no caching takes place
        DhosRedis.set_value("KEY", "VALUE")
        assert DhosRedis.get_value("KEY") == None

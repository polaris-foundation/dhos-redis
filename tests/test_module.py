from pytest_mock import MockFixture

from dhosredis import DhosRedis, get_value, set_value


class TestModule:
    def test_get_value(self, mocker: MockFixture) -> None:
        mock_get = mocker.patch.object(DhosRedis, "get_value", return_value=1)
        value = get_value("value")
        assert mock_get.call_count == 1
        assert value == 1

    def test_get_value_default(self, mocker: MockFixture) -> None:
        mock_get = mocker.patch.object(DhosRedis, "get_value", return_value=None)
        value = get_value("value", default="other")
        assert mock_get.call_count == 1
        assert value == "other"

    def test_set_value_success(self, mocker: MockFixture) -> None:
        mock_set = mocker.patch.object(DhosRedis, "set_value", return_value=True)
        set_value("key", "value")
        assert mock_set.call_count == 1
        assert mock_set.call_args == ((), {"key": "key", "value": "value"})

    def test_set_value_failure(self, mocker: MockFixture) -> None:
        mock_set = mocker.patch.object(DhosRedis, "set_value", return_value=False)
        set_value("key", "value")
        assert mock_set.call_count == 1
        assert mock_set.call_args == ((), {"key": "key", "value": "value"})

from tests import TestCase
import os
import time
from unittest.mock import patch, MagicMock
from src.masonite.broadcasting import Channel, PrivateChannel
import pytest


class CanBroadcast:
    def broadcast_on(self):
        return Channel(f"order.{self.order_id}")

    def broadcast_with(self):
        return vars(self)

    def broadcast_as(self):
        return self.__class__.__name__


class OrderProcessed(CanBroadcast):
    def __init__(self):
        self.order_id = 1


def _mock_pusher_conn():
    conn = MagicMock()
    conn.trigger.return_value = {"status": 200}
    return conn


_PATCH_TARGET = (
    "src.masonite.broadcasting.drivers.PusherDriver.PusherDriver.get_connection"
)


@pytest.mark.integrations
class TestFileCache(TestCase):
    def setUp(self):
        super().setUp()
        self.application.make("cache")
        self.driver = self.application.make("broadcast")

    def test_can_get_file_driver(self):
        mock_conn = _mock_pusher_conn()
        with patch(_PATCH_TARGET, return_value=mock_conn):
            result = self.driver.channel("order.1", "status", {"status": "processed"})
        mock_conn.trigger.assert_called_once_with("order.1", "status", {"status": "processed"})

    def test_can_fire_class(self):
        mock_conn = _mock_pusher_conn()
        with patch(_PATCH_TARGET, return_value=mock_conn):
            self.driver.channel(OrderProcessed())
        mock_conn.trigger.assert_called_once()

import pytest
from boto3.exceptions import ResourceNotExistsError

from src.masonite.exceptions import InvalidConfigurationSetup
from tests import TestCase


class TestAmazonServices(TestCase):
    def test_clients(self):
        amazon = self.application.make("amazon")
        # valid clients
        s3_client = amazon.client("s3")
        assert s3_client is not None
        # with a "service" key
        gateway1 = amazon.client("api_gateway")
        assert gateway1 is not None

        # invalid options
        with pytest.raises(InvalidConfigurationSetup) as e_info:
            amazon.client("some_gateway")
        assert (
            str(e_info.value)
            .lower()
            .startswith("no amazon service configuration found")
        )
        with pytest.raises(InvalidConfigurationSetup) as e_info:
            amazon.client("disabled")
        assert str(e_info.value).lower().endswith("is not active")

    def test_resources(self):
        amazon = self.application.make("amazon")
        # valid resources
        s3_resource = amazon.resource("s3")
        assert s3_resource is not None

        # invalid resource interface with "service" key
        with pytest.raises(ResourceNotExistsError) as e_info:
            gateway1 = amazon.resource("api_gateway")
        assert "resource does not exist" in str(e_info.value).lower()

        # invalid options
        with pytest.raises(InvalidConfigurationSetup) as e_info:
            amazon.resource("some_gateway")
        assert (
            str(e_info.value)
            .lower()
            .startswith("no amazon service configuration found")
        )
        with pytest.raises(InvalidConfigurationSetup) as e_info:
            amazon.resource("disabled")
        assert str(e_info.value).lower().endswith("is not active")

    def test_service_config(self):
        amazon = self.application.make("amazon")

        full_config = amazon.service_config("s3", True)
        assert all(k in full_config for k in ("options", "buckets"))

        limited_config = amazon.service_config("s3")
        assert limited_config.get("options", False) == False
        assert len(limited_config) == 1
        assert len(limited_config.get("buckets")) == 2

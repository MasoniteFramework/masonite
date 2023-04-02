import warnings
from typing import Any

from botocore.client import BaseClient

from ..exceptions import InvalidConfigurationSetup


class AmazonServices:
    """Wrapper for AWS services"""

    def __init__(self, application, config=None):
        self.application = application
        self.config = config or {}
        self._resources = {}
        self._clients = {}

    def services(self):
        """list configured service names"""
        return self.config.keys()

    def client(self, name=None) -> "BaseClient|None":
        """get a named client interface"""
        if not name:
            return None

        try:
            return self._clients[name]
        except KeyError:
            # client not yet initialised
            client = self._setup_client(name)
            self._clients[name] = client = client
            return client

    def resource(self, name=None) -> "Any|None":
        """get a named resource interface"""
        if not name:
            return None

        try:
            warnings.warn(
                "The 'resource' interface is no longer being updated by Amazon in boto3.\n \
                It is recommended to use the 'client' interface instead",
                DeprecationWarning,
            )
            return self._resources[name]
        except KeyError:
            # resource not yet initialised
            resource = self._setup_resource(name)
            self._resources[name] = resource
            return resource

    def _setup_client(self, name: str = None) -> BaseClient:
        """setup the service using the 'client' API"""
        try:
            import boto3
            from botocore.exceptions import UnknownServiceError

            try:
                svc_config = self.service_config(name, True)

                service_name = svc_config.get("service", name)
                extra_config = svc_config.get("options", {})

                return boto3.client(service_name, **extra_config)
            except UnknownServiceError as error:
                raise InvalidConfigurationSetup(
                    f"Unknown client interface '{service_name}': {error}"
                )
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'boto3' library. Run 'pip install boto3' to fix this."
            )

    def service_config(self, name: str, full: bool = False) -> dict:
        """get the service config"""
        try:
            svc_config: dict = self.config[name]
            # services are active by default
            if not svc_config.get("active", True):
                raise InvalidConfigurationSetup(f"Resource '{name} is not active")

            if not full:
                # remove internal configuration keys (if any)
                svc_config.pop("service", None)
                svc_config.pop("options", None)
                svc_config.pop("active", None)

            return svc_config
        except KeyError:
            raise InvalidConfigurationSetup(
                f"No Amazon Service configuration found for: {name}"
            )

    def _setup_resource(self, name: str = None) -> Any:
        """setup the service using the 'resource' interface"""
        try:
            import boto3
            from botocore.exceptions import UnknownServiceError

            try:
                svc_config = self.service_config(name, True)

                service_name = svc_config.get("service", name)
                extra_config = svc_config.get("options", {})

                return boto3.resource(service_name, **extra_config)
            except UnknownServiceError as error:
                raise InvalidConfigurationSetup(
                    f"Unknown resource interface '{service_name}': {error}"
                )
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'boto3' or 'botocore' module. Run 'pip install boto3' to fix this."
            )

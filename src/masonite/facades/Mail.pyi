from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..mail import Mailable

class Mail:
    """Mail facade."""

    def add_driver(name: str, driver: Any): ...
    def set_configuration(config: dict) -> "Mail": ...
    def get_driver(name: str = None) -> Any: ...
    def get_config_options(driver: str = None) -> dict: ...
    def mailable(mailable: "Mailable") -> "Mail": ...
    def send(driver: str = None): ...

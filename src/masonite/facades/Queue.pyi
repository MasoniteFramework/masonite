from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..queues import Queueable

class Queue:
    """Queue facade class allowing to queue jobs to be run asynchronously."""

    def add_driver(name: str, driver: str) -> None: ...
    def get_driver(name: str) -> Any: ...
    def set_configuration(config: dict) -> "Queue": ...
    def get_config_options(driver: str) -> dict: ...
    def push(*jobs: "Queueable", **options) -> None:
        """Push given job(s) into the queue using the given (or default) queue driver. The queue
        can be given in the options."""
        ...
    def consume(options: dict):
        """Consume job(s) pushed on the queue using the given (or default) queue driver. The queue
        can be given in the options."""
        ...
    def retry(options: dict):
        """Retry failed job(s) on the queue using the given (or default) queue driver. The queue
        can be given in the options."""
        ...

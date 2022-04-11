from typing import Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..dumps import Dump as DumpObject

class Dump:
    """Dumper facade."""

    def clear(self) -> "Dump":
        """Clear all dumped data"""
        ...
    def dd(*objects: List[Any]):
        """Dump all provided args and die, raising a DumpException."""
        ...
    def dump(*objects: List[Any]):
        """Dump all provided args and continue code execution. This does not raise a DumpException."""
        ...
    def get_dumps(ascending: bool = False) -> List[DumpObject]:
        """Get all dumps as Dump objects. If ascending is True, get dumps from oldest to most recents."""
        ...
    def last(self) -> DumpObject:
        """Return last added dump."""
        ...
    def get_serialized_dumps(ascending: bool = False) -> List[dict]:
        """Get all dumps as dict. If ascending is True, sort dumps from oldest to most recents."""
        ...

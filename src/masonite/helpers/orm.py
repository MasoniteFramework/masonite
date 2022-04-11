from typing import TYPE_CHECKING, Type

from ..facades import Loader
from ..exceptions import RecordNotFoundException

if TYPE_CHECKING:
    from masoniteorm import Model


def find_or_fail(model: "str|Type[Model]", pk: int) -> "Type[Model]":
    """
    Find model by primary key or raise RecordNotFoundException which will be rendered as
    HTTP 404 error.

    model can be a model class or a the python model path relative to project root.
    """
    if isinstance(model, str):
        model_name = model.split(".")[-1]
        model_class = Loader.get_object(model, model_name)
    else:
        model_class = model

    record = model_class.find(pk)
    if not record:
        raise RecordNotFoundException()

    return record

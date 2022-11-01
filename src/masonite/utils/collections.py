import json
import random
import operator
from functools import reduce
from dotty_dict import Dotty
from typing import Any, Callable, Iterable

from .structures import data_get


class Collection:
    """Wraps various data types to make working with them easier."""

    def __init__(self, items: "Iterable" = None):
        self._items = items or []
        self.__appends__ = []

    def take(self, number: int) -> "Collection":
        """Takes a specific number of results from the items and returns a sub-collection of those
        items."""
        if number < 0:
            return self[number:]

        return self[:number]

    def first(self, callback: "Callable" = None) -> "Any":
        """Takes the first item of the collection. If a callback is given then the first item will
        be the first item of the filtered collection."""
        filtered = self
        if callback:
            filtered = self.filter(callback)
        response = None
        if filtered:
            response = filtered[0]
        return response

    def last(self, callback: "Callable" = None) -> "Any":
        """Takes the last item of the collection. If a callback is given then the last item will
        be the last item of the filtered collection."""
        filtered = self
        if callback:
            filtered = self.filter(callback)
        return filtered[-1]

    def all(self) -> "Iterable":
        """Returns all the items in the Collection."""
        return self._items

    def avg(self, key: str = None) -> float:
        """Returns the average of the items in the collection. If a key is given it will return
        the average of all the values at key."""
        result = 0
        items = self._get_value(key) or self._items
        try:
            result = sum(items) / len(items)
        except TypeError:
            pass
        return result

    def max(self, key: str = None) -> "float|int":
        """Returns the maximum value of the items in the collection. If a key is given it will return
        the maximum of all the values at key."""
        result = 0
        items = self._get_value(key) or self._items

        try:
            return max(items)
        except (TypeError, ValueError):
            pass
        return result

    def min(self, key: str = None) -> "float|int":
        """Returns the minimum value of the items in the collection. If a key is given it will return
        the minimum of all the values at key."""
        result = 0
        items = self._get_value(key) or self._items

        try:
            return min(items)
        except (TypeError, ValueError):
            pass
        return result

    def chunk(self, size: int) -> "Collection":
        """Chunks the collection into collection chunks of the given size. This will return a collection of
        chunks."""
        items = []
        for i in range(0, self.count(), size):
            items.append(self[i : i + size])
        return self.__class__(items)

    def collapse(self) -> "Collection":
        """Collapse the collection (if each item in the collection is an iterable itself) in a
        flat collection."""
        items = []
        for item in self:
            items += self.__get_items(item)
        return self.__class__(items)

    def contains(self, key: str, value: "Any" = None) -> bool:
        """Check if an item of the collection contains the given value at given key or attribute.
        Items can be dictionaries or classes."""
        if value:
            return self.contains(lambda x: self._data_get(x, key) == value)

        if self._check_is_callable(key, raise_exception=False):
            return self.first(key) is not None

        return key in self

    def count(self) -> int:
        """Get the number of items in the collection."""
        return len(self._items)

    def diff(self, items: "Iterable") -> "Collection":
        """Get the difference between the given set of items and items in the collection."""
        items = self.__get_items(items)
        return self.__class__([x for x in self if x not in items])

    def each(self, callback: "Callable") -> None:
        """Run the callback for each item of the collection while result is truthy and update
        the collection with the callback result. This will edit the collection 'in place'."""
        self._check_is_callable(callback)

        for k, v in enumerate(self):
            result = callback(v)
            if not result:
                break
            self[k] = result

    def every(self, callback: "Callable") -> list:
        """Run the callback for every item of the collection and returns a list with callback
        result for each item."""
        self._check_is_callable(callback)
        return all([callback(x) for x in self])

    def filter(self, callback: "Callable") -> "Collection":
        """Filter the collection with the given callable."""
        self._check_is_callable(callback)
        return self.__class__(list(filter(callback, self)))

    def flatten(self) -> "Collection":
        """Recursively flatten the collection into a new collection. Each item will be 'flattened'."""

        def _flatten(items):
            if isinstance(items, dict):
                for v in items.values():
                    for x in _flatten(v):
                        yield x
            elif isinstance(items, list):
                for i in items:
                    for j in _flatten(i):
                        yield j
            else:
                yield items

        return self.__class__(list(_flatten(self._items)))

    def forget(self, *keys: str) -> "Collection":
        """Remove items with the given values or keys from the collection."""
        keys = reversed(sorted(keys))

        for key in keys:
            del self[key]

        return self

    def for_page(self, page: int, number: int) -> "Collection":
        """Get the collection at the given page with the given items per page. This will take a
        slice from the collection."""
        return self.__class__(self[page:number])

    def get(self, key: str, default: Any = None) -> Any:
        """Get item at the given key (or the default value if not found) in the collection."""
        try:
            return self[key]
        except IndexError:
            pass

        return self._value(default)

    def implode(self, glue=",", key=None) -> str:
        """Join all item of the collection with the given 'glue' character. If a key is given,
        only items values at keys will be joined."""
        first = self.first()
        if not isinstance(first, str) and key:
            return glue.join(self.pluck(key))
        return glue.join([str(x) for x in self])

    def is_empty(self) -> bool:
        """Check if collection is empty."""
        return not self

    def map(self, callback: "Callable") -> "Collection":
        """Map each item of the collection with the given callable."""
        self._check_is_callable(callback)
        items = [callback(x) for x in self]
        return self.__class__(items)

    def map_into(self, cls, method=None, **kwargs) -> "Collection":
        """Map each item of the collection into instances of the given class or into result of the
        class method called on the item with the given arguments."""
        results = []
        for item in self:
            if method:
                results.append(getattr(cls, method)(item, **kwargs))
            else:
                results.append(cls(item))

        return self.__class__(results)

    def merge(self, items=list) -> "Collection":
        """Append given list of items to the collection."""
        if not isinstance(items, list):
            raise ValueError("Unable to merge uncompatible types")

        items = self.__get_items(items)

        self._items += items
        return self

    def pluck(self, value: Any, key: str = None) -> "Collection":
        """Get a sub collection with the values at given key. If value is provided, the collection
        will be filtered by keys equal to the value."""
        if key:
            attributes = {}
        else:
            attributes = []

        if isinstance(self._items, dict):
            return Collection([self._items.get(value)])

        for item in self:
            if isinstance(item, dict):
                iterable = item.items()
            elif hasattr(item, "serialize"):
                iterable = item.serialize().items()
            else:
                iterable = self.all().items()

            for k, v in iterable:
                if k == value:
                    if key:
                        attributes[self._data_get(item, key)] = self._data_get(
                            item, value
                        )
                    else:
                        attributes.append(v)

        return Collection(attributes)

    def pop(self) -> Any:
        """Removes and returns last item in the collection."""
        last = self._items.pop()
        return last

    def prepend(self, item) -> "Collection":
        """Preprend the given item in the collection."""
        self._items.insert(0, item)
        return self

    def pull(self, key: Any) -> Any:
        """Get and remove the given item from the collection."""
        value = self.get(key)
        self.forget(key)
        return value

    def push(self, item: Any) -> "Collection":
        """Append the given item to the collection."""
        self._items.append(item)
        return self

    def put(self, key: Any, value: Any) -> "Collection":
        """Set the value of the given item in the collection."""
        self[key] = value
        return self

    def random(self, count: int = None) -> "Any|Collection":
        """Returns a random item of the collection. If count is given a collection with 'count'
        randomly selected items will be returned."""
        collection_count = self.count()
        if collection_count == 0:
            return None
        elif count and count > collection_count:
            raise ValueError("count argument must be inferior to collection length.")
        elif count:
            self._items = random.sample(self._items, k=count)
            return self
        else:
            return random.choice(self._items)

    def reduce(self, callback: "Callable", initial: int = 0) -> Any:
        """Reduce the collection into one value by applying given callback on items and starting
        from the given initial index in the collection."""
        return reduce(callback, self, initial)

    def reject(self, callback: "Callable"):
        # @M5 not sure that this is useful, isn't it a filter method ?
        self._check_is_callable(callback)

        items = self._get_value(callback) or self._items
        self._items = items

    def reverse(self) -> None:
        """Reverse (in place) the order of items in the collection."""
        self._items = self[::-1]

    def serialize(self) -> list:
        """Serialize recursively all items in the collection. If items (or sub-items) implements
        serialize() or to_dict(), the serialization will be done accordingly to this method."""

        def _serialize(item):
            if self.__appends__:
                item.set_appends(self.__appends__)

            if hasattr(item, "serialize"):
                return item.serialize()
            elif hasattr(item, "to_dict"):
                return item.to_dict()
            return item

        return list(map(_serialize, self))

    def add_relation(self, result=None):
        # @M5: very specific ORM method, ideally masonite-orm should subclass the class in
        # ORMCollection(Collection) and adds ORM specific methods in it
        for model in self._items:
            model.add_relations(result or {})

        return self

    def shift(self) -> Any:
        """Get and remove first item in the collection."""
        return self.pull(0)

    def sort(self, key: Any = None) -> "Collection":
        """Sort all items in the collection according to their values. If a key is given, items
        will be sorted by this key."""
        if key:
            self._items.sort(key=lambda x: x[key], reverse=False)
            return self

        self._items = sorted(self)
        return self

    def sum(self, key: Any = None) -> "float|int":
        """Try to returns a sum of all items in the collection at the given key."""
        result = 0
        items = self._get_value(key) or self._items
        try:
            result = sum(items)
        except TypeError:
            pass
        return result

    def to_json(self, **kwargs) -> str:
        """Dumps the collection as JSON string (serializing all items)."""
        return json.dumps(self.serialize(), **kwargs)

    def group_by(self, key: Any) -> "Collection":
        """Group all items by the given key into a new collection."""
        from itertools import groupby

        self.sort(key)

        new_dict = {}

        for k, v in groupby(self._items, key=lambda x: x[key]):
            new_dict.update({k: list(v)})

        return Collection(new_dict)

    def transform(self, callback: "Callable") -> None:
        """Apply the given callback on each item in the collection. The collection is modified
        in place as Collection.map() is returning a new collection."""
        self._check_is_callable(callback)
        self._items = self._get_value(callback)

    def unique(self, key: Any = None) -> "Collection":
        """Try to remove all duplicates values in the collection. If key is given, remove all
        duplicate values of the item keys."""
        if not key:
            items = list(set(self._items))
            return self.__class__(items)

        keys = set()
        items = []
        if isinstance(self.all(), dict):
            return self

        for item in self:
            if isinstance(item, dict):
                comparison = item.get(key)
            elif isinstance(item, str):
                comparison = item
            else:
                comparison = getattr(item, key)
            if comparison not in keys:
                items.append(item)
                keys.add(comparison)

        return self.__class__(items)

    def where(self, key: Any, *args) -> "Collection":
        """Filter items of the collection with a comparison of the key with a logical operator.
        Example: where("id", ">", 3)
        """
        op = "=="
        value = args[0]

        if len(args) >= 2:
            op = args[0]
            value = args[1]

        attributes = []

        for item in self._items:
            if isinstance(item, dict):
                comparison = item.get(key)
            else:
                comparison = getattr(item, key)
            if self._make_comparison(comparison, value, op):
                attributes.append(item)

        return self.__class__(attributes)

    def zip(self, items: "Iterable") -> "Collection":
        """Zip the given items into a Collection where each item is a tuple of the two zipped
        values."""
        items = self.__get_items(items)
        if not isinstance(items, list):
            raise ValueError("The 'items' parameter must be a list or a Collection")

        _items = []
        for x, y in zip(self, items):
            _items.append([x, y])
        return self.__class__(_items)

    def set_appends(self, appends: list) -> "Collection":
        """
        Set the attributes that should be appended to the Collection.

        :rtype: list
        """
        # @M5: same as for add_relations()
        self.__appends__ += appends
        return self

    def _get_value(self, key):
        if not key:
            return None

        items = []
        for item in self:
            if isinstance(key, str):
                if hasattr(item, key) or (key in item):
                    items.append(getattr(item, key, item[key]))
            elif callable(key):
                result = key(item)
                if result:
                    items.append(result)
        return items

    def _data_get(self, item, key, default=None):
        try:
            if isinstance(item, (list, tuple)):
                item = item[key]
            elif isinstance(item, (dict, Dotty)):
                item = data_get(item, key, default)
            elif isinstance(item, object):
                item = getattr(item, key)
        except (IndexError, AttributeError, KeyError, TypeError):
            return self._value(default)

        return item

    def _value(self, value):
        if callable(value):
            return value()
        return value

    def _check_is_callable(self, callback, raise_exception=True):
        if not callable(callback):
            if not raise_exception:
                return False
            raise ValueError("The 'callback' should be a function")
        return True

    def _make_comparison(self, a, b, op):
        operators = {
            "<": operator.lt,
            "<=": operator.le,
            "==": operator.eq,
            "!=": operator.ne,
            ">": operator.gt,
            ">=": operator.ge,
        }
        return operators[op](a, b)

    def __iter__(self):
        for item in self._items:
            yield item

    def __eq__(self, other):
        if isinstance(other, Collection):
            return other == other.all()
        return other == self._items

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__class__(self._items[item])

        return self._items[item]

    def __setitem__(self, key, value):
        self._items[key] = value

    def __delitem__(self, key):
        del self._items[key]

    def __ne__(self, other):
        other = self.__get_items(other)
        return other != self._items

    def __len__(self):
        return len(self._items)

    def __le__(self, other):
        other = self.__get_items(other)
        return self._items <= other

    def __lt__(self, other):
        other = self.__get_items(other)
        return self._items < other

    def __ge__(self, other):
        other = self.__get_items(other)
        return self._items >= other

    def __gt__(self, other):
        other = self.__get_items(other)
        return self._items > other

    @classmethod
    def __get_items(cls, items):
        if isinstance(items, Collection):
            items = items.all()

        return items


def collect(iterable: "Iterable") -> "Collection":
    """Transform an iterable into a collection."""
    return Collection(iterable)


def flatten(iterable: "Iterable") -> list:
    """Flatten all sub-iterables of an iterable structure (recursively)."""
    flat_list = []
    for item in iterable:
        if isinstance(item, list):
            for subitem in flatten(item):
                flat_list.append(subitem)
        else:
            flat_list.append(item)

    return flat_list

import json
import random
import operator
from functools import reduce
from dotty_dict import Dotty

from .structures import data_get


class Collection:
    """Wraps various data types to make working with them easier."""

    def __init__(self, items=None):
        self._items = items or []
        self.__appends__ = []

    def take(self, number: int):
        """Takes a specific number of results from the items.

        Arguments:
            number {integer} -- The number of results to take.

        Returns:
            int
        """
        if number < 0:
            return self[number:]

        return self[:number]

    def first(self, callback=None):
        """Takes the first result in the items.

        If a callback is given then the first result will be the result after the filter.

        Keyword Arguments:
            callback {callable} -- Used to filter the results before returning the first item. (default: {None})

        Returns:
            mixed -- Returns whatever the first item is.
        """
        filtered = self
        if callback:
            filtered = self.filter(callback)
        response = None
        if filtered:
            response = filtered[0]
        return response

    def last(self, callback=None):
        """Takes the last result in the items.

        If a callback is given then the last result will be the result after the filter.

        Keyword Arguments:
            callback {callable} -- Used to filter the results before returning the last item. (default: {None})

        Returns:
            mixed -- Returns whatever the last item is.
        """
        filtered = self
        if callback:
            filtered = self.filter(callback)
        return filtered[-1]

    def all(self):
        """Returns all the items.

        Returns:
            mixed -- Returns all items.
        """
        return self._items

    def avg(self, key=None):
        """Returns the average of the items.

        If a key is given it will return the average of all the values of the key.

        Keyword Arguments:
            key {string} -- The key to use to find the average of all the values of that key. (default: {None})

        Returns:
            int -- Returns the average.
        """
        result = 0
        items = self._get_value(key) or self._items
        try:
            result = sum(items) / len(items)
        except TypeError:
            pass
        return result

    def max(self, key=None):
        """Returns the average of the items.

        If a key is given it will return the average of all the values of the key.

        Keyword Arguments:
            key {string} -- The key to use to find the average of all the values of that key. (default: {None})

        Returns:
            int -- Returns the average.
        """
        result = 0
        items = self._get_value(key) or self._items

        try:
            return max(items)
        except (TypeError, ValueError):
            pass
        return result

    def chunk(self, size: int):
        """Chunks the items.

        Keyword Arguments:
            size {integer} -- The number of values in each chunk.

        Returns:
            int -- Returns the average.
        """
        items = []
        for i in range(0, self.count(), size):
            items.append(self[i : i + size])
        return self.__class__(items)

    def collapse(self):
        items = []
        for item in self:
            items += self.__get_items(item)
        return self.__class__(items)

    def contains(self, key, value=None):
        if value:
            return self.contains(lambda x: self._data_get(x, key) == value)

        if self._check_is_callable(key, raise_exception=False):
            return self.first(key) is not None

        return key in self

    def count(self):
        return len(self._items)

    def diff(self, items):
        items = self.__get_items(items)
        return self.__class__([x for x in self if x not in items])

    def each(self, callback):
        self._check_is_callable(callback)

        for k, v in enumerate(self):
            result = callback(v)
            if not result:
                break
            self[k] = result

    def every(self, callback):
        self._check_is_callable(callback)
        return all([callback(x) for x in self])

    def filter(self, callback):
        self._check_is_callable(callback)
        return self.__class__(list(filter(callback, self)))

    def flatten(self):
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

    def forget(self, *keys):
        keys = reversed(sorted(keys))

        for key in keys:
            del self[key]

        return self

    def for_page(self, page, number):
        return self.__class__(self[page:number])

    def get(self, key, default=None):
        try:
            return self[key]
        except IndexError:
            pass

        return self._value(default)

    def implode(self, glue=",", key=None):
        first = self.first()
        if not isinstance(first, str) and key:
            return glue.join(self.pluck(key))
        return glue.join([str(x) for x in self])

    def is_empty(self):
        return not self

    def map(self, callback):
        self._check_is_callable(callback)
        items = [callback(x) for x in self]
        return self.__class__(items)

    def map_into(self, cls, method=None, **kwargs):
        results = []
        for item in self:
            if method:
                results.append(getattr(cls, method)(item, **kwargs))
            else:
                results.append(cls(item))

        return self.__class__(results)

    def merge(self, items):
        if not isinstance(items, list):
            raise ValueError("Unable to merge uncompatible types")

        items = self.__get_items(items)

        self._items += items
        return self

    def pluck(self, value, key=None):
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

    def pop(self):
        last = self._items.pop()
        return last

    def prepend(self, value):
        self._items.insert(0, value)
        return self

    def pull(self, key):
        value = self.get(key)
        self.forget(key)
        return value

    def push(self, value):
        self._items.append(value)

    def put(self, key, value):
        self[key] = value
        return self

    def random(self, count=None):
        """Returns a random item of the collection."""
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

    def reduce(self, callback, initial=0):
        return reduce(callback, self, initial)

    def reject(self, callback):
        self._check_is_callable(callback)

        items = self._get_value(callback) or self._items
        self._items = items

    def reverse(self):
        self._items = self[::-1]

    def serialize(self):
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
        for model in self._items:
            model.add_relations(result or {})

        return self

    def shift(self):
        return self.pull(0)

    def sort(self, key=None):
        if key:
            self._items.sort(key=lambda x: x[key], reverse=False)
            return self

        self._items = sorted(self)
        return self

    def sum(self, key=None):
        result = 0
        items = self._get_value(key) or self._items
        try:
            result = sum(items)
        except TypeError:
            pass
        return result

    def to_json(self, **kwargs):
        return json.dumps(self.serialize(), **kwargs)

    def group_by(self, key):

        from itertools import groupby

        self.sort(key)

        new_dict = {}

        for k, v in groupby(self._items, key=lambda x: x[key]):
            new_dict.update({k: list(v)})

        return Collection(new_dict)

    def transform(self, callback):
        self._check_is_callable(callback)
        self._items = self._get_value(callback)

    def unique(self, key=None):
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

    def where(self, key, *args):
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

    def zip(self, items):
        items = self.__get_items(items)
        if not isinstance(items, list):
            raise ValueError("The 'items' parameter must be a list or a Collection")

        _items = []
        for x, y in zip(self, items):
            _items.append([x, y])
        return self.__class__(_items)

    def set_appends(self, appends):
        """
        Set the attributes that should be appended to the Collection.

        :rtype: list
        """
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


def collect(iterable):
    """Transform an iterable into a collection."""
    return Collection(iterable)


def flatten(iterable):
    """Flatten all sub-iterables of an iterable structure (recursively)."""
    flat_list = []
    for item in iterable:
        if isinstance(item, list):
            for subitem in flatten(item):
                flat_list.append(subitem)
        else:
            flat_list.append(item)

    return flat_list

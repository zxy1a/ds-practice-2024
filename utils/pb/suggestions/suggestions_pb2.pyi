from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VectorClock(_message.Message):
    __slots__ = ("entries",)
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.ScalarMap[str, int]
    def __init__(self, entries: _Optional[_Mapping[str, int]] = ...) -> None: ...

class SuggestionsRequest(_message.Message):
    __slots__ = ("orderID", "title", "author", "vector_clock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    title: str
    author: str
    vector_clock: VectorClock
    def __init__(self, orderID: _Optional[str] = ..., title: _Optional[str] = ..., author: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class SuggestionsResponse(_message.Message):
    __slots__ = ("titles", "vector_clock")
    TITLES_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    titles: _containers.RepeatedScalarFieldContainer[str]
    vector_clock: VectorClock
    def __init__(self, titles: _Optional[_Iterable[str]] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

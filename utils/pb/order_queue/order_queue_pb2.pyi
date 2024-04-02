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

class OrderRequest(_message.Message):
    __slots__ = ("orderId", "userId", "bookTitles", "vector_clock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    BOOKTITLES_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    userId: str
    bookTitles: _containers.RepeatedScalarFieldContainer[str]
    vector_clock: VectorClock
    def __init__(self, orderId: _Optional[str] = ..., userId: _Optional[str] = ..., bookTitles: _Optional[_Iterable[str]] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ("success", "message", "vector_clock")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    vector_clock: VectorClock
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class DequeueRequest(_message.Message):
    __slots__ = ("executorId",)
    EXECUTORID_FIELD_NUMBER: _ClassVar[int]
    executorId: str
    def __init__(self, executorId: _Optional[str] = ...) -> None: ...

class ElectionRequest(_message.Message):
    __slots__ = ("executorId",)
    EXECUTORID_FIELD_NUMBER: _ClassVar[int]
    executorId: str
    def __init__(self, executorId: _Optional[str] = ...) -> None: ...

class ElectionResponse(_message.Message):
    __slots__ = ("isLeader",)
    ISLEADER_FIELD_NUMBER: _ClassVar[int]
    isLeader: bool
    def __init__(self, isLeader: bool = ...) -> None: ...

class ClearLeaderRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClearLeaderResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

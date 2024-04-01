from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

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

class CheckUserDataRequest(_message.Message):
    __slots__ = ("orderID", "user", "vector_clock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    user: User
    vector_clock: VectorClock
    def __init__(self, orderID: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class CheckUserDataResponse(_message.Message):
    __slots__ = ("is_fraud", "reason", "vector_clock")
    IS_FRAUD_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    is_fraud: bool
    reason: str
    vector_clock: VectorClock
    def __init__(self, is_fraud: bool = ..., reason: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class FraudDetectionRequest(_message.Message):
    __slots__ = ("orderID", "number", "expirationDate", "vector_clock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    number: str
    expirationDate: str
    vector_clock: VectorClock
    def __init__(self, orderID: _Optional[str] = ..., number: _Optional[str] = ..., expirationDate: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class FraudDetectionResponse(_message.Message):
    __slots__ = ("is_fraud", "reason", "vector_clock")
    IS_FRAUD_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    is_fraud: bool
    reason: str
    vector_clock: VectorClock
    def __init__(self, is_fraud: bool = ..., reason: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("name", "contact", "address")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    address: str
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...

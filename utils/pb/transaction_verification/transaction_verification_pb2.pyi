from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("name", "contact", "address")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    address: str
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...

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

class CreditCard(_message.Message):
    __slots__ = ("number", "expirationDate", "cvv")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    number: str
    expirationDate: str
    cvv: str
    def __init__(self, number: _Optional[str] = ..., expirationDate: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...

class TransactionVerificationRequest(_message.Message):
    __slots__ = ("orderID", "title", "user", "creditCard", "vector_clock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    title: str
    user: User
    creditCard: CreditCard
    vector_clock: VectorClock
    def __init__(self, orderID: _Optional[str] = ..., title: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., creditCard: _Optional[_Union[CreditCard, _Mapping]] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class TransactionVerificationResponse(_message.Message):
    __slots__ = ("is_valid", "message", "vector_clock")
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    message: str
    vector_clock: VectorClock
    def __init__(self, is_valid: bool = ..., message: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class VerifyCreditCardFormatRequest(_message.Message):
    __slots__ = ("orderID", "creditCard", "vector_clock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    creditCard: CreditCard
    vector_clock: VectorClock
    def __init__(self, orderID: _Optional[str] = ..., creditCard: _Optional[_Union[CreditCard, _Mapping]] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class VerifyCreditCardFormatResponse(_message.Message):
    __slots__ = ("is_valid", "message", "vector_clock")
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    message: str
    vector_clock: VectorClock
    def __init__(self, is_valid: bool = ..., message: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class VerifyOrderItemsRequest(_message.Message):
    __slots__ = ("orderID", "itemTitles", "vector_clock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    ITEMTITLES_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    itemTitles: _containers.RepeatedScalarFieldContainer[str]
    vector_clock: VectorClock
    def __init__(self, orderID: _Optional[str] = ..., itemTitles: _Optional[_Iterable[str]] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class VerifyOrderItemsResponse(_message.Message):
    __slots__ = ("is_valid", "message", "vector_clock")
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    message: str
    vector_clock: VectorClock
    def __init__(self, is_valid: bool = ..., message: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class VerifyMandatoryUserDataRequest(_message.Message):
    __slots__ = ("orderID", "user", "vector_clock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    user: User
    vector_clock: VectorClock
    def __init__(self, orderID: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class VerifyMandatoryUserDataResponse(_message.Message):
    __slots__ = ("is_valid", "message", "vector_clock")
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    message: str
    vector_clock: VectorClock
    def __init__(self, is_valid: bool = ..., message: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

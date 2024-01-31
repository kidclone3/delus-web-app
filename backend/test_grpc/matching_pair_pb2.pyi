from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PairType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DRIVER: _ClassVar[PairType]
    CUSTOMER: _ClassVar[PairType]
    RESET: _ClassVar[PairType]
DRIVER: PairType
CUSTOMER: PairType
RESET: PairType

class MatchingRequest(_message.Message):
    __slots__ = ["type", "id", "name", "location"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    type: PairType
    id: str
    name: str
    location: str
    def __init__(self, type: _Optional[_Union[PairType, str]] = ..., id: _Optional[str] = ..., name: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class ReturnStatus(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CurrentLocation(_message.Message):
    __slots__ = ["pos_x", "pos_y"]
    POS_X_FIELD_NUMBER: _ClassVar[int]
    POS_Y_FIELD_NUMBER: _ClassVar[int]
    pos_x: int
    pos_y: int
    def __init__(self, pos_x: _Optional[int] = ..., pos_y: _Optional[int] = ...) -> None: ...

class Destination(_message.Message):
    __slots__ = ["pos_x", "pos_y"]
    POS_X_FIELD_NUMBER: _ClassVar[int]
    POS_Y_FIELD_NUMBER: _ClassVar[int]
    pos_x: int
    pos_y: int
    def __init__(self, pos_x: _Optional[int] = ..., pos_y: _Optional[int] = ...) -> None: ...

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MALE: _ClassVar[Gender]
    FEMALE: _ClassVar[Gender]
MALE: Gender
FEMALE: Gender

class HelloRequest(_message.Message):
    __slots__ = ["name", "url", "gender", "map", "addTime"]
    class MapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    ADDTIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    url: str
    gender: Gender
    map: _containers.ScalarMap[str, str]
    addTime: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., url: _Optional[str] = ..., gender: _Optional[_Union[Gender, str]] = ..., map: _Optional[_Mapping[str, str]] = ..., addTime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

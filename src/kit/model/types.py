from sqlalchemy.types import TypeDecorator, Integer
from enum import Enum

class IntEnumType(TypeDecorator):
    impl = Integer
    cache_ok = True

    def __init__(self, enum_cls: type[Enum], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_cls = enum_cls

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, self.enum_cls):
            return value.value
        raise ValueError(f"Expected {self.enum_cls}, got {type(value)}")

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_cls(value)

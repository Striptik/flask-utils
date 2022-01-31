import enum as _enum


class ErrorTypeEnum(str, _enum.Enum):
    SERVER = "server"
    INTEGRITY = "integrity"
    BODY_VALIDATION = "body validation"
    SCHEMA_VALIDATION = "schema validation"

#!python3
from marshmallow import fields
from marshmallow_enum import EnumField
from enum import Enum
from datetime import datetime

from . import BaseSchema, BaseResponse, BaseResponseSchema


class Status(Enum):
    MAINTENANCE = 'MAINTENANCE'
    PREOPEN = 'PREOPEN'
    OPEN = 'OPEN'


class GetStatusData:
    def __init__(self, status: Status) -> None:
        self.status = status


class GetStatusResSchema(BaseSchema):
    __model__ = GetStatusData
    status = EnumField(Status, data_key='status')


class GetStatusRes(BaseResponse):
    def __init__(self, status: int, responsetime: str, data: GetStatusData) -> None:
        super().__init__(status, responsetime)
        self.data = data


class GetStatusResSchema(BaseResponseSchema):
    __model__ = GetStatusRes
    data = fields.Nested(GetStatusResSchema, data_key='data')

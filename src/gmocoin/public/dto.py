#!python3
from marshmallow import fields, pre_load
from marshmallow_enum import EnumField
from enum import Enum
from datetime import datetime

from . import BaseSchema, BaseResponse, BaseResponseSchema


class Status(Enum):
    MAINTENANCE = 'MAINTENANCE'
    PREOPEN = 'PREOPEN'
    OPEN = 'OPEN'


class Symbol(Enum):
    BTC = 'BTC'
    ETH = 'ETH'
    BCH = 'BCH'
    LTC = 'LTC'
    XRP = 'XRP'
    BTC_JPY = 'BTC_JPY'
    ETH_JPY = 'ETH_JPY'
    BCH_JPY = 'BCH_JPY'
    LTC_JPY = 'LTC_JPY'
    XRP_JPY = 'XRP_JPY'


class GetStatusData:
    def __init__(self, status: Status) -> None:
        self.status = status


class GetStatusDataSchema(BaseSchema):
    __model__ = GetStatusData
    status = EnumField(Status, data_key='status')


class GetStatusRes(BaseResponse):
    def __init__(self, status: int, responsetime: str, data: GetStatusData) -> None:
        super().__init__(status, responsetime)
        self.data = data


class GetStatusResSchema(BaseResponseSchema):
    __model__ = GetStatusRes
    data = fields.Nested(GetStatusDataSchema, data_key='data')



class GetTickerData:
    def __init__(self, symbol: Symbol, timestamp: str, volume: float, ask: float, bid: float, high: float, last: float, low: float) -> None:
        self.ask = ask
        self.bid = bid
        self.high = high
        self.last = last
        self.low = low
        self.symbol = symbol
        self.timestamp = timestamp
        self.volume = volume


class GetTickerDataSchema(BaseSchema):
    __model__ = GetTickerData
    ask = fields.Number(data_key='ask')
    bid = fields.Number(data_key='bid')
    high = fields.Number(data_key='high')
    last = fields.Number(data_key='last')
    low = fields.Number(data_key='low')
    symbol = EnumField(Symbol, data_key='symbol')
    timestamp = fields.Str(data_key='timestamp')
    volume = fields.Number(data_key='volume')

    @pre_load
    def convert_none_to_zero(self, in_data, **kwargs):
        for key in ['ask', 'bid', 'high', 'last', 'low']:
            if in_data[key] is None:
                in_data[key] = 0
        return in_data

class GetTickerRes(BaseResponse):
    def __init__(self, status: int, responsetime: str, data: GetTickerData) -> None:
        super().__init__(status, responsetime)
        self.data = data


class GetTickerResSchema(BaseResponseSchema):
    __model__ = GetTickerRes
    data = fields.Nested(GetTickerDataSchema, data_key='data', many=True)

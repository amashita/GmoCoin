#!python3
from marshmallow import fields, pre_load
from marshmallow_enum import EnumField
from enum import Enum
from datetime import datetime
from typing import List

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

class SalesSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


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


class OrderData:
    def __init__(self, price: float, size: float) -> None:
        self.price = price
        self.size = size


class OrderDataSchema(BaseSchema):
    __model__ = OrderData
    price = fields.Number(data_key='price')
    size = fields.Number(data_key='size')

class GetOrderBooksData:
    def __init__(self, asks: List[OrderData], bids: List[OrderData], symbol: Symbol) -> None:
        self.asks = asks
        self.bids = bids
        self.symbol = symbol


class GetOrderBooksDataSchema(BaseSchema):
    __model__ = GetOrderBooksData
    asks = fields.Nested(OrderDataSchema, data_key='asks', many=True)
    bids = fields.Nested(OrderDataSchema, data_key='bids', many=True)
    symbol = EnumField(Symbol, data_key='symbol')


class GetOrderBooksRes(BaseResponse):
    def __init__(self, status: int, responsetime: str, data: GetOrderBooksData) -> None:
        super().__init__(status, responsetime)
        self.data = data


class GetOrderBooksResSchema(BaseResponseSchema):
    __model__ = GetOrderBooksRes
    data = fields.Nested(GetOrderBooksDataSchema, data_key='data')


class TradesPagenation:
    def __init__(self, current_page: int, count: int) -> None:
        self.current_page = current_page
        self.count = count


class TradesPagenationSchema(BaseSchema):
    __model__ = TradesPagenation
    current_page = fields.Int(data_key='currentPage')
    count = fields.Int(data_key='count')


class Trade:
    def __init__(self, price: float, side: SalesSide, size: float, timestamp: str) -> None:
        self.price = price
        self.side = side
        self.size = size
        self.timestamp = timestamp


class TradeSchema(BaseSchema):
    __model__ = Trade
    price = fields.Number(data_key='price')
    side = EnumField(SalesSide, data_key='side')
    size = fields.Number(data_key='size')
    timestamp = fields.Str(data_key='timestamp')


class GetTradesData:
    def __init__(self, pagination: TradesPagenation, trades: List[Trade]) -> None:
        self.pagination = pagination
        self.trades = trades


class GetTradesDataSchema(BaseSchema):
    __model__ = GetTradesData
    pagination = fields.Nested(TradesPagenationSchema, data_key='pagination')
    trades = fields.Nested(TradeSchema, data_key='list', many=True)


class GetTradesRes(BaseResponse):
    def __init__(self, status: int, responsetime: str, data: GetOrderBooksData) -> None:
        super().__init__(status, responsetime)
        self.data = data


class GetTradesResSchema(BaseResponseSchema):
    __model__ = GetTradesRes
    data = fields.Nested(GetTradesDataSchema, data_key='data')

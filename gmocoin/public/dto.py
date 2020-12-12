#!python3
from marshmallow import fields, pre_load
from marshmallow_enum import EnumField
from enum import Enum
from datetime import datetime
from pytz import timezone
from typing import List
from decimal import Decimal

from ..common.dto import BaseSchema, BaseResponse, BaseResponseSchema, Status, Symbol, SalesSide


class GetStatusData:
    """
    取引所稼動状態データクラスです。
    """
    def __init__(self, status: Status) -> None:
        """
        コンストラクタです。

        Args:
            status:
                ステータスコードを設定します。
        """
        self.status = status


class GetStatusDataSchema(BaseSchema):
    """
    取引所稼動状態データスキーマクラスです。
    """
    __model__ = GetStatusData
    status = EnumField(Status, data_key='status')


class GetStatusRes(BaseResponse):
    """
    取引所稼動状態レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: GetStatusData) -> None:
        """
        コンストラクタです。

        Args:
            status:
                ステータスコードを設定します。
            responsetime:
                レスポンスタイムを設定します。
            data:
                レスポンスデータを設定します。
        """
        super().__init__(status, responsetime)
        self.data = data


class GetStatusResSchema(BaseResponseSchema):
    """
    取引所稼動状態レスポンススキーマクラスです。
    """
    __model__ = GetStatusRes
    data = fields.Nested(GetStatusDataSchema, data_key='data')



class GetTickerData:
    """
    銘柄最新レートデータクラスです。
    """
    def __init__(self, symbol: Symbol, timestamp: datetime, volume: Decimal, ask: Decimal, bid: Decimal, high: Decimal, last: Decimal, low: Decimal) -> None:
        """
        コンストラクタです。

        Args:
            ask:
            bid:
            high:
            last:
            low:
            symbol:
            timestamp:
            volume:
        """
        self.ask = ask
        self.bid = bid
        self.high = high
        self.last = last
        self.low = low
        self.symbol = symbol
        self.timestamp = timestamp.astimezone(timezone('Asia/Tokyo'))
        self.volume = volume


class GetTickerDataSchema(BaseSchema):
    """
    銘柄最新レートデータスキーマクラスです。
    """
    __model__ = GetTickerData
    ask = fields.Decimal(data_key='ask')
    bid = fields.Decimal(data_key='bid')
    high = fields.Decimal(data_key='high')
    last = fields.Decimal(data_key='last')
    low = fields.Decimal(data_key='low')
    symbol = EnumField(Symbol, data_key='symbol')
    timestamp = fields.DateTime(format='%Y-%m-%dT%H:%M:%S.%fZ', data_key='timestamp')
    volume = fields.Decimal(data_key='volume')

    @pre_load
    def convert_none_to_zero(self, in_data, **kwargs):
        """
        Noneを0に変換する関数です。

        Args:
            in_data:
            kwargs:

        Returns:
            in_data
        """
        for key in ['ask', 'bid', 'high', 'last', 'low']:
            if in_data[key] is None:
                in_data[key] = 0
        return in_data

class GetTickerRes(BaseResponse):
    """
    銘柄最新レートレスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: GetTickerData) -> None:
        """
        コンストラクタです。

        Args:
            status:
                ステータスコードを設定します。
            responsetime:
                レスポンスタイムを設定します。
            data:
                レスポンスデータを設定します。
        """
        super().__init__(status, responsetime)
        self.data = data


class GetTickerResSchema(BaseResponseSchema):
    """
    銘柄最新レートレスポンススキーマクラスです。
    """
    __model__ = GetTickerRes
    data = fields.Nested(GetTickerDataSchema, data_key='data', many=True)


class OrderData:
    """
    注文データクラスです。
    """
    def __init__(self, price: Decimal, size: Decimal) -> None:
        """
        コンストラクタです。

        Args:
            price:
                取引金額を設定します。
            size:
                取引数量を設定します。
        """
        self.price = price
        self.size = size


class OrderDataSchema(BaseSchema):
    """
    注文データスキーマクラスです。
    """
    __model__ = OrderData
    price = fields.Decimal(data_key='price')
    size = fields.Decimal(data_key='size')

class GetOrderBooksData:
    """
    銘柄板データクラスです。
    """
    def __init__(self, asks: List[OrderData], bids: List[OrderData], symbol: Symbol) -> None:
        """
        コンストラクタです。

        Args:
            asks:
                売り注文の情報を設定します。
            bids:
                買い注文の情報を設定します。
            symbol:
                銘柄を設定します。
        """
        self.asks = asks
        self.bids = bids
        self.symbol = symbol


class GetOrderBooksDataSchema(BaseSchema):
    """
    銘柄板データスキーマクラスです。
    """
    __model__ = GetOrderBooksData
    asks = fields.Nested(OrderDataSchema, data_key='asks', many=True)
    bids = fields.Nested(OrderDataSchema, data_key='bids', many=True)
    symbol = EnumField(Symbol, data_key='symbol')


class GetOrderBooksRes(BaseResponse):
    """
    銘柄板レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: GetOrderBooksData) -> None:
        """
        コンストラクタです。

        Args:
            status:
                ステータスコードを設定します。
            responsetime:
                レスポンスタイムを設定します。
            data:
                レスポンスデータを設定します。
        """
        super().__init__(status, responsetime)
        self.data = data


class GetOrderBooksResSchema(BaseResponseSchema):
    """
    銘柄板レスポンススキーマクラスです。
    """
    __model__ = GetOrderBooksRes
    data = fields.Nested(GetOrderBooksDataSchema, data_key='data')


class TradesPagenation:
    """
    取引ページングデータクラスです。
    """
    def __init__(self, current_page: int, count: int) -> None:
        """
        コンストラクタです。

        Args:
            current_page:
                現在のページ番号を設定します。
            count:
                データ数を設定します。
        """
        self.current_page = current_page
        self.count = count


class TradesPagenationSchema(BaseSchema):
    """
    取引ページングデータスキーマクラスです。
    """
    __model__ = TradesPagenation
    current_page = fields.Int(data_key='currentPage')
    count = fields.Int(data_key='count')


class Trade:
    """
    取引データクラスです。
    """
    def __init__(self, price: Decimal, side: SalesSide, size: Decimal, timestamp: datetime) -> None:
        """
        コンストラクタです。

        Args:
            price:
                取引価格を設定します。
            side:
                売買種別を設定します。
            size:
                取引数量を設定します。
            timestamp:
                取引日時を設定します。
        """
        self.price = price
        self.side = side
        self.size = size
        self.timestamp = timestamp.astimezone(timezone('Asia/Tokyo'))


class TradeSchema(BaseSchema):
    """
    取引データスキーマクラスです。
    """
    __model__ = Trade
    price = fields.Decimal(data_key='price')
    side = EnumField(SalesSide, data_key='side')
    size = fields.Decimal(data_key='size')
    timestamp = fields.DateTime(format='%Y-%m-%dT%H:%M:%S.%fZ', data_key='timestamp')



class GetTradesData:
    """
    取引履歴データクラスです。
    """
    def __init__(self, pagination: TradesPagenation, trades: List[Trade]) -> None:
        """
        コンストラクタです。

        Args:
            pagination:
                ページングを設定します。
            trades:
                取引リストを設定します。
        """
        self.pagination = pagination
        self.trades = trades


class GetTradesDataSchema(BaseSchema):
    """
    取引履歴データスキーマクラスです。
    """
    __model__ = GetTradesData
    pagination = fields.Nested(TradesPagenationSchema, data_key='pagination')
    trades = fields.Nested(TradeSchema, data_key='list', many=True)


class GetTradesRes(BaseResponse):
    """
    取引履歴レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: GetOrderBooksData) -> None:
        """
        コンストラクタです。

        Args:
            status:
                ステータスコードを設定します。
            responsetime:
                レスポンスタイムを設定します。
            data:
                レスポンスデータを設定します。
        """
        super().__init__(status, responsetime)
        self.data = data


class GetTradesResSchema(BaseResponseSchema):
    """
    取引履歴レスポンススキーマです。
    """
    __model__ = GetTradesRes
    data = fields.Nested(GetTradesDataSchema, data_key='data')

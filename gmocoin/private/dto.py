#!python3
from marshmallow import fields
from marshmallow_enum import EnumField
from enum import Enum
from datetime import datetime
from pytz import timezone
from typing import List
from decimal import Decimal

from ..common.dto import BaseSchema, BaseResponse, BaseResponseSchema, \
    Symbol, AssetSymbol, SalesSide, OrderType, ExecutionType, SettleType, \
    OrderStatus, TimeInForce


class GetMarginData:
    """
    余力情報データクラスです。
    """
    def __init__(self, actual_profit_loss: Decimal, available_amount: Decimal, margin: Decimal, profit_loss: Decimal) -> None:
        """
        コンストラクタです。

        Args:
            actual_profit_loss:
                時価評価総額
            available_amount:
                取引余力
            margin:
                拘束証拠金
            profit_loss:
                評価損益
        """
        self.actual_profit_loss = actual_profit_loss
        self.available_amount = available_amount
        self.margin = margin
        self.profit_loss = profit_loss


class GetMarginDataSchema(BaseSchema):
    """
   余力情報データスキーマクラスです。
    """
    __model__ = GetMarginData
    actual_profit_loss = fields.Decimal(data_key='actualProfitLoss')
    available_amount = fields.Decimal(data_key='availableAmount')
    margin = fields.Decimal(data_key='margin')
    profit_loss = fields.Decimal(data_key='profitLoss')


class GetMarginRes(BaseResponse):
    """
    余力情報レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: GetMarginData) -> None:
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


class GetMarginResSchema(BaseResponseSchema):
    """
    余力情報レスポンススキーマクラスです。
    """
    __model__ = GetMarginRes
    data = fields.Nested(GetMarginDataSchema, data_key='data')


class GetAssetsData:
    """
    資産残高データクラスです。
    """
    def __init__(self, amount: Decimal, available: Decimal, conversion_rate: Decimal, symbol: AssetSymbol) -> None:
        """
        コンストラクタです。

        Args:
            amount:
                残高
            available:
                利用可能金額（残高 - 出金予定額）
            conversion_rate
                円転レート
            symbol
                銘柄名: JPY BTC ETH BCH LTC XRP
        """
        self.amount = amount
        self.available = available
        self.conversion_rate = conversion_rate
        self.symbol = symbol


class GetAssetsDataSchema(BaseSchema):
    """
   資産残高データスキーマクラスです。
    """
    __model__ = GetAssetsData
    amount = fields.Decimal(data_key='amount')
    available = fields.Decimal(data_key='available')
    conversion_rate = fields.Decimal(data_key='conversionRate')
    symbol = EnumField(AssetSymbol, data_key='symbol')


class GetAssetsRes(BaseResponse):
    """
    資産残高レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: GetAssetsData) -> None:
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


class GetAssetsResSchema(BaseResponseSchema):
    """
    資産残高レスポンススキーマクラスです。
    """
    __model__ = GetAssetsRes
    data = fields.Nested(GetAssetsDataSchema, data_key='data', many=True)


class ActiveOrdersPagenation:
    """
    有効注文一覧ページングデータクラスです。
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


class ActiveOrdersPagenationSchema(BaseSchema):
    """
    有効注文一覧ページングデータスキーマクラスです。
    """
    __model__ = ActiveOrdersPagenation
    current_page = fields.Int(data_key='currentPage')
    count = fields.Int(data_key='count')


class ActiveOrder:
    """
    有効注文一覧クラスです。
    """
    def __init__(self, root_order_id: int, order_id: int, symbol: Symbol, side: SalesSide, order_type: OrderType, 
                 execution_type: ExecutionType, settle_type: SettleType, size: Decimal, executed_size: Decimal,
                 price: Decimal, losscut_price: Decimal, status: OrderStatus, time_in_force: TimeInForce, timestamp: datetime) -> None:
        """
        コンストラクタです。

        Args:
            root_order_id:
                親注文ID
            order_id:
                注文ID
            symbol:
                銘柄名: BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
            side:
                売買区分: BUY SELL
            order_type:
                取引区分: NORMAL LOSSCUT
            execution_type:
                注文タイプ: MARKET LIMIT STOP
            settle_type:
            	決済区分: OPEN CLOSE
            size:
                発注数量
            executed_size:
                約定数量
            price:
                注文価格 (MARKET注文の場合は"0")
            losscut_price:
                ロスカットレート (現物取引や未設定の場合は"0")
            status:
                注文ステータス: WAITING ORDERED MODIFYING CANCELLING CANCELED EXECUTED EXPIRED
                ※逆指値注文の場合はWAITINGが有効
            time_in_force:
                執行数量条件: FAK FAS FOK (Post-onlyの場合はSOK)
            timestamp:
                注文日時
        """
        self.root_order_id = root_order_id
        self.order_id = order_id
        self.symbol = symbol
        self.side = side
        self.order_type = order_type
        self.execution_type = execution_type
        self.settle_type = settle_type
        self.size = size
        self.executed_size = executed_size
        self.price = price
        self.losscut_price = losscut_price
        self.status = status
        self.time_in_force = time_in_force
        self.timestamp = timestamp.astimezone(timezone('Asia/Tokyo'))


class ActiveOrderSchema(BaseSchema):
    """
    有効注文一覧スキーマクラスです。
    """
    __model__ = ActiveOrder
    root_order_id = fields.Int(data_key='rootOrderId')
    order_id = fields.Int(data_key='orderId')
    symbol = EnumField(Symbol, data_key='symbol')
    side = EnumField(SalesSide, data_key='side')
    order_type = EnumField(OrderType, data_key='orderType')
    execution_type = EnumField(ExecutionType, data_key='executionType')
    settle_type = EnumField(SettleType, data_key='settleType')
    size = fields.Decimal(data_key='size')
    executed_size = fields.Decimal(data_key='executedSize')
    price = fields.Decimal(data_key='price')
    losscut_price = fields.Decimal(data_key='losscutPrice')
    status = EnumField(OrderStatus, data_key='status')
    time_in_force = EnumField(TimeInForce, data_key='timeInForce')
    timestamp = fields.DateTime(format='%Y-%m-%dT%H:%M:%S.%fZ', data_key='timestamp')


class GetActiveOrdersData:
    """
    有効注文一覧データクラスです。
    """
    def __init__(self, pagination: ActiveOrdersPagenation=None, active_orders: List[ActiveOrder]=None) -> None:
        """
        コンストラクタです。

        Args:
            pagination:
                ページングを設定します。
            active_orders:
                有効注文一覧リストを設定します。
        """
        self.pagination = pagination
        self.active_orders = active_orders


class GetActiveOrdersDataSchema(BaseSchema):
    """
    有効注文一覧データスキーマクラスです。
    """
    __model__ = GetActiveOrdersData
    pagination = fields.Nested(ActiveOrdersPagenationSchema, data_key='pagination')
    active_orders = fields.Nested(ActiveOrderSchema, data_key='list', many=True)


class GetActiveOrdersRes(BaseResponse):
    """
    有効注文一覧レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: GetActiveOrdersData) -> None:
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


class GetActiveOrdersResSchema(BaseResponseSchema):
    """
    有効注文一覧レスポンススキーマクラスです。
    """
    __model__ = GetActiveOrdersRes
    data = fields.Nested(GetActiveOrdersDataSchema, data_key='data')


class PositionSummary:
    """
    建玉サマリークラスです。
    """
    def __init__(self, average_position_rate: Decimal, position_loss_gain: Decimal, side: SalesSide,
                 sum_order_quantity: Decimal, sum_position_quantity: Decimal, symbol: Symbol) -> None:
        """
        コンストラクタです。

        Args:
            average_position_rate:
                平均建玉レート
            position_loss_gain:
                評価損益
            side:
                売買区分: BUY SELL
            sum_order_quantity:
                発注中数量
            sum_position_quantity:
                建玉数量
            symbol:
                銘柄名: BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
        """
        self.average_position_rate = average_position_rate
        self.position_loss_gain = position_loss_gain
        self.side = side
        self.sum_order_quantity = sum_order_quantity
        self.sum_position_quantity = sum_position_quantity
        self.symbol = symbol


class PositionSummarySchema(BaseSchema):
    """
    建玉サマリースキーマクラスです。
    """
    __model__ = PositionSummary
    average_position_rate = fields.Decimal(data_key='averagePositionRate')
    position_loss_gain = fields.Decimal(data_key='positionLossGain')
    side = EnumField(SalesSide, data_key='side')
    sum_order_quantity = fields.Decimal(data_key='sumOrderQuantity')
    sum_position_quantity = fields.Decimal(data_key='sumPositionQuantity')
    symbol = EnumField(Symbol, data_key='symbol')


class GetPositionSummaryData:
    """
    建玉サマリーデータクラスです。
    """
    def __init__(self, position_summarys: List[PositionSummary]=[]) -> None:
        """
        コンストラクタです。

        Args:
            pagination:
                ページングを設定します。
            positions:
                建玉サマリー一覧リストを設定します。
        """
        self.position_summarys = position_summarys


class GetPositionSummaryDataSchema(BaseSchema):
    """
    建玉サマリーデータスキーマクラスです。
    """
    __model__ = GetPositionSummaryData
    position_summarys = fields.Nested(PositionSummarySchema, data_key='list', many=True, allow_none=True)


class GetPositionSummaryRes(BaseResponse):
    """
    建玉サマリーレスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: str, data: GetPositionSummaryData) -> None:
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


class GetPositionSummaryResSchema(BaseResponseSchema):
    """
    建玉サマリーレスポンススキーマクラスです。
    """
    __model__ = GetPositionSummaryRes
    data = fields.Nested(GetPositionSummaryDataSchema, data_key='data')


class PostOrderRes(BaseResponse):
    """
    新規注文レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: int) -> None:
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


class PostOrderResSchema(BaseResponseSchema):
    """
    新規注文レスポンススキーマクラスです。
    """
    __model__ = PostOrderRes
    data = fields.Int(data_key='data')


class PostCloseOrderRes(BaseResponse):
    """
    決済注文レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: int) -> None:
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


class PostCloseOrderResSchema(BaseResponseSchema):
    """
    決済注文レスポンススキーマクラスです。
    """
    __model__ = PostCloseOrderRes
    data = fields.Int(data_key='data')


class PostCloseBulkOrderRes(BaseResponse):
    """
    一括決済注文レスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: datetime, data: int) -> None:
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


class PostCloseBulkOrderResSchema(BaseResponseSchema):
    """
    一括決済注文レスポンススキーマクラスです。
    """
    __model__ = PostCloseBulkOrderRes
    data = fields.Int(data_key='data')

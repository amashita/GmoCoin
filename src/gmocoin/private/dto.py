#!python3
from marshmallow import fields, pre_load
from marshmallow_enum import EnumField
from enum import Enum
from datetime import datetime
from typing import List
from decimal import Decimal

from ..common.dto import BaseSchema, BaseResponse, BaseResponseSchema, AssetSymbol


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
    def __init__(self, status: int, responsetime: str, data: GetMarginData) -> None:
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
    def __init__(self, status: int, responsetime: str, data: GetAssetsData) -> None:
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

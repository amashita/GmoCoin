#!python3
from marshmallow import fields, pre_load
from marshmallow_enum import EnumField
from enum import Enum
from datetime import datetime
from typing import List
from decimal import Decimal

from ..common.dto import BaseSchema, BaseResponse, BaseResponseSchema


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
    actual_profit_loss = fields.Number(data_key='actualProfitLoss')
    available_amount = fields.Number(data_key='availableAmount')
    margin = fields.Number(data_key='margin')
    profit_loss = fields.Number(data_key='profitLoss')


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

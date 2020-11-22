#!python3
from marshmallow import Schema, fields, post_load
# from datetime import datetime


class BaseSchema(Schema):
    """
    ベーススキーマクラスです。
    """
    __model__ = None

    @post_load
    def to_dto(self, data, **_):
        """
        dto変換関数です。

        Args:
            data
            **_

        """
        return self.__model__(**data)

    class Meta:
        """
        ベーススキーマメタクラスです。
        """
        ordered = True


class BaseResponse:
    """
    ベースレスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: str) -> None:
        """
        コンストラクタです。

        Args:
            status:
                ステータスコードを設定します。
            responsetime :
                レスポンスタイムを設定します。
        """
        self.status = status
        self.responsetime = responsetime


class BaseResponseSchema(BaseSchema):
    """
    ベースレスポンススキーマクラスです。
    """
    __model__ = BaseResponse
    status = fields.Int(data_key='status')
    # responsetime = fields.DateTime(format='%Y-%m-%dT%H:%M:%S.%fZ', data_key='responsetime')
    responsetime = fields.Str(data_key='responsetime')

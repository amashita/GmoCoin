#!python3
import requests
import json
import hmac
import hashlib
import time
from datetime import datetime

from ..common.const import GMOConst
from ..common.exception import GmoCoinException
from ..common.logging import get_logger, log
from .dto import GetMarginResSchema, GetMarginRes


logger = get_logger()


class Client:
    '''
    GMOCoinのプライベートAPIクライアントクラスです。
    '''

    @log(logger)
    def __init__(self, api_key: str, secret_key: str):
        """
        コンストラクタです。

        Args:
            api_key:
               APIキーを設定します。

            secret_key:
                APIシークレットを設定します。
        """
        self._api_key = api_key
        self._secret_key = secret_key

    @log(logger)
    def get_margin(self) -> GetMarginRes:
        """
        余力情報を取得します。

        Args:
            なし

        Returns:
            GetMarginRes
        """

        path = '/v1/account/margin'

        headers = self._create_header(method='GET', path=path)

        response = requests.get(GMOConst.END_POINT_PRIVATE + path, headers=headers)
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetMarginResSchema().load(response.json())

    @log(logger)
    def _create_header(self, method :str, path :str) -> dict:
        """
        ヘッダーを生成します。

        Args:
            method:
                HTTPメソッドを指定します。
            path:
                url(private以下)を指定します。

        Returns:
            header
        """
        timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))

        # text = timestamp + method + path
        # sign = hmac.new(bytes('OPxTXz9Goy2chqhTZ6mGK++Ml7tYF3alRrOUHt5NxChZpuJPTjorQQq5d4SbETP1'.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
        # headers = {
        #     "API-KEY": 'PpYQR24/rhlRAE7/SdDS5+0gs9TMpEzg',
        #     "API-TIMESTAMP": timestamp,
        #     "API-SIGN": sign
        # }

        text = timestamp + method + path
        sign = hmac.new(bytes(self._secret_key.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
        headers = {
            "API-KEY": self._api_key,
            "API-TIMESTAMP": timestamp,
            "API-SIGN": sign
        }

        return headers

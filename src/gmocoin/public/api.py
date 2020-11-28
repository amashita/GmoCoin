#!python3
import requests
import json

from ..common.const import GMOConst
from ..common.exception import GmoCoinException
from ..common.logging import get_logger, log
from .dto import GetStatusResSchema, GetStatusRes, \
    GetTickerResSchema, GetTickerRes, Symbol , \
    GetOrderBooksResSchema, GetOrderBooksRes ,\
    GetTradesResSchema, GetTradesRes


logger = get_logger()


class Client:
    '''
    GMOCoinのパブリックAPIクライアントクラスです。
    '''

    @log(logger)
    def get_status(self) -> GetStatusRes:
        """
        取引所の稼動状態を取得します。

        Args:
            なし

        Returns:
            GetStatusRes
        """
        response = requests.get(GMOConst.END_POINT_PUBLIC + 'status')
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetStatusResSchema().load(response.json())
        
    @log(logger)
    def get_ticker(self, symbol:Symbol = None) -> GetTickerRes:
        """
        指定した銘柄の最新レートを取得します。
        全銘柄分の最新レートを取得する場合はsymbolパラメータ指定無しでの実行をおすすめします。

        Args:
            symbol:
                指定しない場合は全銘柄分の最新レートを返す。
                BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY

        Returns:
            GetTickerRes
        """
        if symbol is None:
            response = requests.get(GMOConst.END_POINT_PUBLIC + f'ticker')
        else:
            response = requests.get(GMOConst.END_POINT_PUBLIC + f'ticker?symbol={symbol.value}')
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetTickerResSchema().load(response.json())

    @log(logger)
    def get_orderbooks(self, symbol:Symbol) -> GetOrderBooksRes:
        """
        指定した銘柄の板情報(snapshot)を取得します。

        Args:
            symbol:
                BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY

        Returns:
            GetOrderBooksRes
        """
        response = requests.get(GMOConst.END_POINT_PUBLIC + f'orderbooks?symbol={symbol.value}')
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetOrderBooksResSchema().load(response.json())
    
    @log(logger)
    def get_trades(self, symbol:Symbol, page:int=1, count:int=100) -> GetTradesRes:
        """
        指定した銘柄の板情報(snapshot)を取得します。

        Args:
            symbol:
                BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
            page:
                取得対象ページ
                指定しない場合は1を指定したとして動作する。
            count:
                1ページ当りの取得件数
                指定しない場合は100(最大値)を指定したとして動作する。

        Returns:
            GetTradesRes
        """
        response = requests.get(GMOConst.END_POINT_PUBLIC + f'trades?symbol={symbol.value}&page={page}&count={count}')
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetTradesResSchema().load(response.json())

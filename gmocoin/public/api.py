#!python3
import requests
import json

from ..common.annotation import post_request
from ..common.const import GMOConst
from ..common.logging import get_logger, log
from .dto import GetStatusResSchema, GetStatusRes, \
    GetTickerResSchema, GetTickerRes, Symbol , \
    GetOrderBooksResSchema, GetOrderBooksRes, \
    GetTradesResSchema, GetTradesRes


logger = get_logger()


class Client:
    '''
    GMOCoinのパブリックAPIクライアントクラスです。
    '''
    
    @log(logger)
    @post_request(GetStatusResSchema)
    def get_status(self) -> GetStatusRes:
        """
        取引所の稼動状態を取得します。

        Args:
            なし

        Returns:
            GetStatusRes
        """
        return requests.get(GMOConst.END_POINT_PUBLIC + 'status')
        
    @log(logger)
    @post_request(GetTickerResSchema)
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
            return requests.get(GMOConst.END_POINT_PUBLIC + f'ticker')
        else:
            return requests.get(GMOConst.END_POINT_PUBLIC + f'ticker?symbol={symbol.value}')

    @log(logger)
    @post_request(GetOrderBooksResSchema)
    def get_orderbooks(self, symbol:Symbol) -> GetOrderBooksRes:
        """
        指定した銘柄の板情報(snapshot)を取得します。

        Args:
            symbol:
                BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY

        Returns:
            GetOrderBooksRes
        """
        return requests.get(GMOConst.END_POINT_PUBLIC + f'orderbooks?symbol={symbol.value}')
    
    @log(logger)
    @post_request(GetTradesResSchema)
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
        return requests.get(GMOConst.END_POINT_PUBLIC + f'trades?symbol={symbol.value}&page={page}&count={count}')

#!python3
import requests
import json

from ..common.const import GMOConst
from ..common.exception import GmoCoinException
from .dto import GetStatusResSchema, GetStatusRes, \
    GetTickerResSchema, GetTickerRes, Symbol , \
    GetOrderBooksResSchema, GetOrderBooksRes ,\
    GetTradesResSchema, GetTradesRes


class Client:
    '''
    GMOCoinの公開APIクライアントクラスです。
    A public API client class for GMOCoin.
    '''
    def get_status(self) -> GetStatusRes:
        response = requests.get(GMOConst.END_POINT_PUBLIC + 'status')
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetStatusResSchema().load(response.json())
        

    def get_ticker(self, symbol:Symbol = None) -> GetTickerRes:
        if symbol is None:
            response = requests.get(GMOConst.END_POINT_PUBLIC + f'ticker')
        else:
            response = requests.get(GMOConst.END_POINT_PUBLIC + f'ticker?symbol={symbol.value}')
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetTickerResSchema().load(response.json())

    def get_orderbooks(self, symbol:Symbol) -> GetOrderBooksRes:
        response = requests.get(GMOConst.END_POINT_PUBLIC + f'orderbooks?symbol={symbol.value}')
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetOrderBooksResSchema().load(response.json())
    
    def get_trades(self, symbol:Symbol, page:int=1, count:int=100) -> GetTradesRes:
        response = requests.get(GMOConst.END_POINT_PUBLIC + f'trades?symbol={symbol.value}&page={page}&count={count}')
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetTradesResSchema().load(response.json())

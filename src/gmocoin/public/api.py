#!python3
import requests
import json

from ..common.const import GMOConst
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
        return GetStatusResSchema().load(response.json())
        

    def get_ticker(self, symbol:Symbol = None) -> GetTickerRes:
        if symbol is None:
            response = requests.get(GMOConst.END_POINT_PUBLIC + f'ticker')
        else:
            response = requests.get(GMOConst.END_POINT_PUBLIC + f'ticker?symbol={symbol.value}')
        return GetTickerResSchema().load(response.json())

    def get_orderbooks(self, symbol:Symbol) -> GetOrderBooksRes:
        response = requests.get(GMOConst.END_POINT_PUBLIC + f'orderbooks?symbol={symbol.value}')
        return GetOrderBooksResSchema().load(response.json())
    
    def get_trades(self, symbol:Symbol, page:int=1, count:int=100) -> GetTradesRes:
        response = requests.get(GMOConst.END_POINT_PUBLIC + f'trades?symbol={symbol.value}&page={page}&count={count}')
        return GetTradesResSchema().load(response.json())

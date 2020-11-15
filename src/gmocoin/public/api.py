#!python3
import requests
import json

from ..common.const import GMOConst


class Client:
    '''
    GMOCoinの公開APIクライアントクラスです。
    A public API client class for GMOCoin.
    '''
    def get_status(self):
        response = requests.get(GMOConst.END_POINT_PUBLIC + 'status')
        return response.json()

    def get_ticker(self):
        pass
    
    def get_orderbooks(self):
        pass
    
    def get_trades(self):
        pass
    
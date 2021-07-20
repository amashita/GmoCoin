#!python3
import requests
import json
from datetime import datetime, date, timedelta
import pandas as pd

from ..common.annotation import post_request
from ..common.const import GMOConst
from ..common.logging import get_logger, log
from ..common.dto import Status
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
        ret = requests.get(GMOConst.END_POINT_PUBLIC + 'status')

        res_json = ret.json()
        if res_json['status'] == 5 and res_json['messages'][0]['message_code'] == 'ERR-5201':
            # メンテナンス中の場合、メンテナンスレスポンスを返却
            # {'status': 5, 'messages': [{'message_code': 'ERR-5201', 'message_string': 'MAINTENANCE. Please wait for a while'}]}
            return GetStatusRes(status=0, responsetime=datetime.now(), 
                                data=GetStatusData(status=Status.MAINTENANCE))

        return ret
        
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

    @log(logger)
    def get_historical_data(self, symbol:Symbol, page:int=1, count:int=100) -> GetTradesRes:
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

    @log(logger)
    def get_historical_data(self, symbol:Symbol, past_days: int, base_date:date = None) -> pd.DataFrame:
        """
        指定した銘柄の過去取引情報を取得します。

        Args:
            symbol:
                BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
            past_days:
                過去期間日
                base_date-past_days　～　base_dateのデータを取得する。
            base_date:
                過去基準日
                指定しない場合は現在日を指定したとして動作する。

        Returns:
            DataFrame
        """
        if base_date == None:
            base_date = date.today()

        start_date = base_date - timedelta(days=past_days)

        #差分を使って、スタートの日から現在まで一日ずつ足していく
        url_list = []
        for d in range(past_days):
            day=start_date + timedelta(days=d)
            # print(day)
            url = f'https://api.coin.z.com/data/trades/{symbol.value}/{day.year}/{day.month:02}/{day.year}{day.month:02}{day.day:02}_{symbol.value}.csv.gz'
            # MEMO: 土日は更新されないようなので、存在する日付だけlistに追加する
            if requests.get(url).status_code == 200:
                url_list.append(url)

        return pd.concat([pd.read_csv(url) for url in url_list], axis=0, sort=True)

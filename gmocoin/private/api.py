#!python3
import requests
import json
import hmac
import hashlib
import time
from datetime import datetime

from ..common.annotation import post_request
from ..common.const import GMOConst
from ..common.logging import get_logger, log
from ..common.dto import Symbol, SalesSide, ExecutionType, TimeInForce, BaseResponseSchema , BaseResponse
from .dto import GetMarginResSchema, GetMarginRes, GetAssetsResSchema, GetAssetsRes,\
    GetActiveOrdersResSchema, GetActiveOrdersRes, GetPositionSummaryResSchema, GetPositionSummaryRes,\
    PostOrderResSchema, PostOrderRes, PostCloseOrderResSchema, PostCloseOrderRes,\
    PostCloseBulkOrderResSchema, PostCloseBulkOrderRes


logger = get_logger()


class Client:
    '''
    GMOCoinのプライベートAPIクライアントクラスです。
    '''

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
    @post_request(GetMarginResSchema)
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

        return requests.get(GMOConst.END_POINT_PRIVATE + path, headers=headers)

    @log(logger)
    @post_request(GetAssetsResSchema)
    def get_assets(self) -> GetAssetsRes:
        """
        資産残高を取得します。

        Args:
            なし

        Returns:
            GetAssetsRes
        """

        path = '/v1/account/assets'

        headers = self._create_header(method='GET', path=path)

        return requests.get(GMOConst.END_POINT_PRIVATE + path, headers=headers)

    @log(logger)
    @post_request(GetActiveOrdersResSchema)
    def get_active_orders(self, symbol:Symbol, page:int=1, count:int=100) -> GetActiveOrdersRes:
        """
        有効注文一覧を取得します。
        対象: 現物取引、レバレッジ取引。

        Args:
            symbol:
                BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
            page:
                取得対象ページ: 指定しない場合は1を指定したとして動作する。
            count:
                1ページ当りの取得件数: 指定しない場合は100(最大値)を指定したとして動作する。

        Returns:
            GetActiveOrdersRes
        """

        path = '/v1/activeOrders'

        headers = self._create_header(method='GET', path=path)
        parameters = {
            "symbol": symbol.value,
            "page": page,
            "count": count
        }

        return requests.get(GMOConst.END_POINT_PRIVATE + path, headers=headers, params=parameters)

    @log(logger)
    @post_request(GetPositionSummaryResSchema)
    def get_position_summary(self, symbol:Symbol) -> GetPositionSummaryRes:
        """
        建玉サマリーを取得します。
        対象: レバレッジ取引

        銘柄ごと、売買区分(買/売)ごとの建玉サマリー取得ができます。

        Args:
            symbol:
                BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY

        Returns:
            GetPositionSummaryRes
        """

        path = '/v1/positionSummary'

        headers = self._create_header(method='GET', path=path)
        parameters = {
            "symbol": symbol.value
        }

        return requests.get(GMOConst.END_POINT_PRIVATE + path, headers=headers, params=parameters)

    @log(logger)
    @post_request(PostOrderResSchema)
    def order(self, symbol:Symbol, side:SalesSide, execution_type:ExecutionType, time_in_force: TimeInForce,
              size:str, price:str='0', losscut_price:str='0') -> PostOrderRes:
        """
        新規注文をします。
        対象: 現物取引、レバレッジ取引

        現物取引: 買/売注文
        レバレッジ取引: 新規の買/売注文

        Args:
            symbol:
                BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
            side:
                BUY SELL
            execution_type:
                MARKET LIMIT STOP
            time_in_force:
                Optional	FAK ( MARKET STOPの場合のみ設定可能 )
                FAS FOK ((Post-onlyの場合はSOK) LIMITの場合のみ設定可能 )
                *指定がない場合は成行と逆指値はFAK、指値はFASで注文されます。
                SOKは現物取引（全銘柄）とレバレッジ取引(BTC_JPY)の場合のみ指定可能です。
            price:
                *executionTypeによる
                LIMIT STOP の場合は必須、 MARKET の場合は不要。
            losscut_price:
            	レバレッジ取引で、executionTypeが LIMIT または STOP の場合のみ設定可能。
            size:
                数量

        Returns:
            PostOrderRes
        """

        path = '/v1/order'

        req_body = {
            "symbol": symbol.value,
            "side": side.value,
            "executionType": execution_type.value,
            "timeInForce": time_in_force.value,
            "size": size
        }
        if execution_type != ExecutionType.MARKET:
            req_body["price"] = price
        if losscut_price != '0' and execution_type != ExecutionType.MARKET and self._is_leverage(symbol):
            req_body["losscutPrice"] = losscut_price

        headers = self._create_header(method='POST', path=path, req_body=req_body)

        return requests.post(GMOConst.END_POINT_PRIVATE + path, headers=headers, data=json.dumps(req_body))

    @log(logger)
    @post_request(BaseResponseSchema)
    def change_order(self, order_id:int, price: str, losscut_price: str='') -> BaseResponse:
        """
        注文変更をします。
        対象: 現物取引、レバレッジ取引

        Args:
            order_id:
                Required
            price:
                Required
            losscut_price
                Optional	

        Returns:
            BaseResponse
        """

        path = '/v1/changeOrder'
        req_body = {
            "orderId": order_id,
            "price": price
        }
        if len(losscut_price) > 0:
            req_body["losscutPrice"] = losscut_price

        headers = self._create_header(method='POST', path=path, req_body=req_body)

        return requests.post(GMOConst.END_POINT_PRIVATE + path, headers=headers, data=json.dumps(req_body))

    @log(logger)
    @post_request(BaseResponseSchema)
    def cancel_order(self, order_id:int) -> BaseResponse:
        """
        注文取消をします。
        対象: 現物取引、レバレッジ取引

        Args:
            order_id:

        Returns:
            BaseResponse
        """

        path = '/v1/cancelOrder'
        req_body = {
            "orderId": order_id
        }

        headers = self._create_header(method='POST', path=path, req_body=req_body)

        return requests.post(GMOConst.END_POINT_PRIVATE + path, headers=headers, data=json.dumps(req_body))


    @log(logger)
    @post_request(PostCloseOrderResSchema)
    def close_order(self, symbol:Symbol, side:SalesSide, execution_type:ExecutionType, time_in_force: TimeInForce,
                    position_id:int, position_size: str, price:str='0') -> PostCloseOrderRes:
        """
        決済注文をします。
        対象: レバレッジ取引

        Args:
            symbol:
                Required
                BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
            side:
                Required
                BUY SELL
            execution_type:
                Required
                MARKET LIMIT STOP
            time_in_force:
                Optional
                FAK ( MARKET STOPの場合のみ設定可能 )
                FAS FOK ((Post-onlyの場合はSOK) LIMITの場合のみ設定可能 )
                *指定がない場合は成行と逆指値はFAK、指値はFASで注文されます。
                SOKはBTC_JPYの場合のみ指定可能です。
            price:
                *executionTypeによる
                LIMIT STOP の場合は必須、 MARKET の場合は不要。
            position_id:
                Required
                建玉は1つのみ指定可能。
            position_size:
                Required
                建玉は1つのみ指定可能。

        Returns:
            PostCloseOrderRes
        """

        path = '/v1/closeOrder'

        req_body = {
            "symbol": symbol.value,
            "side": side.value,
            "executionType": execution_type.value,
            "timeInForce": time_in_force.value,
            "settlePosition": [
                {
                    "positionId": position_size,
                    "size": position_size
                }
            ]
        }
        if execution_type != ExecutionType.MARKET:
            req_body["price"] = price

        headers = self._create_header(method='POST', path=path, req_body=req_body)

        return requests.post(GMOConst.END_POINT_PRIVATE + path, headers=headers, data=json.dumps(req_body))

    @log(logger)
    @post_request(PostCloseBulkOrderResSchema)
    def close_bulk_order(self, symbol:Symbol, side:SalesSide, execution_type:ExecutionType, time_in_force: TimeInForce,
                         size: str, price:str='0') -> PostCloseBulkOrderRes:
        """
        一括決済注文をします。
        対象: レバレッジ取引

        Args:
            symbol:
                Required
                BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
            side:
                Required
                BUY SELL
            execution_type:
                Required
                MARKET LIMIT STOP
            time_in_force:
                Optional
                FAK ( MARKET STOPの場合のみ設定可能 )
                FAS FOK ((Post-onlyの場合はSOK) LIMITの場合のみ設定可能 )
                *指定がない場合は成行と逆指値はFAK、指値はFASで注文されます。
                SOKはBTC_JPYの場合のみ指定可能です。
            price:
                *executionTypeによる
                LIMIT STOP の場合は必須、 MARKET の場合は不要。
            size:
                Required

        Returns:
            PostCloseBulkOrderRes
        """

        path = '/v1/closeBulkOrder'

        req_body = {
            "symbol": symbol.value,
            "side": side.value,
            "executionType": execution_type.value,
            "timeInForce": time_in_force.value,
            "size": size
        }
        if execution_type != ExecutionType.MARKET:
            req_body["price"] = price

        headers = self._create_header(method='POST', path=path, req_body=req_body)

        return requests.post(GMOConst.END_POINT_PRIVATE + path, headers=headers, data=json.dumps(req_body))

    def _create_header(self, method :str, path :str, req_body:[] = None) -> dict:
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

        if req_body is None:
            text = timestamp + method + path
        else:
            text = timestamp + method + path + json.dumps(req_body)

        sign = hmac.new(bytes(self._secret_key.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
        headers = {
            "API-KEY": self._api_key,
            "API-TIMESTAMP": timestamp,
            "API-SIGN": sign
        }

        return headers

    def _is_leverage(self, symbol: Symbol) -> bool:
        """
        取引種別がレバレッジ取引かどうかを返却します。

        Args:
            symbol:
                取引種別。

        Returns:
            bool
        """

        return (symbol == Symbol.BTC_JPY or 
                symbol == Symbol.ETH_JPY or 
                symbol == Symbol.BCH_JPY or 
                symbol == Symbol.LTC_JPY or 
                symbol == Symbol.XRP_JPY)

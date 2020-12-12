#!python3
from functools import wraps
from time import sleep

from .exception import GmoCoinException
from .dto import ErrorResponseResSchema


def post_request(Schema, interval: float=0.1, retry_count: int=10):
    """
    リクエスト後の処理を実施するラッパー関数。
        ステータス200のチェック
        1秒間のリクエスト上限を超えた場合のリトライをする
    Args:
        interval:
            リトライ間隔秒数
        retry_count:
            リトライ回数
    Returns:
        _decoratorの返り値
    """

    def _decorator(func):
        """
        デコレーターを使用する関数を引数とする
        Args:
            func (function)
        Returns:
            wrapperの返り値
        """

        # funcのメタデータを引き継ぐ
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            実際の処理を書くための関数
            Args:
                *args:
                    funcの引数
                 **kwargs:
                    funcの引数
            Returns:
                funcの返り値
            """

            for i in range(retry_count):
                # funcの実行
                ret = func(*args, **kwargs)
                if ret.status_code != 200:
                    raise GmoCoinException(ret.status_code)

                res_json = ret.json()

                if 'messages' in res_json:
                    sleep(interval)
                else:
                    return Schema().load(res_json)

            if 'messages' in res_json:
                raise GmoCoinException(ret.status_code, 
                                       messageg=ErrorResponseResSchema().load(res_json))

        return wrapper
    return _decorator
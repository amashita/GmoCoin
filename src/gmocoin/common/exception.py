#!python3
from .dto import ErrorResponse


class GmoCoinException(Exception):
    """
    例外クラスです。
    """

    def __init__(self, status_code: int, messageg: ErrorResponse=None):
        """
        コンストラクタです。

        Args:
            status_code:
                httpステータスコードを設定します。
            messageg :
                メッセージを設定します。

        """
        self.status_code = status_code
        self.messageg = messageg

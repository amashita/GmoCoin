#!python3


class GmoCoinException(Exception):
    """
    例外クラスです。
    """

    def __init__(self, status_code: int, messageg: str=''):
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

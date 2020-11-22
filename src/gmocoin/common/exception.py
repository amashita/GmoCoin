#!python3


class GmoCoinException(Exception):

    def __init__(self, status_code: int, messageg: str=''):
        self.status_code = status_code
        self.messageg = messageg

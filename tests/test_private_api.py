#!python3
from pprint import pprint
from enum import Enum
import time
import json

from src.gmocoin.private.api import Client
from src.gmocoin.public.dto import Status, Symbol, SalesSide
from .const import TestConst


class Test:

    @classmethod
    def setup_class(cls):
        with open(str('./tests/api_conf.json'), encoding='utf-8') as f:
            cls._api_conf = json.load(f)

    def test_get_margin(self):
        time.sleep(TestConst.API_CALL_INTERVAL)
        client = Client(api_key=self._api_conf['API_KEY'], secret_key=self._api_conf['SECRET_KEY'])
        res = client.get_margin()

        assert type(res.status) is int
        assert type(res.responsetime) is str
        assert type(res.data.actual_profit_loss) is float
        assert type(res.data.available_amount) is float
        assert type(res.data.margin) is float
        assert type(res.data.profit_loss) is float

        print(res.status)
        print(res.responsetime)
        print(res.data.actual_profit_loss)
        print(res.data.available_amount)
        print(res.data.margin)
        print(res.data.profit_loss)

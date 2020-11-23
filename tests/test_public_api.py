#!python3
from pprint import pprint
from enum import Enum
import time

from src.gmocoin.public.api import Client
from src.gmocoin.public.dto import Status, Symbol, SalesSide
from .const import TestConst


def test_get_status(capfd):
    time.sleep(TestConst.API_CALL_INTERVAL)
    client = Client()
    res = client.get_status()

    assert type(res.status) is int
    assert type(res.responsetime) is str
    assert type(res.data.status) is Status

    print(res.status)
    print(res.responsetime)
    print(res.data.status)


def test_get_ticker(capfd):
    time.sleep(TestConst.API_CALL_INTERVAL)
    client = Client()
    res = client.get_ticker(Symbol.BTC_JPY)

    assert type(res.status) is int
    assert type(res.responsetime) is str
    for d in res.data:
        assert type(d.ask) is float
        assert type(d.bid) is float
        assert type(d.high) is float
        assert type(d.last) is float
        assert type(d.low) is float
        assert type(d.symbol) is Symbol
        assert type(d.timestamp) is str
        assert type(d.volume) is float
        
        print(d.ask)
        print(d.bid)
        print(d.high)
        print(d.last)
        print(d.low)
        print(d.symbol)
        print(d.timestamp)
        print(d.volume)

    time.sleep(TestConst.API_CALL_INTERVAL)
    res = client.get_ticker()
    symbol_list = [s for s in Symbol]
    assert len(res.data) == len(symbol_list)
    for d in res.data:
        assert d.symbol in symbol_list


def test_get_orderbooks(capfd):

    time.sleep(TestConst.API_CALL_INTERVAL)
    client = Client()
    res = client.get_orderbooks(Symbol.BTC_JPY)

    assert type(res.status) is int
    assert type(res.responsetime) is str
    for ask in res.data.asks:
        assert type(ask.price) is float
        assert type(ask.size) is float

    for bid in res.data.bids:
        assert type(bid.price) is float
        assert type(bid.size) is float

    assert type(res.data.symbol) is Symbol
    assert res.data.symbol == Symbol.BTC_JPY


def test_get_trades(capfd):

    time.sleep(TestConst.API_CALL_INTERVAL)
    client = Client()
    res = client.get_trades(Symbol.BTC_JPY)

    assert type(res.status) is int
    assert type(res.responsetime) is str
    assert type(res.data.pagination.current_page) is int
    assert type(res.data.pagination.count) is int

    for trade in res.data.trades:
        assert type(trade.price) is float
        assert type(trade.side) is SalesSide
        assert type(trade.size) is float
        assert type(trade.timestamp) is str

    time.sleep(TestConst.API_CALL_INTERVAL)
    res = client.get_trades(Symbol.BTC_JPY, page=2, count=50)
    assert len(res.data.trades) == 50

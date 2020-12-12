#!python3
from pprint import pprint
from enum import Enum
import time
from decimal import Decimal
from datetime import datetime

from gmocoin.public.api import Client
from gmocoin.common.dto import Status, Symbol, SalesSide
from .const import TestConst


def test_get_status(capfd):
    time.sleep(TestConst.API_CALL_INTERVAL)
    client = Client()
    res = client.get_status()

    assert type(res.status) is int
    assert type(res.responsetime) is datetime
    assert type(res.data.status) is Status

    print(res.status)
    print(res.responsetime)
    print(res.data.status)


def test_get_ticker(capfd):
    time.sleep(TestConst.API_CALL_INTERVAL)
    client = Client()
    res = client.get_ticker(Symbol.BTC_JPY)

    assert type(res.status) is int
    assert type(res.responsetime) is datetime
    for d in res.data:
        assert type(d.ask) is Decimal
        assert type(d.bid) is Decimal
        assert type(d.high) is Decimal
        assert type(d.last) is Decimal
        assert type(d.low) is Decimal
        assert type(d.symbol) is Symbol
        assert type(d.timestamp) is datetime
        assert type(d.volume) is Decimal
        
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
    assert type(res.responsetime) is datetime
    for ask in res.data.asks:
        assert type(ask.price) is Decimal
        assert type(ask.size) is Decimal

    for bid in res.data.bids:
        assert type(bid.price) is Decimal
        assert type(bid.size) is Decimal

    assert type(res.data.symbol) is Symbol
    assert res.data.symbol == Symbol.BTC_JPY


def test_get_trades(capfd):

    time.sleep(TestConst.API_CALL_INTERVAL)
    client = Client()
    res = client.get_trades(Symbol.BTC_JPY)

    assert type(res.status) is int
    assert type(res.responsetime) is datetime
    assert type(res.data.pagination.current_page) is int
    assert type(res.data.pagination.count) is int

    for trade in res.data.trades:
        assert type(trade.price) is Decimal
        assert type(trade.side) is SalesSide
        assert type(trade.size) is Decimal
        assert type(trade.timestamp) is datetime

    time.sleep(TestConst.API_CALL_INTERVAL)
    res = client.get_trades(Symbol.BTC_JPY, page=2, count=50)
    assert len(res.data.trades) == 50


def test_get_trades_loop(capfd):
    client = Client()
    for i in range(10):
        res = client.get_trades(Symbol.BTC_JPY)
        print(res.status)


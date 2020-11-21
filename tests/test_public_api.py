#!python3
from pprint import pprint
from enum import Enum

from src.gmocoin.public.api import Client
from src.gmocoin.public.dto import Status

def test_get_status(capfd):
    client = Client()
    get_status_res = client.get_status()

    assert type(get_status_res.status) is int
    assert type(get_status_res.responsetime) is str
    assert type(get_status_res.data.status) is Status

    print(get_status_res.status)
    print(get_status_res.responsetime)
    print(get_status_res.data.status)

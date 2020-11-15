#!python3
from pprint import pprint

from src.gmocoin.public.api import Client

def test_get_status(capfd):
    client = Client()
    json = client.get_status()
    pprint(json)

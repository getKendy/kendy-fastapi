#!/usr/bin/env python
import redis
import time
import logging
import json
import os
from binance.lib.utils import config_logging
from binance.spot import Spot as SpotClient
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebSocketClient
from project.celery_tasks import tasks

r = redis.Redis(host=os.environ.get('REDIS_CACHE'),
                port=os.environ.get('REDIS_PORT'),
                db=os.environ.get('REDIS_DB'))

config_logging(logging, logging.DEBUG)

spot_client = SpotClient()
# logging.info(spot_client.exchange_info())

excahnge_info = spot_client.exchange_info()
# print(type(excahnge_info))
# timezone
# serverTime
# rateLimits
# exchangeFilters
# symbols
allSymbols = []
for x in excahnge_info['symbols']:
    # print(x)
    # print(type(x))
    allSymbols.append(x["symbol"])
    # r.set(("market" + x["symbol"]), str(json.dumps(x)), 86400)


def pop_all(l):
    '''remove all items from list'''
    r, l[:] = l[:], []
    return r

collected_tickers = []
def message_handler(message):
    '''process incoming ticker message'''
    # Collect multiple messages and send to task
    if len(collected_tickers) < 100:
        collected_tickers.append(message)
        print(len(collected_tickers))
    else:
        tasks.pre_process_tickers.delay(collected_tickers)
        print(len(collected_tickers))
        pop_all(l=collected_tickers)
        print(len(collected_tickers))
        collected_tickers.append(message)
    

if len(allSymbols) > 4000:
    print("!!! We need more WebSockets to Binanace !!!",str(len(allSymbols) / 1000))
else:
    print("We have enough sockets", str(len(allSymbols) / 1000))
# 5 persecond 1024 streams max
time.sleep(1)
try:
    ws_client1 = WebSocketClient()
    ws_client1.start()
    print('client1 started')
    time.sleep(1)
    ws_client2 = WebSocketClient()
    ws_client2.start()
    print('client2 started')
    time.sleep(1)
    ws_client3 = WebSocketClient()
    ws_client3.start()
    print('client3 started')
    time.sleep(1)
    ws_client4 = WebSocketClient()
    ws_client4.start()
    print('client4 started')
    time.sleep(1)

    # start kline sockets
    for x in range(len(allSymbols)):
        if x < 1000:
            ws_client1.kline(allSymbols[x], id=1,
                            interval='1m', callback=message_handler)
            time.sleep(0.25)
        elif x > 1000 and x < 2000:
            ws_client2.kline(allSymbols[x], id=2,
                            interval='1m', callback=message_handler)
            time.sleep(0.25)
        elif x > 2000 and x < 3000:
            ws_client3.kline(allSymbols[x], id=3,
                            interval='1m', callback=message_handler)
            time.sleep(0.25)
        else:
            ws_client4.kline(allSymbols[x], id=4,
                            interval='1m', callback=message_handler)
            time.sleep(0.25)


    time.sleep(120)

    logging.debug("closing ws connection")
    ws_client1.stop()
    time.sleep(1)
    ws_client2.stop()
    time.sleep(1)
    ws_client3.stop()
    time.sleep(1)
    ws_client4.stop()
except KeyboardInterrupt:
    logging.debug("closing ws connection")
    ws_client1.stop()
    time.sleep(1)
    ws_client2.stop()
    time.sleep(1)
    ws_client3.stop()
    time.sleep(1)
    ws_client4.stop()

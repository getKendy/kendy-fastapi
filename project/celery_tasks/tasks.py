from celery import shared_task
from time import time
import os
import time
import redis
import ccxt
import json
import datetime
import requests
from binance import ThreadedWebsocketManager
# from sqlalchemy import false
import pandas as pd
import pandas_ta as ta

from fastapi_pagination import paginate
from fastapi import Request

# from ..ticker24h import main as ticker_main
# from .. import models

r = redis.Redis(host=os.environ.get('REDIS_CACHE'),
                port=os.environ.get('REDIS_PORT'),
                db=os.environ.get('REDIS_DB'))
# MONGO_URL = "mongodb://ron:Oldsch00l@mongo/middleware"

exchange_class = getattr(ccxt, "binance")
binance = exchange_class(
    {
        "apiKey": "",
        "secret": "",
        "timeout": 2400000,
        "enableRateLimit": True,
    }
)


# @shared_task
# def create_task(task_type):
#     time.sleep(int(task_type) * 2)
#     return True


@shared_task
def start_24h_ticker():
    '''start 24h ticker'''
    data = r.get("TickerRunning")
    if not data:
        print('starting ticker')
        twm = ThreadedWebsocketManager(api_key='', api_secret='')
        # start is required to initialise its internal loop
        twm.start()

        def handle_ticker_message(msg):
            save_ticker_message.delay(tickers=msg)

        # def handel_klines_message(msg):
        #     print(msg)

        twm.start_miniticker_socket(
            callback=handle_ticker_message, update_time=1000)
        # twm.start_kline_socket(symbol='BNBBTC' ,interval='1m', callback=handelKlinesMessage)
        twm.join()
        return
    else:
        print('data exists')


@shared_task
def update_markets():
    '''update binance markets'''
    markets = binance.fetch_markets()
    for market in markets:
        # print(json.dumps(market))
        r.set(("market" + market["id"]), str(json.dumps(market)), 86400)


@shared_task
def save_ticker_message(tickers):
    '''save tickers'''
    all_tickers = []
    for ticker in tickers:
        if ticker["e"] == "error":
            import logging

            logging.info(ticker)
        else:
            try:
                symbol = dict(json.loads(r.get("market" + ticker["s"])))
            except :
                symbol = {"symbol": "noData"}
            print(ticker)
            # key = str(ticker["s"]).encode("UTF-8")
            # # print(key)
            # r.set(
            #     key,
            #     str(
            #         json.dumps(
            #             {
            #                 "symbol": ticker["s"],
            #                 "market": symbol["symbol"],
            #                 "c": ticker["c"],
            #                 "o": ticker["o"],
            #                 "h": ticker["h"],
            #                 "l": ticker["l"],
            #                 "v": ticker["v"],
            #                 "q": ticker["q"],
            #             }
            #         )
            #     ),
            #     60,
            # )
            all_tickers.append(
                {
                    "date": ticker["E"],
                    "symbol": ticker["s"],
                    "market": symbol["symbol"],
                    "c": ticker["c"],
                    "o": ticker["o"],
                    "h": ticker["h"],
                    "l": ticker["l"],
                    "v": ticker["v"],
                    "q": ticker["q"],
                }
            )
    # enf for loop
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    tickers = all_tickers
    if len(all_tickers) >= 1:
        requests.post(
            os.environ.get('API') + "v2/tickers/", json=tickers, headers=headers)

            # print('saved')
    # r.set("allTickers", str(json.dumps({"tickers": allTickers})), 86400)
    # r.set("TickerRunning", "1", 120)


# @shared_task
# def saveUserMessage(msg):
#     print(msg)


# @shared_task
# def createAllTickers():
#     tickers = []
#     keys = r.keys("market*")
#     dateNow = datetime.datetime.now()
#     # print(keys)
#     for key in keys:
#         # print(key)
#         try:
#             ticker = dict(
#                 json.loads(
#                     r.get(str(key.decode("UTF-8")).replace("market", "")))
#             )
#             # print(ticker)
#             # print(type(ticker))
#             tickers.append(
#                 {
#                     # dateNow,
#                     'symbol':  ticker["symbol"],
#                     'market': ticker["market"],
#                     'close': ticker["c"],
#                     'open': ticker["o"],
#                     'high': ticker["h"],
#                     'low':  ticker["l"],
#                     'volume': ticker["v"],
#                     'quote': ticker["q"],
#                 }
#             )
#         except TypeError:
#             pass
#     # tickers = {"tickers": tickers}
#     # r.set("1mTicker", json.dumps(tickers), 86400)
#     # insertTickersList(tickers)
#     # connect(host=MONGO_URL)
#     headers = {
#         "Content-Type": "application/json",
#         "accept": "application/json"
#     }
#     if tickers:
#         requests.post(
#             os.environ.get('API') + "v2/tickers/", json=tickers, headers=headers)

#     # for tic in tickers:
#     # print(tic)

#     # print(type(tic))
#     # tickerTable = Tickers(
#     #     date=tic[0],
#     #     symbol=tic[1],
#     #     market=tic[2],
#     #     close=tic[3],
#     #     open=tic[4],
#     #     high=tic[5],
#     #     low=tic[6],
#     #     volume=tic[7],
#     #     quote=tic[8])
#     # tickerTable.save()
#     # PostTicker(data={
#     #     "symbol": str(tic[1]),
#     #     "market": str(tic[2]),
#     #     "close": float(tic[3]),
#     #     "open": float(tic[4]),
#     #     "high": float(tic[5]),
#     #     "low": float(tic[6]),
#     #     "volume": float(tic[7]),
#     #     "quote": float(tic[8])
#     # })

#     # PostTicker2.delay(data={
#     #     # "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M"),
#     #     "symbol": str(tic[1]),
#     #     "market": str(tic[2]),
#     #     "close": float(tic[3]),
#     #     "open": float(tic[4]),
#     #     "high": float(tic[5]),
#     #     "low": float(tic[6]),
#     #     "volume": float(tic[7]),
#     #     "quote": float(tic[8])
#     # })

#     # disconnect()


# @shared_task
# def PostTicker(data):
#     requests.post(
#         "http://nextjs:3000/api/tickers/newTicker", data=data)


# @shared_task
# def PostTicker2(data):
#     '''post ticker to mongo'''

#     headers = {
#         "Content-Type": "application/json",
#         "accept": "application/json"
#     }
#     requests.post(
#         os.environ.get('API') + "v2/ticker/", json=data, headers=headers)


# @shared_task
# def UpdateBarometer(save=False):

#     # if save:
#     #     storeTickersToDatabase.delay()
#     # try:
#     # print(get_connection())
#     dateNow = datetime.datetime.now()
#     brl_markets = []
#     bkrw_markets = []
#     aud_markets = []
#     doge_markets = []
#     eur_markets = []
#     bnb_markets = []
#     busd_markets = []
#     usdc_markets = []
#     rub_markets = []
#     usdp_markets = []
#     gbp_markets = []
#     trx_markets = []
#     zar_markets = []
#     bidr_markets = []
#     usds_markets = []
#     try_markets = []
#     ngn_markets = []
#     xrp_markets = []
#     uah_markets = []
#     bvnd_markets = []
#     gyen_markets = []
#     eth_markets = []
#     ust_markets = []
#     pax_markets = []
#     idrt_markets = []
#     dot_markets = []
#     vai_markets = []
#     dai_markets = []
#     btc_markets = []
#     usdt_markets = []
#     tusd_markets = []
#     fiat_btc_markets = []
#     fiat_eth_markets = []
#     fiat_bnb_markets = []

#     keys = r.keys("market*")
#     quotePairs = []
#     basePairs = ['BRL', 'BKRW', 'AUD', 'DOGE', 'EUR', 'BNB', 'BUSD', 'USDC', 'RUB', 'USDP', 'GBP', 'TRX', 'ZAR', 'BIDR', 'USDS',
#                  'TRY', 'NGN', 'XRP', 'UAH', 'BVND', 'GYEN', 'ETH', 'UST', 'PAX', 'IDRT', 'DOT', 'VAI', 'DAI', 'BTC', 'USDT', 'TUSD']
#     newPairs = []
#     for key in keys:
#         market = dict(json.loads(r.get(key)))
#         quotePairs.append(market["quote"])

#         # print(market)
#         # print(type(market))
#         if market["quote"] == "BRL":
#             brl_markets.append(market)
#         if market["quote"] == "BKRW":
#             bkrw_markets.append(market)
#         if market["quote"] == "AUD":
#             aud_markets.append(market)
#         if market["quote"] == "DOGE":
#             doge_markets.append(market)
#         if market["quote"] == "EUR":
#             eur_markets.append(market)
#         if market["quote"] == "BNB":
#             bnb_markets.append(market)
#         if market["quote"] == "RUB":
#             rub_markets.append(market)
#         if market["quote"] == "USDP":
#             usdp_markets.append(market)
#         if market["quote"] == "GBP":
#             gbp_markets.append(market)
#         if market["quote"] == "TRX":
#             trx_markets.append(market)
#         if market["quote"] == "ZAR":
#             zar_markets.append(market)
#         if market["quote"] == "BIDR":
#             bidr_markets.append(market)
#         if market["quote"] == "USDS":
#             usds_markets.append(market)
#         if market["quote"] == "TRY":
#             try_markets.append(market)
#         if market["quote"] == "NGN":
#             ngn_markets.append(market)
#         if market["quote"] == "XRP":
#             xrp_markets.append(market)
#         if market["quote"] == "UAH":
#             uah_markets.append(market)
#         if market["quote"] == "BVND":
#             bvnd_markets.append(market)
#         if market["quote"] == "GYEN":
#             gyen_markets.append(market)
#         if market["quote"] == "ETH":
#             eth_markets.append(market)
#         if market["quote"] == "UST":
#             ust_markets.append(market)
#         if market["quote"] == "PAX":
#             pax_markets.append(market)
#         if market["quote"] == "IDRT":
#             idrt_markets.append(market)
#         if market["quote"] == "DOT":
#             dot_markets.append(market)
#         if market["quote"] == "VAI":
#             vai_markets.append(market)
#         if market["quote"] == "DAI":
#             dai_markets.append(market)
#         if market["quote"] == "BTC":
#             btc_markets.append(market)

#         if market["quote"] == "USDT":
#             if market["base"] == "BTC":
#                 fiat_btc_markets.append(market)
#             elif market["base"] == "ETH":
#                 fiat_eth_markets.append(market)
#             elif market["base"] == "BNB":
#                 fiat_bnb_markets.append(market)
#             else:
#                 usdt_markets.append(market)

#         if market["quote"] == "TUSD":
#             if market["base"] == "BTC":
#                 fiat_btc_markets.append(market)
#             elif market["base"] == "ETH":
#                 fiat_eth_markets.append(market)
#             elif market["base"] == "BNB":
#                 fiat_bnb_markets.append(market)
#             else:
#                 tusd_markets.append(market)

#         if market["quote"] == "USDC":
#             if market["base"] == "BTC":
#                 fiat_btc_markets.append(market)
#             elif market["base"] == "ETH":
#                 fiat_eth_markets.append(market)
#             elif market["base"] == "BNB":
#                 fiat_bnb_markets.append(market)
#             else:
#                 usdc_markets.append(market)

#         if market["quote"] == "BUSD":
#             if market["base"] == "BTC":
#                 fiat_btc_markets.append(market)
#             elif market["base"] == "ETH":
#                 fiat_eth_markets.append(market)
#             elif market["base"] == "BNB":
#                 fiat_bnb_markets.append(market)
#             else:
#                 busd_markets.append(market)

#     quotePairsUnique = list(set(quotePairs))
#     # print(quotePairsUnique)
#     for pair in quotePairsUnique:
#         if pair not in basePairs:
#             # print(pair)
#             newPairs.append(pair)
#     total_brl_alt_volume = 0.0
#     total_bkrw_alt_volume = 0.0
#     total_aud_alt_volume = 0.0
#     total_doge_alt_volume = 0.0
#     total_rub_alt_volume = 0.0
#     total_trx_alt_volume = 0.0
#     total_zar_alt_volume = 0.0
#     total_bidr_alt_volume = 0.0
#     total_try_alt_volume = 0.0
#     total_ngn_alt_volume = 0.0
#     total_xrp_alt_volume = 0.0
#     total_bvnd_alt_volume = 0.0
#     total_gyen_alt_volume = 0.0
#     total_idrt_alt_volume = 0.0
#     total_dot_alt_volume = 0.0
#     total_vai_alt_volume = 0.0
#     total_dai_alt_volume = 0.0
#     total_pax_alt_volume = 0.0
#     total_usds_alt_volume = 0.0
#     total_uah_alt_volume = 0.0
#     total_ust_alt_volume = 0.0
#     total_eur_alt_volume = 0.0
#     total_busd_alt_volume = 0.0
#     total_usdc_alt_volume = 0.0
#     total_usdp_alt_volume = 0.0
#     total_gbp_alt_volume = 0.0
#     total_usdt_alt_volume = 0.0
#     total_tusd_alt_volume = 0.0

#     total_btc_alt_volume = 0.0
#     total_eth_alt_volume = 0.0
#     total_bnb_alt_volume = 0.0
#     total_btc_fiat_volume = 0.0
#     total_eth_fiat_volume = 0.0
#     total_bnb_fiat_volume = 0.0

#     for market in brl_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_brl_alt_volume += float(ticker["q"])
#     for market in bkrw_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_bkrw_alt_volume += float(ticker["q"])
#     for market in aud_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_aud_alt_volume += float(ticker["q"])
#     for market in doge_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_doge_alt_volume += float(ticker["q"])
#     for market in eur_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_eur_alt_volume += float(ticker["q"])

#     for market in busd_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_busd_alt_volume += float(ticker["q"])
#     for market in usdc_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_usdc_alt_volume += float(ticker["q"])
#     for market in rub_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_rub_alt_volume += float(ticker["q"])
#     for market in usdp_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_usdp_alt_volume += float(ticker["q"])
#     for market in gbp_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_gbp_alt_volume += float(ticker["q"])
#     for market in trx_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_trx_alt_volume += float(ticker["q"])
#     for market in zar_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_zar_alt_volume += float(ticker["q"])
#     for market in bidr_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_bidr_alt_volume += float(ticker["q"])
#     for market in usds_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_usds_alt_volume += float(ticker["q"])
#     for market in try_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_try_alt_volume += float(ticker["q"])
#     for market in ngn_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_ngn_alt_volume += float(ticker["q"])
#     for market in xrp_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_xrp_alt_volume += float(ticker["q"])
#     for market in uah_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_uah_alt_volume += float(ticker["q"])
#     for market in bvnd_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_bvnd_alt_volume += float(ticker["q"])
#     for market in gyen_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_gyen_alt_volume += float(ticker["q"])

#     for market in ust_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_ust_alt_volume += float(ticker["q"])
#     for market in pax_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_pax_alt_volume += float(ticker["q"])
#     for market in idrt_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_idrt_alt_volume += float(ticker["q"])
#     for market in dot_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_dot_alt_volume += float(ticker["q"])
#     for market in vai_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_vai_alt_volume += float(ticker["q"])
#     for market in dai_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_dai_alt_volume += float(ticker["q"])

#     for market in usdt_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_usdt_alt_volume += float(ticker["q"])
#     for market in tusd_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_tusd_alt_volume += float(ticker["q"])
# ####
#     for market in btc_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_btc_alt_volume += float(ticker["q"])  # volume = BTC

#     for market in eth_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_eth_alt_volume += float(ticker["q"])  # voluem = ETH

#     for market in bnb_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_bnb_alt_volume += float(ticker["q"])  # volume = BNB

#     for market in fiat_btc_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_btc_fiat_volume += float(ticker["q"])  # volume = USD

#     for market in fiat_eth_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_eth_fiat_volume += float(ticker["q"])  # volume = USD

#     for market in fiat_bnb_markets:
#         ticker = r.get(market["id"])
#         if ticker is not None:
#             ticker = dict(json.loads(ticker))
#             total_bnb_fiat_volume += float(ticker["q"])  # volume = USD

#     total_brl_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="BRL") * total_brl_alt_volume, 2)
#     total_bkrw_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="BKRW") * total_bkrw_alt_volume, 2)
#     total_aud_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="AUD") * total_aud_alt_volume, 2)
#     total_doge_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="DOGE") * total_doge_alt_volume, 2)
#     total_rub_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="RUB") * total_rub_alt_volume, 2)
#     total_trx_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="TRX") * total_trx_alt_volume, 2)
#     total_zar_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="ZAR") * total_zar_alt_volume, 2)
#     total_bidr_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="BIDR") * total_bidr_alt_volume, 2)
#     total_try_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="TRY") * total_try_alt_volume, 2)
#     total_ngn_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="NGN") * total_ngn_alt_volume, 2)
#     total_xrp_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="XRP") * total_xrp_alt_volume, 2)
#     total_bvnd_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="BVND") * total_bvnd_alt_volume, 2)
#     total_gyen_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="GYEN") * total_gyen_alt_volume, 2)
#     total_idrt_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="IDRT") * total_idrt_alt_volume, 2)
#     total_dot_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="DOT") * total_dot_alt_volume, 2)
#     total_vai_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="VAI") * total_vai_alt_volume, 2)
#     total_dai_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="DAI") * total_dai_alt_volume, 2)
#     total_pax_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="PAX") * total_pax_alt_volume, 2)
#     total_usds_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="USDS") * total_usds_alt_volume, 2)
#     total_uah_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="UAH") * total_uah_alt_volume, 2)
#     total_ust_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="UST") * total_ust_alt_volume, 2)
#     total_eur_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="EUR") * total_eur_alt_volume, 2)
#     total_busd_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="BUSD") * total_busd_alt_volume, 2)
#     total_usdc_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="USDC") * total_usdc_alt_volume, 2)
#     total_usdp_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="USDP") * total_usdp_alt_volume, 2)
#     total_gbp_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="GBP") * total_gbp_alt_volume, 2)

#     # print(
#     #     total_brl_alt_volume_usdt,
#     #     total_bkrw_alt_volume_usdt,
#     #     total_aud_alt_volume_usdt,
#     #     total_doge_alt_volume_usdt,
#     #     total_rub_alt_volume_usdt,
#     #     total_trx_alt_volume_usdt,
#     #     total_zar_alt_volume_usdt,
#     #     total_bidr_alt_volume_usdt,
#     #     total_try_alt_volume_usdt,
#     #     total_ngn_alt_volume_usdt,
#     #     total_xrp_alt_volume_usdt,
#     #     total_bvnd_alt_volume_usdt,
#     #     total_gyen_alt_volume_usdt,
#     #     total_idrt_alt_volume_usdt,
#     #     total_dot_alt_volume_usdt,
#     #     total_vai_alt_volume_usdt,
#     #     total_dai_alt_volume_usdt,
#     #     total_pax_alt_volume_usdt,
#     #     total_usds_alt_volume_usdt,
#     #     total_uah_alt_volume_usdt,
#     #     total_ust_alt_volume_usdt,
#     #     total_eur_alt_volume_usdt,
#     #     total_busd_alt_volume_usdt,
#     #     total_usdc_alt_volume_usdt,
#     #     total_usdp_alt_volume_usdt,
#     #     total_gbp_alt_volume_usdt
#     # )

#     total_btc_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="BTC") * total_btc_alt_volume, 2
#     )
#     total_bnb_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="ETH") * total_eth_alt_volume, 2
#     )
#     total_eth_alt_volume_usdt = round(
#         CalculateDollarPrice(coin="BNB") * total_bnb_alt_volume, 2
#     )

#     total_volume = (
#         total_btc_alt_volume_usdt
#         + total_eth_alt_volume_usdt
#         + total_bnb_alt_volume_usdt
#         + total_btc_fiat_volume
#         + total_eth_fiat_volume
#         + total_bnb_fiat_volume
#     )

#     try:
#         btc_strength = round(
#             (total_btc_alt_volume_usdt * 100)
#             / (total_btc_alt_volume_usdt + total_btc_fiat_volume),
#             4,
#         )
#     except TypeError:
#         btc_strength = 0
#     except ZeroDivisionError:
#         btc_strength = 0

#     try:
#         eth_strength = round(
#             (total_eth_alt_volume_usdt * 100)
#             / (total_eth_alt_volume_usdt + total_eth_fiat_volume),
#             4,
#         )
#     except TypeError:
#         eth_strength = 0
#     except ZeroDivisionError:
#         eth_strength = 0

#     try:
#         bnb_strength = round(
#             (total_bnb_alt_volume_usdt * 100)
#             / (total_bnb_alt_volume_usdt + total_bnb_fiat_volume),
#             4,
#         )
#     except TypeError:
#         bnb_strength = 0
#     except ZeroDivisionError:
#         bnb_strength = 0

#     # data = [
#     #     dateNow,
#     #     total_btc_fiat_volume,
#     #     total_eth_fiat_volume,
#     #     total_bnb_fiat_volume,
#     #     total_btc_alt_volume_usdt,
#     #     total_eth_alt_volume_usdt,
#     #     total_bnb_alt_volume_usdt,
#     #     total_volume,
#     #     btc_strength,
#     #     eth_strength,
#     #     bnb_strength,
#     # ]
#     data = {

#         "fiatBtcVolume": total_btc_fiat_volume,
#         "fiatEthVolume": total_eth_fiat_volume,
#         "fiatBnbVolume": total_bnb_fiat_volume,
#         "btcAltVolume": total_btc_alt_volume_usdt,
#         "ethAltVolume": total_eth_alt_volume_usdt,
#         "bnbAltVolume": total_bnb_alt_volume_usdt,
#         "totalVolume": total_volume,
#         "altBtcStrength": btc_strength,
#         "altEthStrength": eth_strength,
#         "altBnbStrength": bnb_strength,
#     }
#     data1Test = {
#         # "date": datetime.datetime.now().strftime("%s"),
#         "fiatBtcVolume": (total_btc_fiat_volume / 1000000),
#         "fiatEthVolume": (total_eth_fiat_volume / 1000000),
#         "fiatBnbVolume": (total_bnb_fiat_volume / 1000000),
#         "btcAltVolume": (total_btc_alt_volume_usdt / 1000000),
#         "ethAltVolume": (total_eth_alt_volume_usdt / 1000000),
#         "bnbAltVolume": (total_bnb_alt_volume_usdt / 1000000),
#         "totalVolume": (total_volume / 1000000),
#         "altBtcStrength": btc_strength,
#         "altEthStrength": eth_strength,
#         "altBnbStrength": bnb_strength,
#         "total_brl_alt_volume_usdt": (total_brl_alt_volume_usdt / 1000000),
#         "total_bkrw_alt_volume_usdt": (total_bkrw_alt_volume_usdt / 1000000),
#         "total_aud_alt_volume_usdt": (total_aud_alt_volume_usdt / 1000000),
#         "total_doge_alt_volume_usdt": (total_doge_alt_volume_usdt / 1000000),
#         "total_rub_alt_volume_usdt": (total_rub_alt_volume_usdt / 1000000),
#         "total_trx_alt_volume_usdt": (total_trx_alt_volume_usdt / 1000000),
#         "total_zar_alt_volume_usdt": (total_zar_alt_volume_usdt / 1000000),
#         "total_bidr_alt_volume_usdt": (total_bidr_alt_volume_usdt / 1000000),
#         "total_try_alt_volume_usdt": (total_try_alt_volume_usdt / 1000000),
#         "total_ngn_alt_volume_usdt": (total_ngn_alt_volume_usdt / 1000000),
#         "total_xrp_alt_volume_usdt": (total_xrp_alt_volume_usdt / 1000000),
#         "total_bvnd_alt_volume_usdt": (total_bvnd_alt_volume_usdt / 1000000),
#         "total_gyen_alt_volume_usdt": (total_gyen_alt_volume_usdt / 1000000),
#         "total_idrt_alt_volume_usdt": (total_idrt_alt_volume_usdt / 1000000),
#         "total_dot_alt_volume_usdt": (total_dot_alt_volume_usdt / 1000000),
#         "total_vai_alt_volume_usdt": (total_vai_alt_volume_usdt / 1000000),
#         "total_dai_alt_volume_usdt": (total_dai_alt_volume_usdt / 1000000),
#         "total_pax_alt_volume_usdt": (total_pax_alt_volume_usdt / 1000000),
#         "total_usds_alt_volume_usdt": (total_usds_alt_volume_usdt / 1000000),
#         "total_uah_alt_volume_usdt": (total_uah_alt_volume_usdt / 1000000),
#         "total_ust_alt_volume_usdt": (total_ust_alt_volume_usdt / 1000000),
#         "total_eur_alt_volume_usdt": (total_eur_alt_volume_usdt / 1000000),
#         "total_busd_alt_volume_usdt": (total_busd_alt_volume_usdt / 1000000),
#         "total_usdc_alt_volume_usdt": (total_usdc_alt_volume_usdt / 1000000),
#         "total_usdp_alt_volume_usdt": (total_usdp_alt_volume_usdt / 1000000),
#         "total_gbp_alt_volume_usdt": (total_gbp_alt_volume_usdt / 1000000),
#     }
#     # connect(host=MONGO_URL)
#     data1 = {
#         "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M"),
#         "fiatBtcVolume": (total_btc_fiat_volume / 1000000),
#         "fiatEthVolume": (total_eth_fiat_volume / 1000000),
#         "fiatBnbVolume": (total_bnb_fiat_volume / 1000000),
#         "btcAltVolume": (total_btc_alt_volume_usdt / 1000000),
#         "ethAltVolume": (total_eth_alt_volume_usdt / 1000000),
#         "bnbAltVolume": (total_bnb_alt_volume_usdt / 1000000),
#         "totalVolume": (total_volume / 1000000),
#         "altBtcStrength": btc_strength,
#         "altEthStrength": eth_strength,
#         "altBnbStrength": bnb_strength,
#     }
#     headers = {
#         "Content-Type": "application/json",
#         "accept": "application/json"
#     }
#     # requests.post("http://nextjs:3000/api/baro/newBaro", data=data)
#     # requests.post("http://10.20.12.164:8000/api/v1/baro/",
#     #               json=data1, headers=headers)

#     # print(data1Test)
#     requests.post(os.environ.get('API') + "v2/baro/",
#                   json=data1Test, headers=headers)
#     # insertBaroData(baroData=data)
#     # baroTable = Baro(date=dateNow,
#     #                  fiatBtcVolume=total_btc_fiat_volume,
#     #                  fiatEthVolume=total_eth_fiat_volume,
#     #                  fiatBnbVolume=total_bnb_fiat_volume,
#     #                  btcAltVolume=total_btc_alt_volume_usdt,
#     #                  ethAltVolume=total_eth_alt_volume_usdt,
#     #                  bnbAltVolume=total_bnb_alt_volume_usdt,
#     #                  totalVolume=total_volume,
#     #                  altBtcStrength=btc_strength,
#     #                  altEthStrength=eth_strength,
#     #                  altBnbStrength=bnb_strength)
#     # baroTable.save()
#     # disconnect()


# @shared_task
# def CalculateDollarPrice(coin):
#     try:
#         price = dict(json.loads(r.get(coin + "USDT")))
#         # print(price)
#         price = float(price["c"])
#     except TypeError:
#         noValueCoins = ["BCX", "JEX", "QI"]
#         if coin not in noValueCoins:
#             price = GetDatabasePriceForPair(coin + "USDT")
#             if price == 0:
#                 price = GetDatabasePriceForPair("USDT" + coin)
#                 # print(price)
#                 if price == 0:
#                     return 0
#             # print(price)
#         else:
#             price = 0
#     return price


# @shared_task
# def CalculateBitcoinPrice(coin):
#     try:
#         # print(coin)
#         price = dict(json.loads(r.get(coin + "BTC")))
#         # print(price)
#         price = float(price["c"])
#     except TypeError:
#         if coin == "BTC":
#             price = 1
#         else:
#             noValueCoins = ["BCX", "JEX", "QI", "SBTC"]
#             if coin not in noValueCoins:
#                 price = GetDatabasePriceForPair(coin + "BTC")

#             else:
#                 price = 0
#     return price


# @shared_task
# def GetDatabasePriceForPair(pair):
#     # print(pair)
#     try:
#         # connect(host=MONGO_URL)
#         obj = requests.get(os.environ.get('API') + "v2/ticker/" + pair)
#         # obj = Tickers.objects.filter(market=pair).last()
#         # obj = filterTickers(market=pair)

#         if not obj:

#             return 0
#         # print(obj)
#         # print(obj.json())
#         # disconnect()
#         data = obj.json()
#         # print(data)
#         # print(type(data))
#         price = data['close']
#         # print(price)
#         return price
#     except AttributeError:
#         # print("Att error")
#         price = 0
#     except IndexError:
#         # print("Index error")
#         price = 0
#     return price


# # @shared_task
# # def GetBalances():
# #     balances = []
# #     # try:
# #     balance = binance.fetch_balance()
# #     # connect(host=MONGO_URL)
# #     # print(balance)
# #     # btcUsdtPrice = CalculateDollarPrice("BTC")
# #     # print(btcUsdtPrice)
# #     # remove empty coins and calculate btc and usdt prices
# #     for asset in balance["info"]["balances"]:
# #         total = float(asset["free"]) + float(asset["locked"])
# #         if total != 0:
# #             coinbtcPrice = CalculateBitcoinPrice(asset["asset"])
# #             usdtPrice = CalculateDollarPrice(asset["asset"])
# #             if asset["asset"] != "BTC":
# #                 tickers = Tickers.objects.filter(symbol=asset["asset"] + "BTC")
# #                 # tickers = filterTickers(market=asset["asset"] + "/BTC")
# #                 # print(tickers)
# #                 if len(tickers) > 1:
# #                     vol = tickers[0][9]
# #                     vol1m = tickers[1][9]
# #                 else:
# #                     vol = 0
# #                     vol1m = 0

# #                 if len(tickers) > 5:
# #                     vol5m = tickers[5][9]
# #                 else:
# #                     vol5m = 0

# #                 if len(tickers) > 60:
# #                     vol1h = tickers[60][9]
# #                 else:
# #                     vol1h = 0

# #                 if len(tickers) > 1440:
# #                     vol1d = tickers[1440][9]
# #                 else:
# #                     vol1d = 0

# #             else:
# #                 tickers = Tickers.objects.filter(
# #                     symbol=asset["asset"] + "USDT")
# #                 # tickers = filterTickers(market=asset["asset"] + "/USDT")
# #                 # print(tickers)
# #                 if len(tickers) > 1:
# #                     vol = tickers[0][8]
# #                     vol1m = tickers[1][8]
# #                 else:
# #                     vol = 0
# #                     vol1m = 0

# #                 if len(tickers) > 5:
# #                     vol5m = tickers[5][8]
# #                 else:
# #                     vol5m = 0

# #                 if len(tickers) > 60:
# #                     vol1h = tickers[60][8]
# #                 else:
# #                     vol1h = 0

# #                 if len(tickers) > 1440:
# #                     vol1d = tickers[1440][8]
# #                 else:
# #                     vol1d = 0

# #             # print("tickerCount:")
# #             # print(len(tickers))
# #             # print(tickers.first())
# #             # print(tickers.last())
# #             if coinbtcPrice != 0:
# #                 balances.append(
# #                     {
# #                         "asset": asset["asset"],
# #                         "free": asset["free"],
# #                         "used": asset["locked"],
# #                         "total": total,
# #                         "btcPrice": coinbtcPrice,
# #                         "btcTotal": round(coinbtcPrice * total, 8),
# #                         "usdtPrice": usdtPrice,
# #                         "usdtTotal": round(usdtPrice * total, 2),
# #                         "vol": vol,
# #                         "vol1m": vol1m,
# #                         "vol5m": vol5m,
# #                         "vol1h": vol1h,
# #                         "vol1d": vol1d,
# #                         "image": "none",
# #                     }
# #                 )
# #             else:
# #                 balances.append(
# #                     {
# #                         "asset": asset["asset"],
# #                         "free": asset["free"],
# #                         "used": asset["locked"],
# #                         "total": total,
# #                         "btcPrice": 0,
# #                         "btcTotal": 0,
# #                         "usdtPrice": 0,
# #                         "usdtTotal": 0,
# #                         "vol": vol,
# #                         "vol1m": vol1m,
# #                         "vol5m": vol5m,
# #                         "vol1h": vol1h,
# #                         "vol1d": vol1d,
# #                         "image": "none",
# #                     }
# #                 )
# #     # clean old balance in database
# #     # Balances.objects.all().delete()

# #     # for balance in balances:
# #     #     logofile = (
# #     #         "./compose/production/images/images/" + balance["asset"] + "-logo.svg"
# #     #     )
# #     #     # save new
# #     #     if os.path.isfile(logofile):
# #     #         image = balance["asset"]
# #     #     else:
# #     #         image = "none"
# #     #     table = Balances()
# #     #     table.asset = balance["asset"]
# #     #     table.free = round(float(balance["free"]), 5)
# #     #     table.used = round(float(balance["used"]), 5)
# #     #     table.total = round(float(balance["total"]), 5)
# #     #     table.btcPrice = round(float(balance["btcPrice"]), 8)
# #     #     table.btcTotal = round(float(balance["btcTotal"]), 8)
# #     #     table.usdtPrice = round(float(balance["usdtPrice"]), 2)
# #     #     table.usdtTotal = round(float(balance["usdtTotal"]), 2)
# #     #     table.image = image
# #     #     table.vol = round(float(balance["vol"]), 2)
# #     #     table.vol1m = round(float(balance["vol1m"]), 2)
# #     #     table.vol5m = round(float(balance["vol5m"]), 2)
# #     #     table.vol1h = round(float(balance["vol1h"]), 2)
# #     #     table.vol1d = round(float(balance["vol1d"]), 2)
# #     #     table.save()
# #     # except:
# #     #    pass
# #     disconnect()
# #     r.set("balances", str(json.dumps({"balances": balances})))


# @shared_task
# def buildIndicatorsFromCandles():
#     # dateNow = datetime.datetime.now()
#     # queryTime = datetime.datetime.now() - datetime.timedelta(minutes=30)
#     # tableTickers = Tickers.objects.all().filter(date__gte=queryTime)
#     # tableTickers = indicatorTickers([queryTime, dateNow])
#     # tableTickers =
#     # response = requests.get(
#     #     'http://10.20.12.164:8000/api/v2/ticker/')
#     # if not response:
#     #     return 'error'
#     # filterTicker = response.json()
#     # print(len(tableTickers))
#     print('starting calculations')
#     keys = r.keys("market*")
#     # print('keys:')
#     # print(keys)
#     # channel_layer = get_channel_layer()
#     for key in keys:
#         # only btc pairs for now!!
#         market = dict(json.loads(r.get(key)))
#         if market["quote"] == "BTC":
#             # print(market["id"])
#             response = requests.get(
#                 os.environ.get('API') + 'v2/tickers/' + market["id"])
#             # print(response)
#             if not response:
#                 continue
#             filterTicker = response.json()
#             # print(len(filterTicker))

#             # filterTicker = []
#             # try:
#             # for x in tableTickers:
#             # if market["id"] in x:
#             # filterTicker.append(x)
#             # print(filterTicker)
#             # print(len(filterTicker))
#             # df.to_timeseries(index='date')
#             # print(df)
#             if len(filterTicker) > 21:  # minimum 20 tickers to build BolingerBands
#                 df = pd.DataFrame(
#                     filterTicker,
#                     columns=[
#                         "id",
#                         "date",
#                         "symbol",
#                         "market",
#                         "close",
#                         "open",
#                         "high",
#                         "low",
#                         "volume",
#                         "quote",
#                     ],
#                 )
#                 # print(df)
#                 # print(len(filterTicker))
#                 lastTicker = filterTicker[-1]
#                 # print(lastTicker)
#                 # print(type(lastTicker))
#                 if lastTicker['quote'] > 50:  # ! min volume > 50 BTC
#                     # print(type(lastTicker))
#                     # print(lastTicker.quote)
#                     # df = filterTicker.to_timeseries(index="date")
#                     print('VOLUME OK')
#                     # print(len(filterTicker))
#                     # print(lastTicker)
#                     # df.ta.indicators()
#                     # help(ta.stoch)
#                     # Returns:   BB          > help(ta.bbands)
#                     #    pd.DataFrame: lower, mid, upper, bandwidth columns.
#                     df.ta.bbands(
#                         close=df["close"],
#                         length=20,
#                         std=2,
#                         mamode="sma",
#                         cumulative=True,
#                         append=True,
#                         fill='nearest',
#                     )
#                     # print(df.tail())
#                     # print(df.columns)
#                     if (
#                         float(df.iloc[-1, df.columns.get_loc("close")])
#                         < float(df.iloc[-1, df.columns.get_loc("BBL_20_2.0")])
#                         and float(df.iloc[-1, df.columns.get_loc("BBB_20_2.0")]) >= 1.5
#                     ):
#                         # print(df["BBB_20_2.0"])
#                         print(df.iloc[
#                                 -1, df.columns.get_loc("symbol", "BBL_20_2.0", "BBL_20_2.0")
#                             ])
#                         # print(df.tail())
#                         # Returns:   STOCH       > help(ta.stoch)
#                         #     pd.DataFrame: %K, %D columns.
#                         df.ta.stoch(
#                             high=df["high"],
#                             low=df["low"],
#                             smooth_k=1,
#                             cumulative=True,
#                             append=True,
#                         )
#                         # print(df.columns)
#                         # print(df.tail())
#                         # Index(['id', 'symbol', 'market', 'close', 'open', 'high', 'low', 'volume',
#                         # 'quote', 'BBL_20_2.0', 'BBM_20_2.0', 'BBU_20_2.0', 'BBB_20_2.0',
#                         # 'STOCHk_14_3_1', 'STOCHd_14_3_1'],dtype='object')
#                         # df.iloc[-1:]
#                         if float(df.iloc[-1, df.columns.get_loc("STOCHk_14_3_1")]) < 20:
#                             # print(df.tail())
#                             # print(df.columns)
#                             print(
#                                 str(df.iloc[-1, df.columns.get_loc("symbol")])
#                                 + " found something: "
#                                 + lastTicker[1].strftime("%y-%m-%d %H:%M")
#                                 + " (UTC)  Price: "
#                                 + str(df.iloc[-1, df.columns.get_loc("close")])
#                                 + " -> BB: "
#                                 + str(df.iloc[-1, df.columns.get_loc("BBL_20_2.0")])
#                                 + " Stoch: "
#                                 + str(df.iloc[-1, df.columns.get_loc("STOCHk_14_3_1")])
#                             )
#                             data = {
#                                 "date": lastTicker[1].strftime("%y-%m-%d %H:%M"),
#                                 "symbol": df.iloc[-1, df.columns.get_loc("symbol")],
#                                 "market": df.iloc[-1, df.columns.get_loc("market")],
#                                 "close": round(
#                                     df.iloc[-1, df.columns.get_loc("close")], 8
#                                 ),
#                                 "volume": round(
#                                     df.iloc[-1,
#                                             df.columns.get_loc("volume")], 2
#                                 ),
#                                 "quote": round(
#                                     df.iloc[-1, df.columns.get_loc("quote")], 2
#                                 ),
#                                 "bbl": round(
#                                     df.iloc[-1,
#                                             df.columns.get_loc("BBL_20_2.0")], 8
#                                 ),
#                                 "bbm": round(
#                                     df.iloc[-1,
#                                             df.columns.get_loc("BBM_20_2.0")], 8
#                                 ),
#                                 "bbu": round(
#                                     df.iloc[-1,
#                                             df.columns.get_loc("BBU_20_2.0")], 8
#                                 ),
#                                 "bbb": round(
#                                     df.iloc[-1,
#                                             df.columns.get_loc("BBB_20_2.0")], 1
#                                 ),
#                                 "stochk": round(
#                                     df.iloc[-1,
#                                             df.columns.get_loc("STOCHk_14_3_1")], 0
#                                 ),
#                                 "stockd": round(
#                                     df.iloc[-1,
#                                             df.columns.get_loc("STOCHd_14_3_1")], 0
#                                 ),
#                             }
#                             oldAlerts = r.get("alerts")
#                             # print(oldAlerts)
#                             # print(type(oldAlerts))
#                             if oldAlerts is not None:
#                                 oldAlerts = json.loads(oldAlerts)
#                                 print(type(oldAlerts))
#                                 oldAlerts.append(data)
#                                 r.set("alerts", json.dumps(oldAlerts))
#                             else:
#                                 r.set("alerts", json.dumps([data]))
#                             print(data)
#                             # insertAlert(data)
#                         # else:
#                         # print('found nothing: '+ lastTicker.date.strftime('%y-%m-%d %H:%M') + '(UTC)  Price: ' +
#                         # str(df.iloc[-1, df.columns.get_loc('close')])  +
#                         # str(df.iloc[-1, df.columns.get_loc('symbol')]) + ' -> BB: ' +
#                         # str(df.iloc[-1, df.columns.get_loc('BBL_20_2.0')]) + ' Stoch: ' +
#                         # str(df.iloc[-1, df.columns.get_loc('STOCHk_14_3_1')]))
#             # except KeyError:
#             #     pass
#             # except TypeError:
#             #     # import logging
#             #     # logging.info('error')
#             #     pass


# @shared_task
# def cleanAlerts():
#     r.delete("alerts")


# # @shared_task
# # def updateOpenorders():
# #     # import logging
# #     # logging.info(BinancePairs)
# #     balances = dict(json.loads(r.get("balances")))
# #     # print(balances)
# #     allOrders = []
# #     for balance in balances['balances']:
# #         print(balance)
# #         print(type(balance))
# #         if balance['used'] != '0.00000000':
# #             try:
# #                 pairs = findPairByCoin(balance['asset'])
# #                 print(pairs)
# #                 for pair in pairs:
# #                     print(pair)
# #                     # logging.info(pair)
# #                     orders = binance.fetch_open_orders(pair)
# #                     print(orders)
# #                     # print(type(orders))
# #                     for order in orders:
# #                         if order not in allOrders:
# #                             allOrders.append(order)
# #                     time.sleep(0.5)
# #                 time.sleep(0.5)
# #             except:
# #                 print('error:')
# #                 print(balance)
# #     # channel_layer = get_channel_layer()
# #     # async_to_sync(channel_layer.group_send)(
# #     #     'private',
# #     #     {
# #     #         'type': 'orders_update',
# #     #         'orders': allOrders
# #     #     }
# #     # )
# #     r.set('all_orders', str(json.dumps({'orders': allOrders})), 86400)
# #     return 'Orders Send.'


# @shared_task
# def findPairByCoin(coin):
#     '''find pair by coin'''
#     markets = []
#     keys = r.keys('market*')
#     print(keys)
#     print(type(keys))
#     try:
#         for key in keys:
#             markets.append(r.get(key))
#         foundPair = []
#         # print(markets)
#         for market in markets:
#             pairs = market['symbol']
#             pairs1 = pairs.split('/')
#             for pair in pairs1:
#                 if pair == coin:
#                     foundPair.append(pairs)
#         return(foundPair)
#     except:
#         return(None)


# @shared_task
# def resample_baros(timeframe, baros):
#     '''resample baros'''

#     df = pd.DataFrame(baros)
#     df['date'] = pd.to_datetime(df['date'])
#     # print(df.columns)
#     # print(df)
#     df = df.set_index('date')
#     data = []
#     # print(df)
#     df = df.resample(timeframe).mean().interpolate()
#     # df = df.resample(timeframe).mean().fillna(0)
#     # print(df)
#     # print(df.columns)
#     # print(type(df))
#     for index, row in df.iterrows():
#         # print(index.strftime('%Y-%m-%d %H:%M:%S'))
#         # print(row)
#         data.append({
#             "date": index.strftime('%m/%d/%Y, %H:%M'),
#             "totalVolume": row['totalVolume'],
#             "altBtcStrength": row['altBtcStrength'],
#             "altEthStrength": row['altEthStrength'],
#             "altBnbStrength": row['altBnbStrength'],
#             "fiatBtcVolume": row['fiatBtcVolume'],
#             "fiatEthVolume": row['fiatEthVolume'],
#             "fiatBnbVolume": row['fiatBnbVolume'],
#             "btcAltVolume": row['btcAltVolume'],
#             "ethAltVolume": row['ethAltVolume'],
#             "bnbAltVolume": row['bnbAltVolume']
#         })
#     data = data[::-1]
#     return data


# @shared_task
# def get_balance(apikey, apisecret):
#     binance = exchange_class(
#         {
#             "apiKey": apikey,
#             "secret": apisecret,
#             "timeout": 2400000,
#             "enableRateLimit": True,
#         }
#     )
#     balances = binance.fetch_balance()
#     print(balances)
#     return balances


# @shared_task
# def clean_old_tickers():
#     '''clean old tickers'''
#     page = 1
#     # i = 0
#     # cleaning = True
#     # while cleaning:
#     response = requests.get(
#         os.environ.get('API') + 'v2/tickerexpired/4')
#     if not response:
#         return 'error'
#     data = response.json()

#     # # print(data)
#     # # print(type(data))
#     # for data_id in data["items"]:
#     #     print(data_id)
#     #     # print(type(data_id))
#     #     requests.delete('http://10.20.12.164:8000/api/v2/ticker/' + str(data_id))
#     #     i += 1
#     # if data["size"] > data["total"]:
#     #     cleaning = False
#     #     return 'deleted ' + str(i) + ' tickers'
#     return data

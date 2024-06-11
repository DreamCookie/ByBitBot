from keys import api, secret
from pybit.unified_trading import HTTP
import pandas as pd
import ta
import requests
import time
from time import sleep
import hashlib
import hmac
import json
# from Crypto.Cipher import AES

session = HTTP(
    # testnet=True,
    api_key= api,
    api_secret= secret,
)

tp = 0.02 # take profit (2%)
sl = 0.01 # stop loss (1%)
timeframe = 15 #(min)
mode = 1 # isolated now (0 for cross)
leverage = 10
qty = 50

# Getting balance on Bybit Derivatrives Asset (in USDT)
def get_balance():
    try:
        response = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        # print("API Response:", response)  #debug
        if response['retCode'] == 0:
            balance = response['result']['list'][0]['coin'][0]['walletBalance']
            return float(balance)
        else:
            raise Exception(response['retMsg'])
    except Exception as err:
        print("Error:", err)
        return None
print(f'Your balance: {get_balance()} USDT')

# Getting all available symbols from Derivatives market (like 'BTCUSDT', 'XRPUSDT', etc)
def get_tickers():
    try:
        resp = session.get_tickers(category="linear")['result']['list']
        symbols = []
        for elem in resp:
            if 'USDT' in elem['symbol'] and not 'USDC' in elem['symbol']:
                symbols.append(elem['symbol'])
        return symbols
    except Exception as err:
        print(err)


# Klines is the candles of some symbol (up to 1500 candles). Dataframe, last elem has [-1] index
def klines(symbol):
    try:
        resp = session.get_kline(
            category='linear',
            symbol=symbol,
            interval=timeframe,
            limit=500
        )['result']['list']
        resp = pd.DataFrame(resp)
        resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']
        resp = resp.set_index('Time')
        resp = resp.astype(float)
        resp = resp[::-1]
        return resp
    except Exception as err:
        print(err)
        
print(klines('XRPUSDT'))


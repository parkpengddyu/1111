import time
import pyupbit
import datetime

access = "mfsl5mu0PxiKky58Fh6Fghe0RzxkyyCNE0Do9L1I"
secret = "PJIveJ3mRFWxxlg2v4mrglIuxxEcnfOcrHhGTeT9"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
money = get_balance("KRW")
print(money)
moneyb = get_balance("BTC")
print(moneyb)
moneye = get_balance("ETH")
print(moneye)
moneyd = get_balance("DOGE")
print(moneyd)
print("autotrade start")
# 자동매매 시작


while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=100) :
            #BTC
            target_price_btc = get_target_price("KRW-BTC", 0.5)
            current_price_btc = get_current_price("KRW-BTC")
            #ETH
            target_price_eth = get_target_price("KRW-ETH", 0.5)
            current_price_eth = get_current_price("KRW-ETH")
            #DOGE
            target_price_doge = get_target_price("KRW-DOGE", 0.5)
            current_price_doge = get_current_price("KRW-DOGE")
            krw = get_balance("KRW")
            btc = get_balance("BTC")
            eth = get_balance("ETH")
            doge = get_balance("DOGE")
            

            if target_price_btc < current_price_btc and btc < 0.01 :
                if eth < 0.1 and doge < 3000 and krw > 10000:
                        upbit.buy_market_order("KRW-BTC", krw*0.5950)
                        print("btc long")
                if eth > 0.1 and doge > 3000 and krw > 10000:
                        upbit.buy_market_order("KRW-BTC", krw*0.9950)
                        print("btc long")
                if eth > 0.1 and doge < 3000 and krw > 10000:
                        upbit.buy_market_order("KRW-BTC", krw*0.7950)
                        print("btc long")
                if eth < 0.1 and doge > 3000 and krw > 10000:
                        upbit.buy_market_order("KRW-BTC", krw*0.7000)
                        print("btc long")
            if target_price_eth < current_price_eth and eth < 0.1 :
                if btc < 0.01 and doge < 3000 and krw > 10000:
                        upbit.buy_market_order("KRW-ETH", krw*0.2450)
                        print("eth long")
                if btc > 0.01 and doge > 3000 and krw > 10000:
                        upbit.buy_market_order("KRW-ETH", krw*0.9950)
                        print("eth long")
                if btc > 0.01 and doge < 3000 and krw > 10000:
                        upbit.buy_market_order("KRW-ETH", krw*0.6200)
                        print("eth long")
                if btc < 0.01 and doge > 3000 and krw > 10000:
                        upbit.buy_market_order("KRW-ETH", krw*0.2900)
                        print("eth long")
            if  target_price_doge < current_price_doge and doge < 3000:
                if btc < 0.01 and eth < 0.1 and krw > 10000:
                        upbit.buy_market_order("KRW-DOGE", krw*0.1450)
                        print("doge long")
                if btc > 0.01 and eth < 0.1 and krw > 10000:
                        upbit.buy_market_order("KRW-DOGE", krw*0.9950)
                        print("doge long")
                        
                if btc > 0.01 and eth < 0.1 and krw > 10000:
                        upbit.buy_market_order("KRW-DOGE", krw*0.3700)
                        print("doge long")
                        
                if btc < 0.01 and eth > 0.1 and krw > 10000:
                        upbit.buy_market_order("KRW-DOGE", krw*0.1950)
                        print("doge long")
            
        else:

            krw = get_balance("KRW")
            btc = get_balance("BTC")
            eth = get_balance("ETH")
            doge = get_balance("DOGE")
            #BTC
            upbit.sell_market_order("KRW-BTC", btc)
            #ETH
            upbit.sell_market_order("KRW-ETH", eth)
            #DOGE
            upbit.sell_market_order("KRW-DOGE", doge)

        time.sleep(5)
        
    except Exception as e:
        print(e)
        time.sleep(10)

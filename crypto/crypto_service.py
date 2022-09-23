import datetime
import threading
import time
import pybithumb
import json
import schedule


class crypto_service:

    target_price = 0
    now_price = 0

    def __init__(self,ticker):
        self.ticker = ticker

    def bull_market_v1(ticker):
        df = pybithumb.get_ohlcv(ticker)
        ma5 = df['close'].rolling(window=5).mean()
        price = pybithumb.get_current_price(ticker)
        last_ma5 = ma5[-2]

        state = None
        if price > last_ma5:
            state = True
        else:
            state = False
        
        return json.dumps({ "price" : price, "last_ma5" : last_ma5, "state" : state})

    def excute_target_price_thread(self,ticker):
        thread = threading.Thread(target=crypto_service.__buy_volatility_breakout, args=(self,ticker,))
        thread.start()

    def reset_target_price(ticker):
        schedule.every().day.at("00:00").do(crypto_service.__get_target_price, args=(ticker,) )
        while True:
            schedule.run_pending()
            time.sleep(1)

    def do_volatility_breakout(self):
        crypto_service.excute_target_price_thread(self,self.ticker)
        crypto_service.reset_target_price(self.ticker)


    def __get_target_price(self):

        df = pybithumb.get_ohlcv(self.ticker)
        yesterday = df.iloc[-2]

        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        target = today_open + (yesterday_high - yesterday_low) * 0.5
        crypto_service.target_price = target

    def __buy_volatility_breakout(self,ticker):

        while True:
            crypto_service.__get_target_price(self)
            crypto_service.now_price = pybithumb.get_current_price(ticker)

            if crypto_service.now_price > crypto_service.target_price:
                print("buy")
                #TODO 사라는 request를 user_server에 보내야 한다.
            time.sleep(1)


cs = crypto_service("BTC")
cs.do_volatility_breakout()

    


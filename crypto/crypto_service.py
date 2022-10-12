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

    #상승장 알림
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
        
        #장중 5일 이동평균선 가져와서 현재가격이 더 높으면 true(산다) 아니면 false(사지않는다)
        return json.dumps({ "price" : price, "last_ma5" : last_ma5, "state" : state})

    def get_target_prices():
        curData = {}
        targetData = {}
        tickers = pybithumb.get_tickers()
        for coin in tickers:
            curData.update({coin : pybithumb.get_current_price(coin)})
            targetData.update(crypto_service.__get_target_price_v2(coin))
        
        return json.dumps({"curData":curData, "targetData": targetData})

    #변동성 돌파 전략
    def do_volatility_breakout(self):
        crypto_service.excute_target_price_thread(self,self.ticker)
        crypto_service.reset_target_price(self.ticker)

    def excute_target_price_thread(self,ticker):
        thread = threading.Thread(target=crypto_service.__buy_volatility_breakout, args=(self,ticker,))
        thread.start()

    #매일 자정에 목표가 수정
    def reset_target_price(ticker):
        schedule.every().day.at("00:00").do(crypto_service.__get_target_price, args=(ticker,) )
        while True:
            schedule.run_pending()
            time.sleep(1)

    def __buy_volatility_breakout(self,ticker):

        while True:
            crypto_service.__get_target_price(self)
            crypto_service.now_price = pybithumb.get_current_price(ticker)

            if crypto_service.now_price > crypto_service.target_price:
                print("buy")
                #TODO 사라는 request를 user_server에 보내야 한다.
            time.sleep(1)


    def __get_target_price(self):

        df = pybithumb.get_ohlcv(self.ticker)
        yesterday = df.iloc[-2]

        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        target = today_open + (yesterday_high - yesterday_low) * 0.5
        crypto_service.target_price = target

    def __get_target_price_v2(ticker):

        df = pybithumb.get_ohlcv(ticker)
        yesterday = df.iloc[-2]

        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        target = today_open + (yesterday_high - yesterday_low) * 0.5
        return {ticker : target}

    


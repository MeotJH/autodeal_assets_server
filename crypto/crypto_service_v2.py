import datetime
import threading
import time
import pybithumb
import json
import schedule


class crypto_service:
    tickers = []
    curData = {}
    targetData = {}

    def __init__(self):
        self.tickers = pybithumb.get_tickers()
        self.__get_target_price_v2()

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
    
    #변동성 돌파 목표가 dictionary 만드는 함수
    def __get_target_price_v2(self):

        for coin in self.tickers:
            df = pybithumb.get_ohlcv(coin)
            yesterday = df.iloc[-2]  

            today_open = yesterday['close']
            yesterday_high = yesterday['high']
            yesterday_low = yesterday['low']
            target = today_open + (yesterday_high - yesterday_low) * 0.5
            self.targetData.update( {coin: target} )

    #매일 자정에 목표가 수정
    def reset_target_price(self):
        schedule.every().day.at("00:00").do(self.__get_target_price_v2, args=() )
        while True:
            schedule.run_pending()
            time.sleep(1)

    #매일 자정에 목표가 수정 배치 스레드
    def excute_reset_target_price_thread(self):
        thread = threading.Thread(target=self.reset_target_price, args=())
        thread.start()

    #변동성 돌파를 위한 현재가격을 추적하기 위한 스레드
    def excute_target_price_thread(self):
        thread = threading.Thread(target=self.__buy_volatility_breakout, args=())
        thread.start()

    #변동성 돌파를 위한 현재가격을 추적함수
    def __buy_volatility_breakout(self):
        
        #현재가격이 목표가보다 높으면 사라
        while True:
            for coin in self.tickers:
                # 변동성 돌파를 위한 현재가 dictionary만든다
                self.curData.update({coin : pybithumb.get_current_price(coin)})    

                # 현재가가 타겟가보다 높으면 산다는 신호를 보낸다
                if  self.curData.get(coin)  > self.targetData.get(coin):
                    print({"name": coin, "buy": True})
                    #TODO {"name": coin, "buy": True} request를 user_server에 보내야 한다.
            time.sleep(10)

    


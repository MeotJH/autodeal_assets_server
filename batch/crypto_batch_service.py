from crypto.crypto_service_v2 import crypto_service


class crypto_batch_service:

    crypto_service

    def __init__(self):
        self.crypto_service = crypto_service()

    #변동성 돌파 배치 시작
    def do_volatility_breakout(self):
        self.crypto_service.excute_target_price_thread()
        self.crypto_service.excute_reset_target_price_thread()
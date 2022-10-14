from flask import Flask
from batch.crypto_batch_service import crypto_batch_service
from crypto import crypto_controller
from crypto.crypto_service_v2 import crypto_service
app = Flask(__name__)

app.register_blueprint(crypto_controller.crypto, url_prefix="/api/crypto")

@app.route('/')
def index():
    return 'Hello World'

if __name__ == "__main__": 
    crypto_batch = crypto_batch_service()
    crypto_batch.do_volatility_breakout()
    app.run(host='127.0.0.1', port='5001', debug=True)
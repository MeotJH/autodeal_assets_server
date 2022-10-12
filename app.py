from flask import Flask
from crypto import crypto_controller
from crypto.crypto_service_v2 import crypto_service
app = Flask(__name__)

app.register_blueprint(crypto_controller.crypto, url_prefix="/api/crypto")

@app.route('/')
def index():
    return 'Hello World'

if __name__ == "__main__": 


    #service = crypto_service()
    #service.get_curData_prices()
    #다음과 같은 방식으로 init할 메소드들 만들면됨
    app.run(host='127.0.0.1', port='5001', debug=True)
from flask import Flask
from crypto import crypto_controller
app = Flask(__name__)

app.register_blueprint(crypto_controller.crypto, url_prefix="/api/crypto")


@app.route('/')
def index():
    return 'Hello World'



if __name__ == "__main__": 
    app.run(host='127.0.0.1', port='5001', debug=True)

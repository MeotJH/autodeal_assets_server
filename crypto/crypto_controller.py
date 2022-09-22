from flask import Blueprint
from . import crypto_service

#url_prefix="/api/crypto"
crypto = Blueprint("crypto", __name__)


@crypto.route('/')
def crypto_ready(): 
  return crypto_service.bull_market_v1("BTC")


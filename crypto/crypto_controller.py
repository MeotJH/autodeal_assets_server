from flask import Blueprint, request
from .crypto_service import crypto_service

#url_prefix="/api/crypto"
crypto = Blueprint("crypto", __name__)


@crypto.route('/')
def crypto_ready():
  ticker = request.args.get("ticker")
  return crypto_service.bull_market_v1(ticker)

@crypto.route('/prices')
def all_ticker_prices():
  return crypto_service.get_target_prices()
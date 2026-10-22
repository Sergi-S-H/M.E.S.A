from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)

# Solo acepta peticiones desde tu interfaz (sustituye la URL por la de tu Static Site)
CORS(app, origins=["https://m-e-s-a.onrender.com"])

@app.route("/")
def inicio():
    return "Servidor M.E.S.A. en funcionamiento"

import requests

@app.route("/api/search")
def search():
    q = request.args.get("q", "")
    r = requests.get(
        "https://query2.finance.yahoo.com/v1/finance/search",
        params={"q": q, "quotesCount": 8},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=8,
    )
    quotes = r.json().get("quotes", [])
    return jsonify([
        {"ticker": x["symbol"], "name": x.get("shortname") or x.get("longname") or x["symbol"]}
        for x in quotes if "symbol" in x
    ])

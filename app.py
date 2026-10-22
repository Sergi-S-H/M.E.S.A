from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route("/")
def inicio():
    return "Servidor MESA funcionando"

@app.route("/api/history")
def history():
    ticker = request.args.get("ticker", "^GSPC")
    df = yf.Ticker(ticker).history(period="3y")
    if df.empty:
        return jsonify({"error": "Sin datos para " + ticker}), 404
    return jsonify({
        "dates": [d.strftime("%Y-%m-%d") for d in df.index],
        "closes": df["Close"].round(4).tolist(),
    })

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

if __name__ == "__main__":
    app.run(port=8000)

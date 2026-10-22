from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)

# Solo acepta peticiones desde tu interfaz (sustituye la URL por la de tu Static Site)
CORS(app, origins=["https://m-e-s-a.onrender.com/"])

@app.route("/")
def inicio():
    return "Servidor M.E.S.A. en funcionamiento"

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

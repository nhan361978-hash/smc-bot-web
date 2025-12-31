
import streamlit as st
import ccxt
import pandas as pd

st.set_page_config(page_title="SMC BOT WEB", layout="wide")

SYMBOLS = ["BTC/USDT","ETH/USDT","SOL/USDT","ZEC/USDT"]
TIMEFRAME = "1h"

exchange = ccxt.binance({"enableRateLimit": True})

def fetch(symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, TIMEFRAME, limit=100)
    df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])
    return df

def bos(df):
    if df.high.iloc[-1] > df.high.iloc[-3] and df.low.iloc[-1] > df.low.iloc[-3]:
        return "BULLISH"
    if df.high.iloc[-1] < df.high.iloc[-3] and df.low.iloc[-1] < df.low.iloc[-3]:
        return "BEARISH"
    return "NONE"

def signal(df):
    trend = bos(df)
    if trend == "BULLISH":
        return "🟢 READY LONG"
    if trend == "BEARISH":
        return "🔴 READY SHORT"
    return "⚪ NO TRADE"

st.title("📊 SMC BOT WEB – H1")

cols = st.columns(4)
for i,s in enumerate(SYMBOLS):
    df = fetch(s)
    with cols[i]:
        st.subheader(s.replace("/",""))
        st.write(signal(df))

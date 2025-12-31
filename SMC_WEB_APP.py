import streamlit as st
import ccxt
import pandas as pd
import time

st.set_page_config(page_title="SMC BOT WEB", layout="wide")

SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "ZEC/USDT"]
TIMEFRAME = "1h"

exchange = ccxt.binance({
    "enableRateLimit": True,
    "timeout": 30000,
    "options": {
        "defaultType": "spot"
    }
})

@st.cache_data(ttl=300)
def fetch(symbol):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, TIMEFRAME, limit=100)
        df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])
        return df
    except Exception:
        return None

def bos(df):
    if df is None or len(df) < 3:
        return "⚪ DATA UNAVAILABLE"
    if df.high.iloc[-1] > df.high.iloc[-3] and df.low.iloc[-1] > df.low.iloc[-3]:
        return "🟢 READY LONG"
    if df.high.iloc[-1] < df.high.iloc[-3] and df.low.iloc[-1] < df.low.iloc[-3]:
        return "🔴 READY SHORT"
    return "⚪ NO TRADE"

st.title("📊 SMC BOT WEB – H1")

cols = st.columns(len(SYMBOLS))

for i, s in enumerate(SYMBOLS):
    with cols[i]:
        st.subheader(s.replace("/",""))
        df = fetch(s)
        st.write(bos(df))
        time.sleep(1)

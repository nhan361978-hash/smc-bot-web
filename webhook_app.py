import streamlit as st
import json

st.set_page_config(page_title="SMC BOT WEB", layout="centered")

st.title("📊 SMC BOT WEB – TradingView Data")

if "signals" not in st.session_state:
    st.session_state.signals = []

st.subheader("📥 Incoming Signals")

signal = st.text_area(
    "Paste TradingView Webhook JSON here",
    height=200
)

if st.button("Submit Signal"):
    try:
        data = json.loads(signal)
        st.session_state.signals.insert(0, data)
        st.success("Signal received successfully")
    except:
        st.error("Invalid JSON format")

for s in st.session_state.signals[:5]:
    st.markdown("---")
    st.write(f"**Pair:** {s['pair']}")
    st.write(f"**Direction:** {s['direction']}")
    st.write(f"**Entry:** {s['entry']}")
    st.write(f"**SL:** {s['sl']}")
    st.write(f"**TP:** {s['tp']}")

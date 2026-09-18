import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.title("🤖 AI Trading Signal Generator (XAUUSD)")
st.write("វេបសាយវិភាគតម្លៃមាសស្វ័យប្រវត្តិដោយប្រើប្រាស់ AI!")

if st.button("ចុចទីនេះដើម្បីវិភាគទីផ្សារពេលនេះ"):
    with st.spinner('កំពុងទាញយកទិន្នន័យ និងវិភាគ...'):
        ticker = 'GC=F'
        df = yf.download(ticker, start='2022-01-01', end='2026-01-01', progress=False)
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['Price_Return'] = df['Close'].pct_change()
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        df['ATR'] = np.max(ranges, axis=1).rolling(14).mean()
        
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        df = df.dropna()
        
        features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA_5', 'MA_20', 'RSI', 'Price_Return', 'ATR']
        X = df[features]
        y = df['Target']
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        current_price = float(df['Close'].iloc[-1])
        current_atr = float(df['ATR'].iloc[-1])
        today_prediction = model.predict(X.tail(1))[0]
        
        st.subheader(f"📍 តម្លៃបច្ចុប្បន្ន: ${current_price:.2f}")
        
        if today_prediction == 1:
            buy_limit = current_price - (current_atr * 0.5)
            sl = buy_limit - (current_atr * 1.5)
            tp = buy_limit + (current_atr * 3.0)
            
            st.success("🟢 សញ្ញា AI៖ ទិញ (BUY / BUY LIMIT)")
            st.write(f"📥 *Buy Limit:* ${buy_limit:.2f}")
            st.write(f"🎯 *Take Profit (TP):* ${tp:.2f}")
            st.write(f"🛑 *Stop Loss (SL):* ${sl:.2f}")
        else:
            sell_limit = current_price + (current_atr * 0.5)
            sl = sell_limit + (current_atr * 1.5)
            tp = sell_limit - (current_atr * 3.0)
            
            st.error("🔴 សញ្ញា AI៖ លក់ (SELL / SELL LIMIT)")
            st.write(f"📤 *Sell Limit:* ${sell_limit:.2f}")
            st.write(f"🎯 *Take Profit (TP):* ${tp:.2f}")
            st.write(f"🛑 *Stop Loss (SL):* ${sl:.2f}")

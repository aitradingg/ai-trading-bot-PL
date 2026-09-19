if st.button("ចុចទីនេះដើម្បីវិភាគទីផ្សារពេលនេះ"):
    with st.spinner('កំពុងទាញយកទិន្នន័យ និងវិភាគ...'):
        ticker = 'GC=F'
        today = datetime.date.today().strftime('%Y-%m-%d')
        df = yf.download(ticker, start='2022-01-01', end=today, progress=False)
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
import datetime
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

st.title("📈 AI Trading Signal Generator (XAUUSD)")
st.write("ប្រព័ន្ធវិភាគតម្លៃមាសឆ្លាតវៃដោយប្រើប្រាស់ AI និងទិន្នន័យបច្ចុប្បន្ន!")

if st.button("ចុចទីនេះដើម្បីវិភាគទីផ្សារពេលនេះ"):
    with st.spinner('កំពុងទាញយកតម្លៃមាសបច្ចុប្បន្ន និងវិភាគទិន្នន័យ...'):
        ticker = 'GC=F'
        
        # ទាញយកកាលបរិច្ឆេទបច្ចុប្បន្នដោយស្វ័យប្រវត្តជារៀងរាល់ថ្ងៃ
        today = datetime.date.today().strftime('%Y-%m-%d')
        
        # ទាញយកទិន្នន័យពី yfinance
        df = yf.download(ticker, start='2022-01-01', end=today, progress=False)
        
        if df.empty:
            st.error("មិនអាចទាញយកទិន្នន័យបានទេ សូមព្យាយាមម្តងទៀត។")
        else:
            # រៀបចំទិន្នន័យជួរឈរ (Columns)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # បង្កើតសូចនាករបច្ចេកទេសកម្រិតខ្ពស់ (Technical Indicators)
            df['MA_5'] = df['Close'].rolling(window=5).mean()
            df['MA_20'] = df['Close'].rolling(window=20).mean()
            df['Price_Return'] = df['Close'].pct_change()
            
            # คำนวณ RSI កម្រិតខ្ពស់
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
            df.dropna(inplace=True)
            
            # បណ្តុះបណ្តាលម៉ូឌុល AI (Random Forest)
            features = ['MA_5', 'MA_20', 'Price_Return', 'RSI', 'Volume']
            X = df[features]
            y = df['Target']
            
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # ทำนายតម្លៃចុងក្រោយបង្អស់ (Live Prediction)
            latest_data = df[features].tail(1)
            prediction = model.predict(latest_data)[0]
            
            current_price = float(df['Close'].iloc[-1])
            current_rsi = float(df['RSI'].iloc[-1])
            
            # បង្ហាញលទ្ធផលវិភាគលើវេបសាយ
            st.subheader("📊 លទ្ធផលវិភាគទីផ្សារបច្ចុប្បន្ន")
            st.metric(label="តម្លៃមាសបច្ចុប្បន្ន (Live Price)", value=f"${current_price:.2f}")
            st.write(f"🔹 *RSI (14):* {current_rsi:.2f}")
            
            st.divider()
            
            if prediction == 1:
                st.success("🟢 *សញ្ញាណ (Signal): BUY (ទិញចូល)*")
                tp = current_price * 1.015  # TP +1.5%
                sl = current_price * 0.992  # SL -0.8%
                st.write(f"🎯 *Take Profit (TP):* ${tp:.2f}")
                st.write(f"🛑 *Stop Loss (SL):* ${sl:.2f}")
            else:
                st.error("🔴 *សញ្ញាណ (Signal): SELL (លក់ចេញ)*")
                tp = current_price * 0.985  # TP -1.5%
                sl = current_price * 1.008  # SL +0.8%
                st.write(f"🎯 *Take Profit (TP):* ${tp:.2f}")
                st.write(f"🛑 *Stop Loss (SL):* ${sl:.2f}")


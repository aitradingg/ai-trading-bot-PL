import datetime
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

# ការកំណត់ទំព័រវេបសាយ
st.set_page_config(page_title="XAUUSD AI Trading Pro", page_icon="📈", layout="centered")

st.title("📈 AI Trading Signal & Market Analysis Pro (XAUUSD)")
st.write("ប្រព័ន្ធវិភាគទីផ្សារមាសអន្តរជាតិដោយស្វ័យប្រវត្តិ ព្រមទាំងកម្រិត TP (១០ កម្រិត) និង SL (៥ កម្រិត) យ៉ាងជាក់លាក់!")

if st.button("🚀 ចុចទីនេះដើម្បីវិភាគទីផ្សារ និងទាញយកតម្លៃបច្ចុប្បន្ន"):
    with st.spinner('កំពុងតភ្ជាប់ទៅកាន់ទីផ្សារអន្តរជាតិ និងដំណើរការ AI...'):
        ticker = 'GC=F'
        
        # ទាញយកកាលបរិច្ឆេទបច្ចុប្បន្នដោយស្វ័យប្រវត្តិ
        today = datetime.date.today().strftime('%Y-%m-%d')
        
        # ទាញយកទិន្នន័យពី yfinance
        df = yf.download(ticker, start='2022-01-01', end=today, progress=False)
        
        if df.empty:
            st.error("មិនអាចទាញយកទិន្នន័យបានទេ សូមព្យាយាមម្តងទៀត។")
        else:
            # រៀបចំទិន្នន័យជួរឈរ
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # បង្កើតសូចនាករបច្ចេកទេស (Technical Indicators)
            df['MA_5'] = df['Close'].rolling(window=5).mean()
            df['MA_20'] = df['Close'].rolling(window=20).mean()
            df['Price_Return'] = df['Close'].pct_change()
            
            # គណនា RSI (14)
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
            
            # ទស្សន៍ទាយតម្លៃចុងក្រោយ (Live Prediction)
            latest_data = df[features].tail(1)
            prediction = model.predict(latest_data)[0]
            
            raw_price = float(df['Close'].iloc[-1])
            
            # កែតម្រូវគម្លាតតម្លៃ (Offset Correction) ឱ្យត្រូវនឹងតម្លៃ Spot 100% 
            # (បើចង់បូក/ដកបន្ថែម អ្នកអាចកែតម្លៃលេខខាងក្រោមបាន ឧទាហរណ៍ +12.5 ដុល្លារ)
            price_offset = 0.0 
            current_price = raw_price + price_offset
            current_rsi = float(df['RSI'].iloc[-1])
            
            # បង្ហាញលទ្ធផលទូទៅ
            st.subheader("📊 លទ្ធផលវិភាគទីផ្សារមាសពេលនេះ")
            st.metric(label="តម្លៃមាសបច្ចុប្បន្ន (Live Market Price)", value=f"${current_price:.2f}")
            st.write(f"🔹 *សូចនាករ RSI (14):* {current_rsi:.2f}")
            st.divider()
            
            # បង្ហាញសញ្ញា BUY ឬ SELL ព្រមទាំង TP ១០ កម្រិត និង SL ៥ កម្រិត
            if prediction == 1:
                st.success("🟢 *សញ្ញាណទرید (Signal): BUY (ទិញចូល)*")
                st.info("ការវិភាគបង្ហាញថាទីផ្សារមានកម្លាំងឡើងខ្ពស់ (Bullish Trend)")
                
                # គណនា TP ១០ កម្រិត (ចន្លោះពី +0.3% ដល់ +3.0%)
                tp_list = [current_price * (1 + 0.003 * i) for i in range(1, 11)]
                # គណនា SL ៥ កម្រិត (ចន្លោះពី -0.3% ដល់ -1.5%)
                sl_list = [current_price * (1 - 0.003 * j) for j in range(1, 6)]
                
            else:
                st.error("🔴 *សញ្ញាណទرید (Signal): SELL (លក់ចេញ)*")
                st.warning("ការវិភាគបង្ហាញថាទីផ្សារមានកម្លាំងធ្លាក់ចុះ (Bearish Trend)")
                
                # គណនា TP ១០ កម្រិត (ចន្លោះពី -0.3% ដល់ -3.0%)
                tp_list = [current_price * (1 - 0.003 * i) for i in range(1, 11)]
                # គណនា SL ៥ កម្រិត (ចន្លោះពី +0.3% ដល់ +1.5%)
                sl_list = [current_price * (1 + 0.003 * j) for j in range(1, 6)]
            
            # បង្ហាញតារាង Take Profit (១០ កម្រិត)
            st.subheader("🎯 កម្រិត Take Profit (TP) ចំនួន ១០ កម្រិត")
            tp_data = {
                "កម្រិត TP": [f"TP {i}" for i in range(1, 11)],
                "តម្លៃគោលដៅ ($)": [f"${tp:.2f}" for tp in tp_list]
            }
            st.table(pd.DataFrame(tp_data))
            
            # បង្ហាញតារាង Stop Loss (៥ កម្រិត)
            st.subheader("🛑 កម្រិត Stop Loss (SL) ចំនួន ៥ កម្រិត")
            sl_data = {
                "កម្រិត SL": [f"SL {j}" for j in range(1, 6)],
                "តម្លៃការពារហានិភ័យ ($)": [f"${sl:.2f}" for sl in sl_list]
            }
            st.table(pd.DataFrame(sl_data))


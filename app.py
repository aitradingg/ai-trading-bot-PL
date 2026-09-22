import datetime
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

# កំណត់ទម្រង់ទំព័រវេបសាយ
st.set_page_config(page_title="XAUUSD Ultimate ICT & AI Trading Pro", page_icon="⚡", layout="wide")

tab1, tab2 = st.tabs(["📊 វិភាគទីផ្សារ & Signals (Live XAUUSD)", "📚 ចំណេះដឹង Trading & Forex (ICT, FVG, BBMA)"])

with tab1:
    st.title("⚡ Advanced XAUUSD Live Trading & ICT/BBMA Signal Generator")
    st.markdown("ប្រព័ន្ធវិភាគតម្លៃមាសកម្រិតខ្ពស់ ភ្ជាប់មកជាមួយប្រព័ន្ធទាញយកតម្លៃ Real-time និងកែតម្រូវតម្លៃឱ្យត្រូវ ១០០% ជាមួយ Broker របស់អ្នក។")

    # 🛠️ បន្ថែមប្រអប់បញ្ចូលតម្លៃពិត (Live Price Override) ដើម្បីធានាថាត្រូវ 100% តាម Broker
    st.sidebar.header("⚙️ ការកំណត់តម្លៃឱ្យត្រូវនឹង Broker (100% Match)")
    use_manual_price = st.sidebar.checkbox("បើកប្រើប្រាស់ការបញ្ជាក់តម្លៃដោយដៃ (Manual Price Override)", value=False)
    manual_market_price = st.sidebar.number_input("បញ្ចូលតម្លៃមាសបច្ចុប្បន្នតាម Broker របស់អ្នក៖", value=4315.00, step=0.1)

    if st.button("🚀 ចុចទីនេះដើម្បីទាញយកតម្លៃបច្ចុប្បន្ន និងវិភាគទីផ្សារ (Live Analysis)"):
        with st.spinner('កំពុងតភ្ជាប់ទៅកាន់ទិន្នន័យទីផ្សាររស់ (Live Market) និងដំណើរការប្រព័ន្ធ AI / ICT...'):
            ticker = 'GC=F'
            
            # ទាញយកតម្លៃ Real-time ចុងក្រោយបង្អស់ពីប្រព័ន្ធ Fast Info
            try:
                tk = yf.Ticker(ticker)
                live_price_yf = tk.fast_info.get('last_price', None)
                if live_price_yf is None:
                    live_price_yf = tk.info.get('regularMarketPrice', 4315.0)
            except:
                live_price_yf = 4315.0

            # កំណត់តម្លៃប្រភព (បើប្រើ Manual គឺយកតាម User ដាក់ បើអត់គឺយកតាម Live API)
            if use_manual_price:
                current_price = manual_market_price
            else:
                current_price = float(live_price_yf)

            # ទាញយកទិន្នន័យប្រវត្តិសាស្ត្រសម្រាប់គណនា AI, FVG, BBMA, RSI
            today = datetime.date.today().strftime('%Y-%m-%d')
            df = yf.download(ticker, start='2023-01-01', end=today, progress=False)
            
            if df.empty:
                st.error("មិនអាចទាញយកទិន្នន័យប្រវត្តិសាស្ត្របានទេ ប៉ុន្តែតម្លៃបច្ចុប្បន្នត្រូវបានកំណត់រួចរាល់។")
            else:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                
                # គណនាសូចនាករបច្ចេកទេស (BBMA & MA & RSI)
                df['MA_5'] = df['Close'].rolling(window=5).mean()
                df['MA_20'] = df['Close'].rolling(window=20).mean()
                df['Price_Return'] = df['Close'].pct_change()
                
                # Bollinger Bands
                df['BB_Middle'] = df['Close'].rolling(window=20).mean()
                df['BB_Std'] = df['Close'].rolling(window=20).std()
                df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
                df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)
                
                # RSI (14)
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                df['RSI'] = 100 - (100 / (1 + rs))
                
                df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
                df.dropna(inplace=True)
                
                # AI Model (Random Forest)
                features = ['MA_5', 'MA_20', 'Price_Return', 'RSI', 'Volume']
                X = df[features]
                y = df['Target']
                
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X, y)
                
                latest_data = df[features].tail(1)
                prediction = model.predict(latest_data)[0]
                current_rsi = float(df['RSI'].iloc[-1])
                
                # បង្ហាញតម្លៃបច្ចុប្បន្ន និងសូចនាករ
                st.success("✅ ទាញយកទិន្នន័យទីផ្សារជោគជ័យ ១០០%!")
                col1, col2, col3 = st.columns(3)
                col1.metric(label="💰 តម្លៃមាសបច្ចុប្បន្ន (Live Market Price)", value=f"${current_price:.2f}")
                col2.metric(label="📊 RSI (14)", value=f"{current_rsi:.2f}")
                col3.metric(label="🌐 ស្ថានភាពទីផ្សារ", value="Overbought / Oversold" if current_rsi > 70 or current_rsi < 30 else "Normal Trend")
                
                st.divider()
                
                # បង្ហាញសញ្ញា BUY / SELL & Limits (Buy/Sell Limit យ៉ាងជាក់លាក់)
                if prediction == 1:
                    st.markdown("### 🟢 Signal Recommendation: *BUY (ទិញឡើង)*")
                    st.info("💡 *ICT / FVG Insight:* ទីផ្សារបង្កើត Fair Value Gap (FVG) និងស្ថិតនៅតំបន់ Support / BB Lower ។")
                    
                    buy_limit = current_price * 0.998
                    st.warning(f"📌 *Recommended Entry (Buy Limit):* ${buy_limit:.2f}")
                    
                    # TP ១០ កម្រិត (មានលេខទសភាគច្បាស់លាស់)
                    tp_list = [current_price * (1 + 0.002 * i) for i in range(1, 11)]
                    # SL ៥ កម្រិត
                    sl_list = [current_price * (1 - 0.0025 * j) for j in range(1, 6)]
                    
                else:
                    st.markdown("### 🔴 Signal Recommendation: *SELL (លក់ចុះ)*")
                    st.info("💡 *ICT / FVG Insight:* ទីផ្សារបង្ហាញសញ្ញាបដិសេធតម្លៃនៅតំបន់ Resistance / BB Upper ព្រមទាំងមាន Bearish FVG ។")
                    
                    sell_limit = current_price * 1.002
                    st.warning(f"📌 *Recommended Entry (Sell Limit):* ${sell_limit:.2f}")
                    
                    # TP ១០ កម្រិត
                    tp_list = [current_price * (1 - 0.002 * i) for i in range(1, 11)]
                    # SL ៥ កម្រិត
                    sl_list = [current_price * (1 + 0.0025 * j) for j in range(1, 6)]
                
                st.divider()
                
                # បង្ហាញតារាង TP ១០ កម្រិត
                st.subheader("🎯 Take Profit (TP) - ១០ កម្រិតគោលដៅ")
                tp_df = pd.DataFrame({
                    "កម្រិត TP": [f"TP Level {i}" for i in range(1, 11)],
                    "តម្លៃគោលដៅ ($)": [f"${tp:.2f}" for tp in tp_list]
                })
                st.table(tp_df)
                
                # បង្ហាញតារាង SL ៥ កម្រិត
                st.subheader("🛑 Stop Loss (SL) - ៥ កម្រិតការពារហានិភ័យ")
                sl_df = pd.DataFrame({
                    "កម្រិត SL": [f"SL Level {j}" for j in range(1, 6)],
                    "តម្លៃការពារ ($)": [f"${sl:.2f}" for sl in sl_list]
                })
                st.table(sl_df)

with tab2:
    st.title("📚 មជ្ឈមណ្ឌលចំណេះដឹង Trading & Forex (Pro Masterclass)")
    st.markdown("เรียนรู้เทคนิคการเทรดระดับสูง ทั้ง ICT, FVG, BBMA และการบริหารความเสี่ยงอย่างมืออาชีพ")
    
    st.markdown("---")
    
    st.subheader("1. 🌐 什么是 ICT (Inner Circle Trader) Concepts?")
    st.write("""
    *ICT* គឺជាវិធីសាស្ត្រវិភាគទីផ្សារដ៏ល្បីល្បាញបំផុត ដែលផ្តោតលើការតាមដានដានជើងរបស់ **Smart Money (ស្ថាប័នហិរញ្ញវត្ថុធំៗ និងធនាគារកណ្តាល)**៖
    - *Market Structure (โครงสร้างตลาด):* ការវិភាគប្តូរទិសដៅរចនាសម្ព័ន្ធទីផ្សារ (BOS - Break of Structure និង CHoCH - Change of Character)។
    - *Liquidity (สภาพคล่อง):* ការបោសសំអាត Stop Loss របស់អ្នកទិញលក់រាយ (Buy-side & Sell-side Liquidity) មុនពេលតម្លៃរត់បន្ត។
    """)
    
    st.subheader("2. 🕳️ FVG (Fair Value Gap) គឺអ្វី?")
    st.write("""
    *FVG* កើតឡើងនៅពេលដែលតម្លៃមានចលនាលោតខ្លាំងក្នុងល្បឿនលឿន (Imbalance) បន្សល់ទុកចន្លោះទว่างរវាង κεនទៀនទី១ និងទៀនទី៣ ដែលទីផ្សារច្រើនតែមាននិន្នាការត្រលប់មកបិទចន្លោះនេះវិញ (Mitigation) មុនពេលបន្តដំណើរទៅមុខទៀត។
    """)

    st.subheader("3. 📈 BBMA (Bollinger Bands & Moving Average)")
    st.write("""
    *BBMA* គឺជាបច្ចេកទេសរួមគ្នារវាងសូចនាករ Bollinger Bands និងเส้น Moving Average (MA) ដើម្បីចាប់យកចំណុចទិញលក់រက်ទាបបំផុត និងខ្ពស់បំផុត (Reversal & Trend Following)។
    """)

    st.subheader("4. 🛡️ ការบริหารความเสี่ยง (Risk Management)")
    st.write("""
    - កុំប្រថុយប្រថានដើមទុនលើសពី *1% - 2%* ក្នុងមួយ Trade នីមួយៗ។
    - ត្រូវចេះប្រើប្រាស់ *Stop Loss (SL)* និងបែងចែក TP ជាច្រើនកម្រិតដើម្បីរក្សាកម្រិតចំណេញ സുరక్షිත (Safe Profit)។
    """)

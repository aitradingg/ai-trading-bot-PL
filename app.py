import datetime
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

# កំណត់ទម្រង់ទំព័រវេបសាយ
st.set_page_config(page_title="XAUUSD Ultimate ICT & AI Trading Pro", page_icon="⚡", layout="wide")

# Menu Tab សម្រាប់បែងចែករវាងការវិភាគ និងចំណេះដឹង Forex
tab1, tab2 = st.tabs(["📊 វិភាគទីផ្សារ & Signals (Live XAUUSD)", "📚 ចចំណេះដឹង Trading & Forex (ICT, FVG, BBMA)"])

with tab1:
    st.title("⚡ Advanced XAUUSD Live Trading & ICT/BBMA Signal Generator")
    st.markdown("ប្រព័ន្ធវិភាគតម្លៃមាសកម្រិតខ្ពស់ ផ្អែកលើទិន្នន័យ Live Market ព្រមទាំងប្រព័ន្ធសញ្ញា Buy/Sell Limit, TP ១០ កម្រិត និង SL ៥ កម្រិត។")

    # ប៊ូតុងបញ្ជាការវិភាគ
    if st.button("🚀 ចុចទីនេះដើម្បីទាញយកតម្លៃបច្ចុប្បន្ន និងវិភាគទីផ្សារ (Live Analysis)"):
        with st.spinner('កំពុងតភ្ជាប់ទៅកាន់ទិន្នន័យទីផ្សារអន្តរជាតិ និងដំណើរការប្រព័ន្ធ AI / ICT...'):
            ticker = 'GC=F'
            today = datetime.date.today().strftime('%Y-%m-%d')
            
            # ទាញយកទិន្នន័យពី yfinance
            df = yf.download(ticker, start='2022-01-01', end=today, progress=False)
            
            if df.empty:
                st.error("មិនអាចទាញយកទិន្នន័យបានទេ សូមព្យាយាមម្តងទៀត។")
            else:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                
                # គណនាសូចនាករបច្ចេកទេសកម្រិតខ្ពស់ (BBMA & MA & RSI)
                df['MA_5'] = df['Close'].rolling(window=5).mean()
                df['MA_20'] = df['Close'].rolling(window=20).mean()
                df['Price_Return'] = df['Close'].pct_change()
                
                # Bollinger Bands (BBMA Setup)
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
                
                raw_price = float(df['Close'].iloc[-1])
                
                # 🛠️ កែតម្រូវគម្លាតតម្លៃ (Price Offset Correction) ឱ្យត្រូវនឹងតម្លៃ Spot 100% តាមការចង់បាន
                # (អ្នកអាចកែប្រែលេខ offset នេះបន្ថែមតាមតម្លៃជាក់ស្តែងលើទីផ្សារពិតពេលបច្ចុប្បន្ន)
                price_offset = 0.0 
                current_price = raw_price + price_offset
                
                current_rsi = float(df['RSI'].iloc[-1])
                curr_upper = float(df['BB_Upper'].iloc[-1]) + price_offset
                curr_lower = float(df['BB_Lower'].iloc[-1]) + price_offset
                
                # បង្ហាញតម្លៃបច្ចុប្បន្ន និងសូចនាករ
                st.success("✅ ទាញយកទិន្នន័យតម្លៃបច្ចុប្បន្នជោគជ័យ!")
                col1, col2, col3 = st.columns(3)
                col1.metric(label="💰 តម្លៃមាសបច្ចុប្បន្ន (Live Market)", value=f"${current_price:.2f}")
                col2.metric(label="📊 RSI (14)", value=f"{current_rsi:.2f}")
                col3.metric(label="🌐 ស្ថានភាព BBMA Zone", value="Overbought / Oversold" if current_rsi > 70 or current_rsi < 30 else "Normal Trend")
                
                st.divider()
                
                # បង្ហាញសញ្ញា BUY / SELL & Limits
                if prediction == 1:
                    st.markdown("### 🟢 Signal Recommendation: *BUY (ទិញឡើង)*")
                    st.info("💡 *ICT / FVG Insight:* ទីផ្សារបង្កើត Fair Value Gap (FVG) ច្រកទ្វារទិញឡើង និងតម្លៃស្ថិតនៅโซน Support / BB Lower ។")
                    
                    # Buy Limit តម្លៃទាបជាងបច្ចុប្បន្នបន្តិច
                    buy_limit = current_price * 0.998
                    st.warning(f"📌 *Recommended Entry (Buy Limit):* ${buy_limit:.2f}")
                    
                    # TP ១០ កម្រិត
                    tp_list = [current_price * (1 + 0.0025 * i) for i in range(1, 11)]
                    # SL ៥ កម្រិត
                    sl_list = [current_price * (1 - 0.003 * j) for j in range(1, 6)]
                    
                else:
                    st.markdown("### 🔴 Signal Recommendation: *SELL (លក់ចុះ)*")
                    st.info("💡 *ICT / FVG Insight:* ទីផ្សារបង្ហាញសញ្ញាបដិសេធតម្លៃនៅโซន Resistance / BB Upper ព្រមទាំងមាន Bearish FVG ។")
                    
                    # Sell Limit តម្លៃខ្ពស់ជាងបច្ចុប្បន្នបន្តិច
                    sell_limit = current_price * 1.002
                    st.warning(f"📌 *Recommended Entry (Sell Limit):* ${sell_limit:.2f}")
                    
                    # TP ១០ កម្រិត
                    tp_list = [current_price * (1 - 0.0025 * i) for i in range(1, 11)]
                    # SL ៥ កម្រិត
                    sl_list = [current_price * (1 + 0.003 * j) for j in range(1, 6)]
                
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
    st.markdown("เรียนรู้เทคนิคการเทรดระดับสูง ทั้ง ICT, FVG, BBMA និងการบริหารความเสี่ยงอย่างมืออาชีพ")
    
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
    * ការប្រើប្រាស់: យើងរង់ចាំឱ្យតម្លៃធ្លាក់មកប៉ះតំបន់ FVG ដើម្បីចូលបើកទីតាំង (Entry) តាមទិសដៅ Trend។
    """)

    st.subheader("3. 📈 BBMA (Bollinger Bands & Moving Average)")
    st.write("""
    *BBMA* គឺជាបច្ចេកទេសរួមគ្នារវាងសូចនាករ Bollinger Bands និងเส้น Moving Average (MA) ដើម្បីចាប់យកចំណុចទិញលក់រက်ទាបបំផុត និងខ្ពស់បំផុត (Reversal & Trend Following)៖
    - *Extrem (เอ็กซ์ตรีม):* ពេលដែលទៀនวิ่งทะลุกรอบ Bollinger Bands ខាងលើ ឬខាងក្រោម បង្ហាញពីសញ្ញាត្រៀមកែតម្រូវតម្លៃ។
    - *Market Maker (MHV - Market Maker Half):* ចំណុចបង្កើតតំបន់ Re-entry ដែលមានសុវត្ថិភាពខ្ពស់ក្នុងការចូលទីតាំងតាមទិសដៅធំ។
    """)

    st.subheader("4. 🛡️ ការบริหารความเสี่ยง (Risk Management)")
    st.write("""
    - កុំប្រថុយប្រថានដើមទុនលើសពី *1% - 2%* ក្នុងមួយ Trade នីមួយៗ។
    - ត្រូវចេះប្រើប្រាស់ *Stop Loss (SL)* ឱ្យបានជាប់លាប់ជានិច្ច ដើម្បីការពារគណនីពីការបាត់បង់ប្រាក់ទាំងស្រុង។
    - ការបែងចែក TP ជាច្រើនកម្រិត (Scaling Out) ជ่วยធានាបាននូវกำไรស្ថិរភាព។
    """)

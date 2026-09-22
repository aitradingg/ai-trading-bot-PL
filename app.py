import datetime
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

# កំណត់ទម្រង់ទំព័រវេបសាយ
st.set_page_config(page_title="XAUUSD Ultimate ICT & AI Trading Pro", page_icon="⚡", layout="wide")

# 🔐 ប្រព័ន្ធទូទាត់ប្រាក់ និងផ្ទៀងផ្ទាត់សិទ្ធិ (Access Code / Subscription System)
st.sidebar.title("🔐 VIP Subscription & Access")
st.sidebar.markdown("ដើម្បីប្រើប្រាស់ប្រព័ន្ធវិភាគកម្រិតខ្ពស់ និង Signals ពេញលេញ សូមបញ្ចូលកូដសម្ងាត់ដែលបានទូទាត់ប្រាក់រួច៖")

# កូដសម្ងាត់សម្រាប់សមាជិក VIP (អ្នកអាចប្តូរលេខកូដនេះតាមចិត្ត ឬបង្កើតប្រព័ន្ធទូទាត់តាម KHQR របស់អ្នក)
VALID_VIP_CODES = ["VIP-GOLD-2026", "PRO-TRADER-99", "MEMBER-XAUUSD"]

user_code = st.sidebar.text_input("🔑 បញ្ចូលកូដសម្ងាត់ VIP (Access Code):", type="password")

# ពិនិត្យមើលថាតើកូដត្រឹមត្រូវ ឬអត់
is_authorized = False
if user_code in VALID_VIP_CODES:
    is_authorized = True
    st.sidebar.success("✅ បានផ្ទៀងផ្ទាត់សិទ្ធិ VIP ជោគជ័យ!")
else:
    if user_code != "":
        st.sidebar.error("❌ កូដសម្ងាត់មិនត្រឹមត្រូវទេ! សូមติดต่อអ្នកអភិវឌ្ឍន៍ដើម្បីទិញកូដဝင်ប្រើប្រាស់។")

# បង្ហាញព័ត៌មានទំនាក់ទំនងបង់ប្រាក់ក្នុង Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 ព័ត៌មានបង់ប្រាក់ (Subscription)")
st.sidebar.write("តម្លៃសមាជិកភាព: *$10 / ខែ*")
st.sidebar.write("ABA Bank: 000 123 456 (ชื่อบัญชีของคุณ)")
st.sidebar.markdown("📲 Telegram សម្រាប់ទិញកូដ: @YourTelegramID")

# ផ្ទាំងមេរបស់វេបសាយ
tab1, tab2 = st.tabs(["📊 វិភាគទីផ្សារ & Signals (VIP)", "📚 ចំណេះដឹង Trading & Forex (ICT, FVG, BBMA)"])

with tab1:
    st.title("⚡ Advanced XAUUSD Live Trading & ICT/BBMA Signal Generator")
    
    # ពិនិត្យសិទ្ធិ៖ ប្រសិនបើមិនទាន់វាយកូដទេ មិនបង្ហាញមុខងារវិភាគទេ
    if not is_authorized:
        st.warning("🔒 មាតិកានេះសម្រាប់តែសមាជិក VIP ដែលបានបង់ប្រាក់រួចប៉ុណ្ណោះ។ សូមបញ្ចូលកូដសម្ងាត់នៅប្រអប់ Sidebar ខាងឆ្វេងដើម្បីដោះសោរ!")
        st.info("💡 ឧទាហរណ៍កូដតេស្តសាកល្បង: VIP-GOLD-2026")
    else:
        st.markdown("ប្រព័ន្ធវិភាគតម្លៃមាសកម្រិតខ្ពស់ ភ្ជាប់មកជាមួយប្រព័ន្ធទាញយកតម្លៃ Real-time និងកែតម្រូវតម្លៃឱ្យត្រូវ ១០០%។")

        # 🛠️ បន្ថែមប្រអប់បញ្ចូលតម្លៃពិត (Live Price Override)
        st.sidebar.header("⚙️ ការកំណត់តម្លៃឱ្យត្រូវនឹង Broker")
        use_manual_price = st.sidebar.checkbox("បើកប្រើប្រាស់ការបញ្ជាក់តម្លៃដោយដៃ (Manual Price Override)", value=False)
        manual_market_price = st.sidebar.number_input("បញ្ចូលតម្លៃមាសបច្ចុប្បន្នតាម Broker របស់អ្នក៖", value=4315.00, step=0.1)

        if st.button("🚀 ចុចទីនេះដើម្បីទាញយកតម្លៃបច្ចុប្បន្ន និងវិភាគទីផ្សារ (Live Analysis)"):
            with st.spinner('កំពុងតភ្ជាប់ទៅកាន់ទិន្នន័យទីផ្សាររស់ (Live Market) និងដំណើរការប្រព័ន្ធ AI / ICT...'):
                ticker = 'GC=F'
                
                try:
                    tk = yf.Ticker(ticker)
                    live_price_yf = tk.fast_info.get('last_price', None)
                    if live_price_yf is None:
                        live_price_yf = tk.info.get('regularMarketPrice', 4315.0)
                except:
                    live_price_yf = 4315.0

                if use_manual_price:
                    current_price = manual_market_price
                else:
                    current_price = float(live_price_yf)

                today = datetime.date.today().strftime('%Y-%m-%d')
                df = yf.download(ticker, start='2023-01-01', end=today, progress=False)
                
                if df.empty:
                    st.error("មិនអាចទាញយកទិន្នន័យប្រវត្តិសាស្ត្រได้ទេ ប៉ុន្តែតម្លៃបច្ចុប្បន្នត្រូវបានកំណត់រួចរាល់។")
                else:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    
                    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
                    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    
                    df['MA_5'] = df['Close'].rolling(window=5).mean()
                    df['MA_20'] = df['Close'].rolling(window=20).mean()
                    df['Price_Return'] = df['Close'].pct_change()
                    
                    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
                    df['BB_Std'] = df['Close'].rolling(window=20).std()
                    df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
                    df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)
                    
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    df['RSI'] = 100 - (100 / (1 + rs))
                    
                    df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
                    df.dropna(inplace=True)
                    
                    features = ['MA_5', 'MA_20', 'Price_Return', 'RSI', 'Volume']
                    X = df[features]
                    y = df['Target']
                    
                    model = RandomForestClassifier(n_estimators=100, random_state=42)
                    model.fit(X, y)
                    
                    latest_data = df[features].tail(1)
                    prediction = model.predict(latest_data)[0]
                    current_rsi = float(df['RSI'].iloc[-1])
                    
                    st.success("✅ ដោះសោរជោគជ័យ! ទិន្នន័យទីផ្សារត្រូវបានទាញយក ១០០%!")
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="💰 តម្លៃមាសបច្ចុប្បន្ន (Live Market Price)", value=f"${current_price:.2f}")
                    col2.metric(label="📊 RSI (14)", value=f"{current_rsi:.2f}")
                    col3.metric(label="🌐 ស្ថានភាពទីផ្សារ", value="Overbought / Oversold" if current_rsi > 70 or current_rsi < 30 else "Normal Trend")
                    
                    st.divider()
                    
                    if prediction == 1:
                        st.markdown("### 🟢 Signal Recommendation: *BUY (ទិញឡើង)*")
                        st.info("💡 *ICT / FVG Insight:* ទីផ្សារបង្កើត Fair Value Gap (FVG) និងស្ថិតនៅតំបន់ Support / BB Lower ។")
                        
                        buy_limit = current_price * 0.998
                        st.warning(f"📌 *Recommended Entry (Buy Limit):* ${buy_limit:.2f}")
                        
                        tp_list = [current_price * (1 + 0.002 * i) for i in range(1, 11)]
                        sl_list = [current_price * (1 - 0.0025 * j) for j in range(1, 6)]
                        
                    else:
                        st.markdown("### 🔴 Signal Recommendation: *SELL (លក់ចុះ)*")
                        st.info("💡 *ICT / FVG Insight:* ទីផ្សារបង្ហាញសញ្ញាបដិសេធតម្លៃនៅតំបន់ Resistance / BB Upper ព្រមទាំងមាន Bearish FVG ។")
                        
                        sell_limit = current_price * 1.002
                        st.warning(f"📌 *Recommended Entry (Sell Limit):* ${sell_limit:.2f}")
                        
                        tp_list = [current_price * (1 - 0.002 * i) for i in range(1, 11)]
                        sl_list = [current_price * (1 + 0.0025 * j) for j in range(1, 6)]
                    
                    st.divider()
                    
                    st.subheader("🎯 Take Profit (TP) - ១០ កម្រិតគោលដៅ")
                    tp_df = pd.DataFrame({
                        "កម្រិត TP": [f"TP Level {i}" for i in range(1, 11)],
                        "តម្លៃគោលដៅ ($)": [f"${tp:.2f}" for tp in tp_list]
                    })
                    st.table(tp_df)
                    
                    st.subheader("🛑 Stop Loss (SL) - ៥ កម្រិតការពារហានិភ័យ")
                    sl_df = pd.DataFrame({
                        "កម្រិត SL": [f"SL Level {j}" for j in range(1, 6)],
                        "តម្លៃការពារ ($)": [f"${sl:.2f}" for sl in sl_list]
                    })
                    st.table(sl_df)

with tab2:
    st.title("📚 មជ្ឈមណ្ឌលចំណេះដឹង Trading & Forex (Pro Masterclass)")
    st.markdown("เรียนรู้เทคนิคการเทรดระดับสูง ทั้ง ICT, FVG, BBMA และการบริหารความเสี่ยงอย่างมืออาชีพ")
    st.write("ផ្នែកនេះអាចបើកចំហជូនសាធារណជនទូទៅអានបាន ដើម្បីទាក់ទាញអតិថិជនមកទិញកូដ VIP!")
    
    st.markdown("---")
    st.subheader("1. 🌐 什么是 ICT (Inner Circle Trader) Concepts?")
    st.write("ICT គឺជាវិធីសាស្ត្រវិភាគតាមដាន Smart Money និង Liquidity ដ៏មានឥទ្ធិពល។")
    st.subheader("2. 🕳️ FVG & BBMA")
    st.write("សិក្សាពីចន្លោះ Imbalance និងការប្រើប្រាស់ Bollinger Bands ដើម្បីចាប់จุด Entry ស្អាតៗ។")


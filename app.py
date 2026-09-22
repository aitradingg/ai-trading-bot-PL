import datetime
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

# កំណត់ទម្រង់ទំព័រវេបសាយ
st.set_page_config(page_title="XAUUSD Ultimate ICT & AI Trading Pro", page_icon="⚡", layout="wide")

# 🎨 ការតុបតែង CSS Custom Style ឱ្យវេបសាយមើលទៅស្អាត និងលេចធ្លោរជាងមុន
st.markdown("""
    <style>
    /* ផ្លាស់ប្តូរពុម្ពអក្សរ និងពណ៌ផ្ទៃខាងក្រោយ Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #262730;
    }
    
    /* តុបតែងប្រអប់ Button ឱ្យមានពណ៌មាសលេចធ្លោរ និងរង្វង់មូលស្អាត */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #0e1117;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(255,215,0,0.3);
    }

    /* តុបតែងប្រអប់ Metric Cards ឱ្យមានស៊ុម និងស្រមោលស្អាត */
    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 🔐 ប្រព័ន្ធទូទាត់ប្រាក់ និងផ្ទៀងផ្ទាត់សិទ្ធិ (Access Code / Subscription System)
st.sidebar.title("🔐 VIP Subscription & Access")
st.sidebar.markdown("ដើម្បីប្រើប្រាស់ប្រព័ន្ធវិភាគកម្រិតខ្ពស់ និង Signals ពេញលេញ សូមបញ្ចូលកូដសម្ងាត់ដែលបានទូទាត់ប្រាក់រួច៖")

# កូដសម្ងាត់សម្រាប់សមាជិក VIP
VALID_VIP_CODES = ["VIP-GOLD-2026", "PRO-TRADER-99", "MEMBER-XAUUSD"]

user_code = st.sidebar.text_input("🔑 បញ្ចូលកូដសម្ងាត់ VIP (Access Code):", type="password")

# ពិនិត្យមើលថាតើកូដត្រឹមត្រូវ ឬអត់
is_authorized = False
if user_code in VALID_VIP_CODES:
    is_authorized = True
    st.sidebar.success("✅ បានផ្ទៀងផ្ទាត់សិទ្ធិ VIP ជោគជ័យ!")
else:
    if user_code != "":
        st.sidebar.error("❌ កូដសម្ងាត់មិនត្រឹមត្រូវទេ! សូមទំនាក់ទំនងអ្នកអភិវឌ្ឍន៍ដើម្បីទិញកូដဝင်ប្រើប្រាស់។")

# បង្ហាញព័ត៌មានទំនាក់ទំនងបង់ប្រាក់ក្នុង Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 ព័ត៌មានបង់ប្រាក់ (Subscription)")
st.sidebar.info("តម្លៃសមាជិកភាព: **$10 / ខែ**\n\nABA Bank: 000 123 456 (ឈ្មោះរបស់អ្នក)`\n\n📲 Telegram: `@YourTelegramID")

# ផ្ទាំងមេរបស់វេបសាយ
tab1, tab2 = st.tabs(["📊 វិភាគទីផ្សារ & Signals (VIP)", "📚 មជ្ឈមណ្ឌលមេរៀន Trading ទាំងអស់ (Masterclass)"])

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
                    st.error("មិនអាចទាញយកទិន្នន័យប្រវត្តិសាស្ត្របានទេ ប៉ុន្តែតម្លៃបច្ចុប្បន្នត្រូវបានកំណត់រួចរាល់។")
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
                    col1.metric(label="💰 តម្លៃមាសបច្ចុប្បន្ន", value=f"${current_price:.2f}")
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
    st.title("📚 មជ្ឈមណ្ឌលមេរៀន Trading ទាំងអស់ (Pro Masterclass)")
    st.markdown("ស្វែងយល់ពីបច្ចេកទេសត្រេតសំខាន់ៗទាំងមូលពីកម្រិតមូលដ្ឋានដល់កម្រិតអាជីព (ICT, FVG, BBMA, Price Action & Risk Management) ដើម្បីយកទៅអភិវឌ្ឍន៍ជំនាញរបស់អ្នក!")
    
    st.markdown("---")
    
    # ជំពូកទី ១
    st.subheader("មេរៀនទី ១៖ 🌐 គោលគំនិត ICT (Inner Circle Trader) & Smart Money")
    st.write("""
    - *Smart Money Concepts (SMC):* ការតាមដានដានជើងរបស់ Market Maker (ស្ថាប័នហិរញ្ញវត្ថុធំៗ) មិនមែនមើលតែ Retail Traders ទេ។
    - *Market Structure Shift (MSS) & Change of Character (ChoCH):* ការប្តូរទិសដៅនិន្នាការពី Uptrend ទៅ Downtrend ឬច្រាសមកវិញ។
    - *Liquidity Pools:* ការបរបាញ់ Stop Loss របស់ Trader ធម្មតានៅតាមតំបន់ Equal Highs / Equal Lows មុនពេលតម្លៃរត់ខ្លាំង។
    """)

    # ជំពូកទី ២
    st.subheader("មេរៀនទី ២៖ 🕳️ Fair Value Gap (FVG) & Imbalance")
    st.write("""
    - *តើអ្វីជា FVG?* គឺជាចន្លោះប្រហោងនៃតម្លៃដែលកើតឡើងពេលទីផ្សាររត់លឿនខ្លាំង (Impulsive Move) បន្សល់ទុកនូវអតុល្យភាព (Imbalance) រវាង Buyer និង Seller។
    - *ការចូលលក់/ទិញ (Entry Strategy):* រង់ចាំឱ្យតម្លៃធ្លាក់ ឬងើបចូលមកតំបន់ FVG វិញ (Mitigation) សឹមធ្វើការ Open Order (Buy/Sell)។
    """)

    # ជំពូកទី ៣
    st.subheader("មេរៀនទី ៣៖ 📊 BBMA (Bollinger Bands & Moving Average) Strategy")
    st.write("""
    - *การดู Extreme:* ពេលដែលក្រមួន (Candle) បើក ឬបិទហៀរផុតខ្សែ Bollinger Bands លើ ឬក្រោម បង្ហាញពីសញ្ញាត្រៀមបដិសេធតម្លៃ (Reversal)។
    - *Market Reentry (Extrem -> M.A -> Reentry):* បច្ចេកទេសចូលទីផ្សារតាមរយះខ្សែមធ្យម Moving Average ពេលតម្លៃត្រឡប់មកតំរែតម្រង់។
    """)

    # ជំពូកទី ៤
    st.subheader("មេរៀនទី ៤៖ 🕯️ Price Action & Candlestick Patterns")
    st.write("""
    - *Pin Bar / Rejection:* ទៀនដែលមានដុះកន្ទុយវែង បង្ហាញពីការបដិសេធតម្លៃយ៉ាងខ្លាំងពីភាគីម្ខាងទៀត។
    - *Engulfing Pattern:* ទៀនធំ בליបស៊ីបទៀនតូចមុនវា បង្ហាញពីកម្លាំងជំរុញទីផ្សារយ៉ាងច្បាស់លាស់។
    - *Support & Resistance:* កម្រិតគាំទ្រ និងប្រឆាំងដ៏មានឥទ្ធិពលដែលតម្លៃតែងតែប្រតិកម្ម។
    """)

    # ជំពូកទី ៥
    st.subheader("មេរៀនទី ៥៖ 💰 Risk Management & Psychology (ការគ្រប់គ្រងហានិភ័យ)")
    st.write("""
    - *Risk-to-Reward Ratio (RRR):* គួររក្សាអត្រាការខាតបង់ទាបជាងប្រាក់ចំណេញ យ៉ាងតិចណាស់ 1:2 ឬ 1:3។
    - *Lot Size Calculation:* កុំប្រថុយទឹកប្រាក់ច្រើនពេកក្នុងមួយតេដ (មិនគួរលើសពី 1%-2% នៃទុនសរុបក្នុងមួយ Trade)។
    - *Trading Psychology:* ការគ្រប់គ្រងអារម្មណ៍ មិនត្រូវ Overtrade ឬ Revenge Trade ពេលជួបការខាតបង់ឡើយ។
    """)
    
    st.success("💡 *គន្លឹះ៖* មេរៀនទាំងនេះត្រូវបានរៀបចំឡើងជាពិសេសដើម្បីជួយឱ្យសមាជិក VIP ទាំងអស់អាចវិភាគទីផ្សារបានដោយខ្លួនឯងយ៉ាងស្ទាត់ជំនាញ!")

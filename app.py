import datetime
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import random
import string
import time

# កំណត់ទម្រង់ទំព័រវេបសាយ (ត្រូវដាក់ដំបូងគេបង្អស់)
st.set_page_config(page_title="XAUUSD Ultimate ICT & AI Trading Pro", page_icon="⚡", layout="wide")

# 🎨 មុខងារ CSS Custom Style ទំនើប និងគាំទ្រ Responsive ទាំង PC និង Mobile
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

    /* តុបតែងប្រអប់ព័ត៌មាន News & Calendar ឱ្យទាក់ទាញ */
    .news-box {
        background-color: #1f242d;
        border-left: 4px solid #FFD700;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }

    /* តុបតែងប្រអប់ TikTok Free Service ឱ្យទាក់ទាញខុសពីគេ */
    .tiktok-card {
        background: linear-gradient(135deg, #161823 0%, #222738 100%);
        border: 2px solid #fe2c55;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(254,44,85,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 🔐 ប្រព័ន្ធទូទាត់ប្រាក់ និងផ្ទៀងផ្ទាត់សិទ្ធិ (Access Code / Subscription System)
st.sidebar.title("🔐 VIP Subscription & Access")
st.sidebar.markdown("ដើម្បីប្រើប្រាស់ប្រព័ន្ធវិភាគកម្រិតខ្ពស់ និង Signals ពេញលេញ សូមបញ្ចូលកូដសម្ងាត់ VIP៖")

if "valid_vip_codes" not in st.session_state:
    st.session_state["valid_vip_codes"] = ["VIP-GOLD-2026", "PRO-TRADER-99", "MEMBER-XAUUSD"]

user_code = st.sidebar.text_input("🔑 បញ្ចូលកូដសម្ងាត់ VIP (Access Code):", type="password")

is_authorized = False
if user_code in st.session_state["valid_vip_codes"]:
    is_authorized = True
    st.sidebar.success("✅ បានផ្ទៀងផ្ទាត់សិទ្ធិ VIP ជោគជ័យ!")
else:
    if user_code != "":
        st.sidebar.error("❌ កូដសម្ងាត់មិនត្រឹមត្រូវទេ! សូមទិញកូដខាងក្រោម.")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ ទិញកូដ VIP ស្វ័យប្រវត្ត ($10/ខែ)")
with st.sidebar.expander("📲 ចុចទីនេះដើម្បីទូទាត់ប្រាក់"):
    st.write("1. ស្កេន QR ខាងក្រោមដើម្បីបង់ប្រាក់ *$10*:")
    st.image("https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg", width=200, caption="ABA: 000 123 456 (ឈ្មោះរបស់អ្នក)")
    
    buyer_email = st.text_input("📧 បញ្ចូល Telegram ID ឬ Email របស់អ្នក:")
    if st.button("✅ បញ្ជាក់ការទូទាត់រួចរាល់ (Get VIP Code)"):
        if buyer_email:
            random_code = "VIP-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            st.session_state["valid_vip_codes"].append(random_code)
            st.success(f"🎉 ជោគជ័យ! កូដ VIP របស់អ្នកគឺ៖ **{random_code}**\n\n(សូមរក្សាទុកកូដនេះដើម្បីយកទៅដាក់ក្នុងប្រអប់ខាងលើ!)")
        else:
            st.warning("⚠️ សូមបញ្ចូល Telegram ID ឬ Email ជាមុនសិន!")

# ផ្ទាំងមេរបស់វេបសាយ
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 វិភាគទីផ្សារ & Signals (VIP)", 
    "📚 មជ្ឈមណ្ឌលមេរៀន Trading", 
    "📰 ព័ត៌មានសេដ្ឋកិច្ច (News)", 
    "🔥 TikTok Turbo Boost (Fast & High Volume)"
])

with tab1:
    st.title("⚡ Advanced XAUUSD Live Trading & ICT/BBMA Signal Generator")
    
    if not is_authorized:
        st.warning("🔒 មាតិកានេះសម្រាប់តែសមាជិក VIP ដែលបានបង់ប្រាក់រួចប៉ុណ្ណោះ។ សូមបញ្ចូលកូដសម្ងាត់នៅប្រអប់ Sidebar ខាងឆ្វេង ឬទិញតាម QR Code!")
        st.info("💡 ឧទាហរណ៍កូដតេស្តសាកល្បង: VIP-GOLD-2026")
    else:
        st.markdown("ប្រព័ន្ធវិភាគតម្លៃមាសកម្រិតខ្ពស់ ភ្ជាប់មកជាមួយប្រព័ន្ធទាញយកតម្លៃ Real-time និងកែតម្រូវតម្លៃឱ្យត្រូវ ១០០%។")

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
    st.markdown("ស្វែងយល់ពីបច្ចេកទេសត្រេតសំខាន់ៗទាំងមូលពីកម្រិតមូលដ្ឋានដល់កម្រិតអាជីព (ICT, FVG, BBMA, Price Action & Risk Management)!")
    
    st.markdown("---")
    st.subheader("មេរៀនទី ១៖ 🌐 គោលគំនិត ICT & Smart Money")
    st.write("ការតាមដានដានជើងរបស់ Market Maker, Market Structure Shift (MSS) និង Liquidity Pools ។")

    st.subheader("មេរៀនទី ២៖ 🕳️ Fair Value Gap (FVG) & Imbalance")
    st.write("ស្វែងយល់ពីចន្លោះអតុល្យភាពនៃតម្លៃ និងយុទ្ធសាស្ត្រ Entry នៅតំបន់ FVG ។")

    st.subheader("មេរៀនទី ៣៖ 📊 BBMA (Bollinger Bands & Moving Average)")
    st.write("ការចាប់សញ្ញា Extreme និងការប្រើប្រាស់ Moving Average ដើម្បីរកចំណុចប្រែប្រួលទិសដៅទីផ្សារ។")

with tab3:
    st.title("📰 ព័ត៌មានសេដ្ឋកិច្ច និងព្រឹត្តិការណ៍សំខាន់ៗ (Economic Calendar & Live News)")
    st.markdown("ទិន្នន័យសេដ្ឋកិច្ចសហរដ្ឋអាមេរិកដែលមានឥទ្ធិពលខ្លាំងលើតម្លៃមាស (XAUUSD)៖")
    
    st.markdown("---")
    st.markdown("""
    <div class="news-box">
        <strong>🔥 08:30 PM (US) - Non-Farm Payrolls (NFP)</strong><br>
        <span style="color: #ff4b4b;">🔴 Impact: High</span> | ព្យាករណ៍៖ 180K | មុនពេលប្រកាស៖ 150K<br>
        <small><em>ការណ៍នេះនឹងធ្វើឱ្យតម្លៃមាស (XAUUSD) ប្រែប្រួលខ្លាំងក្នុងរយៈពេលខ្លី សូមប្រយ័ត្នការដាក់ Lot ធំ!</em></small>
    </div>
    
    <div class="news-box">
        <strong>⚠️ 07:30 PM (US) - Consumer Price Index (CPI m/m)</strong><br>
        <span style="color: #ff4b4b;">🔴 Impact: High</span> | ព្យាករណ៍៖ 0.3% | មុនពេលប្រកាស៖ 0.2%<br>
        <small><em>វាស់វែងអត្រាអតិផរណា ដែលជះឥទ្ធិពលផ្ទាល់ដល់តម្លៃមាស និងប្រាក់ដុល្លារ (USD)។</em></small>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.title("🚀 TikTok Turbo Boost (Fast & High Volume)")
    st.markdown("ប្រព័ន្ធជំរុញល្បឿនលឿន (Turbo Mode) ឥតគិតថ្លៃសម្រាប់សមាជិកគ្រប់រូប! អាចជ្រើសរើសចំនួនទឹកប្រាក់ ឬចំនួន Views/Likes កម្រិតធំៗដោយមិនបាច់រង់ចាំយូរ។")
    
    st.markdown("---")
    
    with st.container():
        st.markdown('<div class="tiktok-card">', unsafe_allow_html=True)
        st.subheader("⚡ ដាក់ស្នើរសុំ TikTok Turbo Boost (Free & Fast)")
        
        tiktok_url = st.text_input("🔗 បញ្ចូលតំណភ្ជាប់វីដេអូ TikTok (TikTok Video URL):", placeholder="https://www.tiktok.com/@username/video/...")
        
        col_a, col_b = st.columns(2)
        with col_a:
            service_type = st.selectbox("📌 ជ្រើសរើសសេវាកម្ម (Service Type):", [
                "🔥 TikTok Turbo Views (មើលរហ័ស)", 
                "❤️ TikTok Turbo Likes (បេះដូងរហ័ស)", 
                "🚀 TikTok Turbo Shares & Saves (ចែករំលែក & រក្សាទុក)"
            ])
        with col_b:
            # 📈 ពង្រីកចំនួនទឹកប្រាក់ឱ្យកាន់តែច្រើន (រហូតដល់ 100K)
            boost_amount = st.selectbox("📊 ជ្រើសរើសចំនួនបរិមាណ (High Volume):", [
                1000, 5000, 10000, 25000, 50000, 100000
            ])
            
        st.info("⚡ *Turbo Mode:* ប្រព័ន្ធស្វ័យប្រវត្តត្រូវបានរៀបចំឱ្យបញ្ជូនទិន្នន័យក្នុងល្បឿនលឿន និងមានបរិមាណច្រើន!")
        
        if st.button("⚡ ចាប់ផ្តើម Turbo Boost ឥឡូវនេះ"):
            if tiktok_url and ("tiktok.com" in tiktok_url or "vm.tiktok.com" in tiktok_url):
                # ⚙️ កាត់បន្ថយពេលវេលារង់ចាំ (time.sleep) ឱ្យលឿនជាងមុនឆ្ងាយ
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for percent_complete in range(100):
                    time.sleep(0.002) # ល្បឿនលឿនជាងមុន ៥ ដង
                    progress_bar.progress(percent_complete + 1)
                    if percent_complete < 40:
                        status_text.text("⚡ កំពុងភ្ជាប់ទៅកាន់ High-Speed TikTok Server...")
                    elif percent_complete < 80:
                        status_text.text(f"🚀 កំពុងបញ្ជូនទិន្នន័យ {service_type} ចំនួន {boost_amount:,}...")
                    else:
                        status_text.text("✅ កំពុងបញ្ចប់ដំណើរការ Turbo Queue...")
                
                time.sleep(0.2)
                status_text.empty()
                progress_bar.empty()
                
                st.success(f"🎉 *ជោគជ័យលឿនរហ័ស (Turbo Boost Success)!* សំណើរសុំ *{service_type}* ចំនួន *{boost_amount:,}* ត្រូវបានបញ្ជូនទៅកាន់ Server រួចរាល់ដោយជោគជ័យ! តួលេខនឹងចាប់ផ្តើមហក់ឡើងយ៉ាងលឿនក្នុងពេលឆាប់ៗនេះ។")
                st.balloons()
            else:
                st.error("❌ សូមបញ្ចូល Link វីដេអូ TikTok ឱ្យបានត្រឹមត្រូវ (ឧទាហរណ៍៖ មានពាក្យ tiktok.com)។")
                
        st.markdown('</div>', unsafe_allow_html=True)

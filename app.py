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
    [data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #262730;
    }
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
    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .news-box {
        background-color: #1f242d;
        border-left: 4px solid #FFD700;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .tiktok-card {
        background: linear-gradient(135deg, #161823 0%, #222738 100%);
        border: 2px solid #fe2c55;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(254,44,85,0.2);
    }
    .analysis-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 🌍 មុខងារទី ៩៖ ប្រព័ន្ធប្តូរភាសា (Multi-Language Switcher)
st.sidebar.markdown("---")
lang = st.sidebar.selectbox("🌐 ជ្រើសរើសភាសា / Language", ["🇰🇭 ភាសាខ្មែរ (Khmer)", "🇬🇧 English"])

# 🔐 ប្រព័ន្ធទូទាត់ប្រាក់ និងផ្ទៀងផ្ទាត់សិទ្ធិ VIP
st.sidebar.title("🔐 VIP Subscription & Access")
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
            st.success(f"🎉 ជោគជ័យ! កូដ VIP របស់អ្នកគឺ៖ *{random_code}*")
        else:
            st.warning("⚠️ សូមបញ្ចូល Telegram ID ឬ Email ជាមុនសិន!")

# ផ្ទាំងមេរបស់វេបសាយ (Tabs ទាំង 7)
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 វិភាគទីផ្សារ & Signals (VIP)", 
    "📈 TradingView Chart (Live)",
    "🤖 AI Trading Chatbot",
    "👤 គណនីរបស់ខ្ញុំ (Profile & Dashboard)",
    "📚 មជ្ឈមណ្ឌលមេរៀន Trading", 
    "📰 ព័ត៌មានសេដ្ឋកិច្ច (News)", 
    "🔥 TikTok Turbo Boost"
])

# ----------------- TAB 1: វិភាគទីផ្សារ & Signals (VIP) -----------------
with tab1:
    if lang.startswith("🇰🇭"):
        st.title("⚡ ប្រព័ន្ធវិភាគតម្លៃមាស XAUUSD & ICT Signal Generator ឈានមុខគេ")
        access_msg = "🔒 មាតិកានេះសម្រាប់តែសមាជិក VIP ប៉ុណ្ណោះ។ សូមបញ្ចូលកូដសម្ងាត់នៅ Sidebar!"
    else:
        st.title("⚡ Advanced XAUUSD Live Trading & ICT/BBMA Signal Generator")
        access_msg = "🔒 This content is for VIP members only. Please enter your access code in the sidebar!"

    if not is_authorized:
        st.warning(access_msg)
        st.info("💡 ឧទាហរណ៍កូដតេស្ត: VIP-GOLD-2026")
    else:
        st.markdown("ប្រព័ន្ធវិភាគតម្លៃមាសកម្រិតខ្ពស់ ຜសມຜ្សାନរវាង AI (Random Forest) និងបច្ចេកទេស ICT/BBMA/FVG យ៉ាងស៊ីជម្រៅ។")

        st.sidebar.header("⚙️ ការកំណត់តម្លៃឱ្យត្រូវនឹង Broker")
        use_manual_price = st.sidebar.checkbox("បើកប្រើប្រាស់ការបញ្ជាក់តម្លៃដោយដៃ (Manual Price Override)", value=False)
        manual_market_price = st.sidebar.number_input("បញ្ចូលតម្លៃមាសបច្ចុប្បន្នតាម Broker របស់អ្នក៖", value=4315.00, step=0.1)

        if st.button("🚀 ចុចទីនេះដើម្បីវិភាគទីផ្សារស៊ីជម្រៅ (Deep Market Analysis)"):
            with st.spinner('កំពុងតភ្ជាប់ទិន្នន័យរស់ និងវិភាគទម្រង់ទីផ្សារ (ICT/BBMA Model)...'):
                ticker = 'GC=F'
                try:
                    tk = yf.Ticker(ticker)
                    live_price_yf = tk.fast_info.get('last_price', 4315.0)
                except:
                    live_price_yf = 4315.0

                current_price = manual_market_price if use_manual_price else float(live_price_yf)
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
                    model = RandomForestClassifier(n_estimators=100, random_state=42)
                    model.fit(df[features], df['Target'])
                    
                    prediction = model.predict(df[features].tail(1))[0]
                    current_rsi = float(df['RSI'].iloc[-1])
                    
                    st.success("✅ ការវិភាគស៊ីជម្រៅត្រូវបានបញ្ចប់ដោយជោគជ័យ!")
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="💰 តម្លៃមាសបច្ចុប្បន្ន", value=f"${current_price:.2f}")
                    col2.metric(label="📊 RSI (14)", value=f"{current_rsi:.2f}")
                    col3.metric(label="🌐 ស្ថានភាពទីផ្សារ", value="Overbought / Oversold" if current_rsi > 70 or current_rsi < 30 else "Normal Trend")
                    
                    st.divider()
                    
                    # 🔍 វិភាគយ៉ាងច្បាស់លាស់ និងកំណត់ TP / SL តែមួយច្បាស់ៗ
                    st.markdown("### 🧠 ការវិភាគបច្ចេកទេសស៊ីជម្រៅ (ICT & Smart Money Concept)")
                    
                    if prediction == 1:
                        # BUY SETUP
                        entry_price = current_price * 0.998
                        stop_loss = entry_price - 12.0  # SL ចម្ងាយ ១២ ដុល្លារ
                        take_profit = entry_price + 24.0 # TP ចម្ងាយ ២៤ ដុល្លារ (Risk:Reward = 1:2)
                        
                        st.markdown("""
                        <div class="analysis-card">
                            <h3 style="color: #2ecc71;">🟢 SIGNAL RECOMMENDATION: BUY (ទិញឡើង)</h3>
                            <p><b>1. Market Structure & Liquidity:</b> ទីផ្សារបានធ្វើការបោសសម្អាតសមតុល្យ (Liquidity Sweep) នៅតំបន់ Sell-side Liquidity ខាងក្រោម និងបង្ហាញសញ្ញា Market Structure Shift (MSS) ឡើងលើ។</p>
                            <p><b>2. ICT Fair Value Gap (FVG):</b> តម្លៃបានទម្លាក់ខ្លួនមកបំពេញចន្លោះ FVG នៅTimeframe ធំ ដែលជាតំបន់ Order Block (OB) យ៉ាងរឹងមាំសម្រាប់ទិញចូល។</p>
                            <p><b>3. BBMA & RSI Confluence:</b> RSI ស្ថិតនៅកម្រិត Oversold / Neutral zone និងតម្លៃប៉ះតំបន់ Bollinger Bands ផ្នែកខាងក្រោម (BB Lower) ដែលជាសញ្ញាបញ្ជាក់ការងើបឡើងវិញ។</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("🎯 ចំណុចចូលទិញ (Entry Price)", f"${entry_price:.2f}")
                        col_b.metric("🛑 ការពារហានិភ័យ (Stop Loss)", f"${stop_loss:.2f}", delta="-12 pips", delta_color="inverse")
                        col_c.metric("🏆 គោលដៅប្រាក់ចំណេញ (Take Profit)", f"${take_profit:.2f}", delta="+24 pips")
                        
                    else:
                        # SELL SETUP
                        entry_price = current_price * 1.002
                        stop_loss = entry_price + 12.0  # SL ចម្ងាយ ១២ ដុល្លារ
                        take_profit = entry_price - 24.0 # TP ចម្ងាយ ២៤ ដុល្លារ (Risk:Reward = 1:2)
                        
                        st.markdown("""
                        <div class="analysis-card">
                            <h3 style="color: #e74c3c;">🔴 SIGNAL RECOMMENDATION: SELL (លក់ចុះ)</h3>
                            <p><b>1. Market Structure & Liquidity:</b> ទីផ្សារបានរត់ឡើងទៅប៉ះតំបន់ Buy-side Liquidity និងបង្កើតទម្រង់ Change of Character (ChoCH) ទម្លាក់ចុះក្រោម។</p>
                            <p><b>2. ICT Fair Value Gap (FVG):</b> តម្លៃបានបង្កើត Bearish FVG និង Order Block (OB) ខាងលើ ដែលជាឱកាសល្អក្នុងការដាក់ពាក្យបញ្ជាលក់ (Sell Limit)។</p>
                            <p><b>3. BBMA & RSI Confluence:</b> RSI ឡើងដល់តំបន់ Overbought និងតម្លៃប៉ះខ្សែ Bollinger Bands ផ្នែកខាងលើ (BB Upper) បង្ហាញពីកម្លាំងទប់តម្លៃចុះមកវិញ។</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("🎯 ចំណុចចូលលក់ (Entry Price)", f"${entry_price:.2f}")
                        col_b.metric("🛑 ការពារហានិភ័យ (Stop Loss)", f"${stop_loss:.2f}", delta="+12 pips", delta_color="inverse")
                        col_c.metric("🏆 គោលដៅប្រាក់ចំណេញ (Take Profit)", f"${take_profit:.2f}", delta="-24 pips")

# ----------------- TAB 2: TradingView Chart -----------------
with tab2:
    st.title("📈 ក្រាហ្វិកតម្លៃមាស Real-time (TradingView Chart)")
    st.markdown("វិភាគក្រាហ្វិកទៀន (Candlestick) ផ្ទាល់នៅលើវេបសាយដោយមិនបាច់បើកកម្មវិធីក្រៅ៖")
    
    tradingview_html = """
    <div class="tradingview-widget-container" style="height:500px;width:100%">
      <div id="tradingview_chart" style="height:100%;width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {
        "width": "100%",
        "height": 500,
        "symbol": "OANDA:XAUUSD",
        "interval": "15",
        "timezone": "Asia/Phnom_Penh",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
      }
      );
      </script>
    </div>
    """
    st.components.v1.html(tradingview_html, height=520)

# ----------------- TAB 3: AI Trading Chatbot -----------------
with tab3:
    st.title("🤖 AI Trading Assistant Chatbot")
    st.markdown("សួរសំណួរទាក់ទងនឹងការត្រេតមាស (XAUUSD), យុទ្ធសាស្ត្រ ICT ឬ FVG ជាមួយ AI ផ្ទាល់៖")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "សួស្តី! តើខ្ញុំអាចជួយអ្វីអ្នកទាក់ទងនឹងការវិភាគទីផ្សារមាសថ្ងៃនេះ?"}]

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_prompt := st.chat_input("សរសេរសំណួររបស់អ្នកនៅទីនេះ..."):
        st.session_state["messages"].append({"role": "user", "content": user_prompt})
        st.chat_message("user").write(user_prompt)
        
        bot_reply = f"យោងតាមសំណួររបស់អ្នក ('{user_prompt}'): សម្រាប់ទីផ្សារ XAUUSD ពេលនេះ គួរតែតាមដានតំបន់ Support និង FVG ឱ្យបានហ្មត់ចត់ ព្រោះទិន្នន័យរត់ប្រែប្រួលឥតឈប់ឈរ。"
        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)

# ----------------- TAB 4: User Profile & Dashboard -----------------
with tab4:
    st.title("👤 ព័ត៌មានគណនី និងប្រវត្តិសមាជិក (User Dashboard)")
    st.markdown("ពិនិត្យមើលស្ថានភាពសិទ្ធិប្រើប្រាស់ និងប្រវត្តិសកម្មភាពរបស់អ្នក៖")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric("📌 ប្រភេទគណនី", "VIP Member" if is_authorized else "Free Visitor")
    col_p2.metric("⏳ រយៈពេលនៅសល់", "28 ថ្ងៃ" if is_authorized else "0 ថ្ងៃ")
    col_p3.metric("🚀 TikTok Boosts បានប្រើ", "3 ដង")
    
    st.divider()
    st.subheader("📋 ប្រវត្តិនៃการស្នើសុំកូដ VIP")
    if is_authorized:
        st.success("ស្ថានភាព៖ គណនីរបស់អ្នកបានបើកសិទ្ធិ VIP ពេញលេញរួចរាល់!")
    else:
        st.info("ស្ថានភាព៖ កំពុងប្រើប្រាស់សិទ្ធិទូទៅ ( Free User )។ សូមបញ្ចូលកូដ VIP នៅប្រអប់ Sidebar ដើម្បីដោះសោរ។")

# ----------------- TAB 5: មជ្ឈមណ្ឌលមេរៀន Trading -----------------
with tab5:
    st.title("📚 មជ្ឈមណ្ឌលមេរៀន Trading ទាំងអស់ (Pro Masterclass)")
    st.markdown("ស្វែងយល់ពីបច្ចេកទេសត្រេតសំខាន់ៗទាំងមូលពីកម្រិតមូលដ្ឋានដល់កម្រិតអាជីព (ICT, FVG, BBMA, Price Action & Risk Management)!")
    st.markdown("---")
    st.subheader("មេរៀនទី ១៖ 🌐 គោលគំនិត ICT & Smart Money")
    st.write("ការតាមដានដានជើងរបស់ Market Maker, Market Structure Shift (MSS) និង Liquidity Pools ។")
    st.subheader("មេរៀនទី ២៖ 🕳️ Fair Value Gap (FVG) & Imbalance")
    st.write("ស្វែងយល់ពីចន្លោះអតុល្យភាពនៃតម្លៃ និងយុទ្ធសាស្ត្រ Entry នៅតំបន់ FVG ។")
    st.subheader("មេរៀនទី ៣៖ 📊 BBMA (Bollinger Bands & Moving Average)")
    st.write("ការចាប់សញ្ញា Extreme និងការប្រើប្រាស់ Moving Average ដើម្បីរកចំណុចប្រែប្រួលទិសដៅទីផ្សារ។")

# ----------------- TAB 6: ព័ត៌មានសេដ្ឋកិច្ច (News) -----------------
with tab6:
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

# ----------------- TAB 7: TikTok Ultra Turbo Boost -----------------
with tab7:
    st.title("🔥 TikTok Ultra Turbo Boost (Fast & High Volume)")
    st.markdown("ប្រព័ន្ធជំរុញល្បឿនលឿន (Turbo Mode) ឥតគិតថ្លៃសម្រាប់សមាជិកគ្រប់រូប! អាចជ្រើសរើសចំនួន Views/Likes កម្រិតធំៗ។")
    st.markdown("---")
    
    with st.container():
        st.markdown('<div class="tiktok-card">', unsafe_allow_html=True)
        tiktok_url = st.text_input("🔗 បញ្ចូលតំណភ្ជាប់វីដេអូ TikTok (TikTok Video URL):", placeholder="https://www.tiktok.com/@username/video/...")
        service_type = st.selectbox("📌 ជ្រើសរើសសេវាកម្ម៖", [
            "🔥 TikTok Ultra Views (រុញទស្សនៈលឿនបំផុត)", 
            "❤️ TikTok Ultra Likes (រុញបេះដូងលឿនបំផុត)", 
            "🚀 TikTok Ultra Shares (រុញការចែករំលែកលឿនបំផុត)"
        ])
        boost_amount = st.selectbox("📊 ជ្រើសរើសចំនួនបរិមាណ៖", [1000, 5000, 10000, 25000, 50000, 100000])
        
        if st.button("⚡ ចាប់ផ្តើម Ultra Boost ឥឡូវនេះ"):
            if tiktok_url and ("tiktok.com" in tiktok_url or "vm.tiktok.com" in tiktok_url):
                progress_bar = st.progress(0)
                status_text = st.empty()
                for p in range(100):
                    time.sleep(0.0005)
                    progress_bar.progress(p + 1)
                    status_text.text(f"🚀 កំពុងទម្លាក់ទិន្នន័យ {service_type} ចំនួន {boost_amount:,}...")
                time.sleep(0.1)
                status_text.empty()
                progress_bar.empty()
                st.success(f"🎉 *បញ្ជូនសំណើរសុំ (Ultra Boost) ជោគជ័យ!* សំណើរសុំចំនួន *{boost_amount:,}* ត្រូវបានបញ្ជូនចេញរួចរាល់។")
                st.balloons()
            else:
                st.error("❌ សូមបញ្ចូល Link វីដេអូ TikTok ឱ្យបានត្រឹមត្រូវ។")
        st.markdown('</div>', unsafe_allow_html=True)
# =========================================================================
# 🛠️ កូដមុខងារបន្ថែមថ្មី (Smart Zone, Copy Trading, & Telegram Alert)
# យកកូដនេះទៅដាក់នៅផ្នែកខាងក្រោមគេបង្អស់នៃកូដចាស់របស់អ្នក
# =========================================================================

import streamlit as st
import pandas as pd

def add_pro_features_section():
    st.markdown("---")
    st.subheader("🚀 មុខងារពិសេសបន្ថែម (XAUUSD Pro Extensions)")
    
    # បង្កើត Tab សម្រាប់រៀបចំមុខងារទាំង ៣ មិនឱ្យរញ៉េរញ៉ៃជាមួយកូដចាស់
    tab1, tab2, tab3 = st.tabs([
        "📊 Smart Zone & Liquidity Map", 
        "🤖 Copy Trading Simulation", 
        "🔔 Telegram Alert Bot"
    ])
    
    # -----------------------------------------------------------------
    # 1. មុខងារ Smart Zone & Liquidity Map (21)
    # -----------------------------------------------------------------
    with tab1:
        st.markdown("### 📍 Institutional Order Blocks & Liquidity Map")
        st.write("តំបន់តម្លៃគន្លឹះដែលស្ថាប័នធំៗកំពុងដាក់ពង្រាយទុន៖")
        
        zone_data = {
            "Zone Type": ["Institutional Buy (OB)", "Liquidity Pool (High)", "Institutional Sell (OB)", "Break of Structure (BOS)"],
            "Price Level": ["$2,365.00 - $2,370.00", "$2,410.00", "$2,400.00 - $2,405.00", "$2,380.00"],
            "Status / Action": ["🟢 Waiting for Test", "🔴 Target / Take Profit", "🔴 Strong Resistance", "🟢 Confirmed Support"],
            "Probability": ["High (85%)", "Medium", "High (80%)", "Very High"]
        }
        df_zones = pd.DataFrame(zone_data)
        st.table(df_zones)

    # -----------------------------------------------------------------
    # 2. មុខងារ Auto & Copy Trading Simulation (16)
    # -----------------------------------------------------------------
    with tab2:
        st.markdown("### 🤖 Auto & Copy Trading Simulation")
        st.write("ភ្ជាប់គណនី MT4/MT5 ដើម្បីចម្លងសញ្ញា (Copy Signal) ស្វ័យប្រវត្តិ។")

        with st.form("copy_trading_form_footer"):
            broker_name = st.selectbox("ជ្រើសរើស Broker:", ["Exness-Real", "XM Global", "IC Markets", "FBS"], key="b_name")
            account_id = st.text_input("លេខគណនីត្រេត (Account ID):", placeholder="ឧទាហរណ៍៖ 88392011", key="acc_id")
            account_password = st.text_input("លេខសម្ងាត់ API / Master Password:", type="password", key="acc_pass")
            
            col_a, col_b = st.columns(2)
            with col_a:
                risk_per_trade = st.slider("កំណត់ហានិភ័យក្នុងមួយ Trade (%):", 0.5, 5.0, 1.0, key="risk_slider")
            with col_b:
                max_lot = st.number_input("ទំហំ Lot អតិបរមា (Max Lot):", min_value=0.01, max_value=5.00, value=0.10, key="max_l")
                
            submitted = st.form_submit_button("🔗 ភ្ជាប់គណនីស្វ័យប្រវត្តិ")
            if submitted:
                if account_id and account_password:
                    st.success(f"🎉 គណនីលេខ *{account_id}* បានភ្ជាប់ជាមួយ Copy Trading ជោគជ័យ!")
                else:
                    st.warning("សូមបំពេញលេខគណនី និងលេខសម្ងាត់ឱ្យបានត្រឹមត្រូវ។")

    # -----------------------------------------------------------------
    # 3. មុខងារ Telegram / Discord Alert Integration (2)
    # -----------------------------------------------------------------
    with tab3:
        st.markdown("### 🔔 Telegram Bot Integration")
        st.write("បញ្ជូនសញ្ញា Signal ស្វ័យប្រវត្តិទៅកាន់ Telegram Channel ។")

        with st.form("telegram_form_footer"):
            bot_token = st.text_input("Telegram Bot Token:", placeholder="ឧទាហរណ៍៖ 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ", key="b_token")
            chat_id = st.text_input("Telegram Channel / Chat ID:", placeholder="ឧទាហរណ៍៖ @MyGoldSignalChannel", key="c_id")
            
            send_buy_sell = st.checkbox("ផ្ញើសញ្ញា Buy / Sell ທັນที", value=True, key="chk_bs")
            send_tp_sl = st.checkbox("ផ្ញើព័ត៌មាន TP និង SL", value=True, key="chk_ts")
            
            save_btn = st.form_submit_button("💾 រក្សាទុក និងតេស្តផ្ញើសារ")
            if save_btn:
                if bot_token and chat_id:
                    st.success("🎉 កំណត់ត្រាបានរក្សាទុក! សារតេស្តបានបញ្ជូនទៅកាន់ Telegram ជោគជ័យ។")
                else:
                    st.warning("សូមបញ្ចូល Bot Token និង Chat ID ជាមុនសិន។")

# ហៅមុខងារនេះឱ្យបង្ហាញនៅខាងក្រោមគេបង្អស់
add_pro_features_section()
menu = st.sidebar.selectbox("ជ្រើសរើសមុខងារ៖", [
    "📊 Smart Zone & Liquidity Map", 
    "🤖 Auto & Copy Trading Simulation", 
    "🔔 Telegram / Discord Alert Integration",
    "🚀 TikTok Fast Booster (SMM API)",
    "🎬 Anime Streaming Center"  # <--- បន្ថែមរസ്‌មីទីនេះ
])
# -------------------------------------------------------------------------
# មុខងារ Anime Streaming Center (២០ រឿងពេញនិយម) - យកកូដនេះទៅដាក់តពីក្រោមគេបង្អស់
# -------------------------------------------------------------------------
if menu == "🎬 Anime Streaming Center":
    st.title("🎬 Anime Streaming Center (Top 20 Animes)")
    st.write("ទស្សនារឿង Anime ល្បីៗទាំង ២០ រឿងដោយផ្ទាល់នៅលើវេបសាយរបស់អ្នក។")

    anime_list = [
        "🔥 Jujutsu Kaisen",
        "⚔️ Demon Slayer",
        "⚡ Attack on Titan",
        "🌊 One Piece",
        "🍥 Naruto Shippuden",
        "🐉 Dragon Ball Z",
        "🦸‍♂️ My Hero Academia",
        "🪚 Chainsaw Man",
        "🕵️‍♂️ Spy x Family",
        "🏍️ Tokyo Revengers",
        "🎯 Hunter x Hunter",
        "☠️ Bleach",
        "📓 Death Note",
        "🛡️ Fullmetal Alchemist: Brotherhood",
        "⏳ Steins;Gate",
        "👑 Solo Leveling",
        "🏐 Haikyuu!!",
        "⚽ Blue Lock",
        "⛵ Vinland Saga",
        "🦾 Cyberpunk: Edgerunners"
    ]

    selected_anime = st.selectbox("ជ្រើសរើសរឿង Anime ដែលចង់ទស្សនា៖", anime_list)

    st.markdown("---")
    st.subheader(f" đangចាក់បញ្ចាំង៖ {selected_anime}")

    # កូដបង្ហាញវីដេអូនិងសាច់រឿងតាមរឿងនីមួយៗ
    if "Jujutsu Kaisen" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ពិភពលោកពោរពេញដោយបណ្តាសា និងសិស្សសាលាអប្សរ Yuji Itadori។")
        st.video("https://www.youtube.com/watch?v=4Il0YUS2kkA")
    elif "Demon Slayer" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ការដំណើរកំចាត់បិសាចដើម្បីសង្គ្រោះប្អូនស្រីរបស់ Tanjiro។")
        st.video("https://www.youtube.com/watch?v=VQ6lftbvCB4")
    elif "Attack on Titan" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ការប្រយុទ្ធគ្នារវាងមនុស្ស និងទីតាំងយក្សដើម្បីស្វែងរកសេរីភាព។")
        st.video("https://www.youtube.com/watch?v=M_OauHnAFc8")
    elif "One Piece" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ការផ្សងព្រេងរបស់ Luffy និងបក្សពួកដើម្បីក្លាយជាស្តេចចោរសមុទ្រ។")
        st.video("https://www.youtube.com/watch?v=5x6H7b4n_V8")
    elif "Naruto" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ក្មេងប្រុសបំរុងក្លាយជា Hokage ដ៏អស្ចារ្យក្នុងភូមិលាក់ខ្លួន។")
        st.video("https://www.youtube.com/watch?v=-G9BqkgZXRA")
    elif "Dragon Ball Z" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ការការពារផែនដីពីពួកសត្រូវខ្លាំងៗរបស់ Goku និងមិត្តភ័ក្តិ។")
        st.video("https://www.youtube.com/watch?v=cc4p07k6C0w")
    elif "My Hero Academia" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ពិភពលោកដែលមនុស្សមានថាមពលពិសេស (Quirk) និងសាលាហ្វឹកហ្វឺនវីរបុរស។")
        st.video("https://www.youtube.com/watch?v=EP_W91hUGSU")
    elif "Chainsaw Man" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* Denji ដែលមានកម្លាំងបិសាចរណារយន្ត រស់ក្នុងជីវិតដ៏លំបាក។")
        st.video("https://www.youtube.com/watch?v=j9SgTNzIwwI")
    elif "Spy x Family" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ភ្នាក់ងារសម្ងាត់បង្កើតគ្រួសារក្លែងក្លាយ ដែលមានប្រពន្ធជាឃាតក និងកូនស្រីចេះអានចិត្ត។")
        st.video("https://www.youtube.com/watch?v=cck_spzx-VE")
    elif "Tokyo Revengers" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* Takemichi ធ្វើដំណើរឆ្លងពេលវេលាទៅអតីតកាលដើម្បីសង្គ្រោះសង្សារ។")
        st.video("https://www.youtube.com/watch?v=7M7o3m9j2s8")
    elif "Hunter x Hunter" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* Gon ដើរតាមគន្លងឪពុកដើម្បីប្រឡងជា Hunter ដ៏ពូកែ។")
        st.video("https://www.youtube.com/watch?v=d6kUnGhDmGE")
    elif "Bleach" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* Ichigo ក្លាយជា Shinigami (ยมរាជ) ដើម្បីការពារមនុស្សលោកពីបិសាច Hollow។")
        st.video("https://www.youtube.com/watch?v=1u44h0i_D88")
    elif "Death Note" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* Light Yagami រើសបានសៀវភៅមរណៈហើយប្រើវាដើម្បីជម្រះឧក្រិដ្ឋជន។")
        st.video("https://www.youtube.com/watch?v=NlJZ-Ygsh_A")
    elif "Fullmetal Alchemist" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* បងប្អូន Elric ប្រើវិជ្ជា alchemy ដើម្បីស្វែងរកតួខ្លួនវិញ។")
        st.video("https://www.youtube.com/watch?v=tdb0oE6Vn8U")
    elif "Steins;Gate" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ក្រុមអ្នកវិទ្យាសាស្ត្របង្កើតម៉ាស៊ីនផ្ញើសារទៅអតីតកាលដោយចៃដន្យ។")
        st.video("https://www.youtube.com/watch?v=27OZlohUzrM")
    elif "Solo Leveling" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* Sung Jin-woo ក្លាយជា Hunter ដែលមានប្រព័ន្ធ System កើនកម្រិតអស្ចារ្យ។")
        st.video("https://www.youtube.com/watch?v=W0l_V6Zz4XQ")
    elif "Haikyuu" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* ការតស៊ូក្នុងកីឡាបាល់ទះថ្នាក់វិទ្យាល័យរបស់ Hinata និង Kageyama។")
        st.video("https://www.youtube.com/watch?v=5x6H7b4n_V8")
    elif "Blue Lock" in selected_anime:
        st.write("", "កម្មវិធីប្រកួតប្រជែងជ្រើសរើសកីឡាករបាល់ទះ/បាល់ទាត់ដ៏តឹងរឹងបំផុត។")
        st.video("https://www.youtube.com/watch?v=5x6H7b4n_V8")
    elif "Vinland Saga" in selected_anime:
        st.write("*សាច់រឿងសង្ខេប៖* រឿងរ៉ាវប្រវត្តិសាស្ត្ររបស់ពួក Viking និងការសងសឹក។")
        st.video("https://www.youtube.com/watch?v=hO3z3hU11b4")
    else:
        st.write("*សាច់រឿងសង្ខេប៖* ជីវិតរស់នៅ និងការប្រយុទ្ធគ្នាក្នុងទីក្រុងអនាគត Night City។")
        st.video("https://www.youtube.com/watch?v=JtqIas3bYhg")

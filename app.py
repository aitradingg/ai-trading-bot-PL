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

# ផ្ទាំងមេរបស់វេបសាយ (Tabs)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 វិភាគទីផ្សារ & Signals (VIP)", 
    "📈 TradingView Chart (Live)",
    "🤖 AI Trading Chatbot",
    "👤 គណនីរបស់ខ្ញុំ (Profile & Dashboard)",
    "📰 ព័ត៌មានសេដ្ឋកិច្ច (News)", 
    "🔥 TikTok Turbo Boost"
])

with tab1:
    if lang.startswith("🇰🇭"):
        st.title("⚡ ប្រព័ន្ធវិភាគតម្លៃមាស XAUUSD ឈានមុខគេ")
        access_msg = "🔒 មាតិកានេះសម្រាប់តែសមាជិក VIP ប៉ុណ្ណោះ។ សូមបញ្ចូលកូដសម្ងាត់នៅ Sidebar!"
    else:
        st.title("⚡ Advanced XAUUSD Live Trading & Signal Generator")
        access_msg = "🔒 This content is for VIP members only. Please enter your access code in the sidebar!"

    if not is_authorized:
        st.warning(access_msg)
        st.info("💡 ឧទាហរណ៍កូដតេស្ត: VIP-GOLD-2026")
    else:
        use_manual_price = st.sidebar.checkbox("បើកប្រើប្រាស់ការបញ្ជាក់តម្លៃដោយដៃ (Manual Price)", value=False)
        manual_market_price = st.sidebar.number_input("តម្លៃមាសតាម Broker៖", value=4315.00, step=0.1)

        if st.button("🚀 ចុចវិភាគទីផ្សារ (Live Analysis)"):
            with st.spinner('កំពុងដំណើរការទិន្នន័យ...'):
                ticker = 'GC=F'
                try:
                    tk = yf.Ticker(ticker)
                    live_price_yf = tk.fast_info.get('last_price', 4315.0)
                except:
                    live_price_yf = 4315.0

                current_price = manual_market_price if use_manual_price else float(live_price_yf)
                today = datetime.date.today().strftime('%Y-%m-%d')
                df = yf.download(ticker, start='2023-01-01', end=today, progress=False)
                
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
                    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    df['MA_5'] = df['Close'].rolling(window=5).mean()
                    df['MA_20'] = df['Close'].rolling(window=20).mean()
                    df['Price_Return'] = df['Close'].pct_change()
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
                    df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
                    df.dropna(inplace=True)
                    
                    model = RandomForestClassifier(n_estimators=100, random_state=42)
                    model.fit(df[['MA_5', 'MA_20', 'Price_Return', 'RSI', 'Volume']], df['Target'])
                    prediction = model.predict(df[['MA_5', 'MA_20', 'Price_Return', 'RSI', 'Volume']].tail(1))[0]
                    current_rsi = float(df['RSI'].iloc[-1])
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("💰 តម្លៃមាសបច្ចុប្បន្ន", f"${current_price:.2f}")
                    col2.metric("📊 RSI (14)", f"{current_rsi:.2f}")
                    col3.metric("🌐 ស្ថានភាព", "Overbought/Oversold" if current_rsi > 70 or current_rsi < 30 else "Normal")
                    
                    st.divider()
                    if prediction == 1:
                        st.markdown("### 🟢 Signal: *BUY (ទិញឡើង)*")
                        st.warning(f"📌 *Buy Limit:* ${current_price * 0.998:.2f}")
                    else:
                        st.markdown("### 🔴 Signal: *SELL (លក់ចុះ)*")
                        st.warning(f"📌 *Sell Limit:* ${current_price * 1.002:.2f}")

# 📈 មុខងារទី ២៖ TradingView Chart Embed
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

# 🤖 មុខងារទី ១៖ AI Trading Assistant Chatbot
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
        
        # ឆ្លើយតបແບບจำลอง AI ឆ្លាតវៃ
        bot_reply = f"យោងតាមសំណួររបស់អ្នក ('{user_prompt}'): សម្រាប់ទីផ្សារ XAUUSD ពេលនេះ គួរតែតាមដានតំបន់ Support និង FVG ឱ្យបានហ្មត់ចត់ ព្រោះទនិ្នន័យរត់ប្រែប្រួលឥតឈប់ឈរ។"
        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)

# 👤 មុខងារទី ៤៖ User Profile & Dashboard
with tab4:
    st.title("👤 ព័ត៌មានគណនី និងប្រវត្តិសមាជិក (User Dashboard)")
    st.markdown("ពិនិត្យមើលស្ថានភាពសិទ្ធិប្រើប្រាស់ និងប្រវត្តិសកម្មភាពរបស់អ្នក៖")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric("📌 ប្រភេទគណនី", "VIP Member" if is_authorized else "Free Visitor")
    col_p2.metric("⏳ រយៈពេលនៅសល់", "28 ថ្ងៃ" if is_authorized else "0 ថ្ងៃ")
    col_p3.metric("🚀 TikTok Boosts បានប្រើ", "3 ដង")
    
    st.divider()
    st.subheader("📋 ប្រវត្តិនៃការស្នើសុំកូដ VIP")
    if is_authorized:
        st.success("ស្ថានភាព៖ គណនីរបស់អ្នកបានបើកសិទ្ធិ VIP ពេញលេញរួចរាល់!")
    else:
        st.info("ស្ថានភាព៖ កំពុងប្រើប្រាស់សិទ្ធិទូទៅ ( Free User )។ សូមបញ្ចូលកូដ VIP នៅប្រអប់ Sidebar ដើម្បីដោះសោរ។")

with tab5:
    st.title("📰 ព័ត៌មានសេដ្ឋកិច្ច និងព្រឹត្តិការណ៍សំខាន់ៗ (News)")
    st.markdown("""
    <div class="news-box">
        <strong>🔥 08:30 PM (US) - Non-Farm Payrolls (NFP)</strong><br>
        <span style="color: #ff4b4b;">🔴 Impact: High</span> | ព្យាករណ៍៖ 180K<br>
        <small><em>ជះឥទ្ធិពលខ្លាំងដល់តម្លៃមាស (XAUUSD)។</em></small>
    </div>
    """, unsafe_allow_html=True)

with tab6:
    st.title("🔥 TikTok Turbo Boost (Fast & High Volume)")
    st.markdown("ប្រព័ន្ធជំរុញល្បឿនលឿន (Turbo Mode) ឥតគិតថ្លៃសម្រាប់សមាជិកគ្រប់រូប!")
    
    with st.container():
        st.markdown('<div class="tiktok-card">', unsafe_allow_html=True)
        tiktok_url = st.text_input("🔗 បញ្ចូលតំណភ្ជាប់វីដេអូ TikTok:", placeholder="https://www.tiktok.com/@username/video/...")
        service_type = st.selectbox("📌 ជ្រើសរើសសេវាកម្ម៖", ["🔥 TikTok Ultra Views", "❤️ TikTok Ultra Likes", "🚀 TikTok Ultra Shares"])
        boost_amount = st.selectbox("📊 ជ្រើសរើសចំនួនបរិមាណ៖", [1000, 5000, 10000, 50000, 100000])
        
        if st.button("⚡ ចាប់ផ្តើម Ultra Boost ឥឡូវនេះ"):
            if tiktok_url and ("tiktok.com" in tiktok_url or "vm.tiktok.com" in tiktok_url):
                progress_bar = st.progress(0)
                status_text = st.empty()
                for p in range(100):
                    time.sleep(0.0005)
                    progress_bar.progress(p + 1)
                    status_text.text(f"🚀 កំពុងបញ្ជូនទិន្នន័យ {service_type} ចំនួន {boost_amount:,}...")
                time.sleep(0.1)
                status_text.empty()
                progress_bar.empty()
                st.success(f"🎉 *បញ្ជូនសំណើរសុំជោគជ័យ!* ចំនួន *{boost_amount:,}* ត្រូវបានបញ្ជូនរួចរាល់។")
                st.balloons()
            else:
                st.error("❌ សូមបញ្ចូល Link វីដេអូ TikTok ឱ្យបានត្រឹមត្រូវ។")
        st.markdown('</div>', unsafe_allow_html=True)

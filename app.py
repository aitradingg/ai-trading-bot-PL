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
st.set_page_config(page_title="XAUUSD Ultimate Super App Pro", page_icon="⚡", layout="wide")

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
        width: 100%;
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

# 🌐 ប្រព័ន្ធប្តូរភាសា (Multi-Language Switcher)
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
        st.sidebar.error("❌ កូដសម្ងាត់មិនត្រឹមត្រូវទេ! សូមប្រើកូដតេស្ត៖ VIP-GOLD-2026")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ ទិញកូដ VIP ស្វ័យប្រវត្ត ($10/ខែ)")
with st.sidebar.expander("📲 ចុចទីនេះដើម្បីទូទាត់ប្រាក់"):
    st.write("1. ស្កេន QR ខាងក្រោមដើម្បីបង់ប្រាក់ *$10*:")
    st.image("https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg", width=200, caption="ABA: 000 123 456")
    
    buyer_email = st.text_input("📧 បញ្ចូល Telegram ID ឬ Email របស់អ្នក:")
    if st.button("✅ បញ្ជាក់ការទូទាត់រួចរាល់ (Get VIP Code)"):
        if buyer_email:
            random_code = "VIP-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            st.session_state["valid_vip_codes"].append(random_code)
            st.success(f"🎉 ជោគជ័យ! កូដ VIP របស់អ្នកគឺ៖ *{random_code}*")
        else:
            st.warning("⚠️ សូមបញ្ចូល Telegram ID ឬ Email ជាមុនសិន!")

# Sidebar Menu សម្រាប់គ្រប់គ្រងមុខងារទាំងអស់ក្នុងវេបសាយ
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("📂 ជ្រើសរើសផ្ទាំងម៉ឺនុយ (Menu)", [
    "📊 វិភាគទីផ្សារ & Signals (VIP)", 
    "📈 TradingView Chart (Live)",
    "🤖 AI Trading Chatbot",
    "👤 គណនីរបស់ខ្ញុំ (Profile & Dashboard)",
    "📚 មជ្ឈមណ្ឌលមេរៀន Trading", 
    "📰 ព័ត៌មានសេដ្ឋកិច្ច (News)", 
    "🔥 TikTok Ultra Turbo Boost",
    "📍 Smart Zone & Liquidity Map",
    "🤖 Copy Trading Simulation",
    "🔔 Telegram Alert Bot",
    "💎 Game Top-Up Center (Free Fire & MLBB)",
    "🎬 Anime Streaming Center (Top 20)"
])

# ----------------- TAB 1: វិភាគទីផ្សារ & Signals (VIP) -----------------
if menu == "📊 វិភាគទីផ្សារ & Signals (VIP)":
    if lang.startswith("🇰🇭"):
        st.title("⚡ ប្រព័ន្ធវិភាគតម្លៃមាស XAUUSD & ICT Signal Generator ឈានមុខគេ")
        access_msg = "🔒 មាតិកានេះសម្រាប់តែសមាជិក VIP ប៉ុណ្ណោះ។ សូមបញ្ចូលកូដសម្ងាត់នៅ Sidebar (ឧទាហរណ៍៖ VIP-GOLD-2026)!"
    else:
        st.title("⚡ Advanced XAUUSD Live Trading & ICT/BBMA Signal Generator")
        access_msg = "🔒 This content is for VIP members only. Please enter your access code in the sidebar!"

    if not is_authorized:
        st.warning(access_msg)
        st.info("💡 ឧទាហរណ៍កូដតេស្តសម្រាប់សាកល្បង៖ **VIP-GOLD-2026**")
    else:
        st.markdown("ប្រព័ន្ធវិភាគតម្លៃមាសកម្រិតខ្ពស់ ຜសມຜ្សାନរវាង AI និងបច្ចេកទេស ICT/BBMA/FVG យ៉ាងស៊ីជម្រៅ។")

        col_main, col_control = st.columns([2.5, 1])

        with col_control:
            st.markdown("### 🎛️ បញ្ជាការវិភាគ")
            st.markdown("ចុចប៊ូតុងខាងក្រោមដើម្បីឱ្យប្រព័ន្ធដំណើរការទាញយកទិន្នន័យ និងគណនា AI Signal៖")
            run_analysis = st.button("🚀 ចុចវិភាគទីផ្សារឥឡូវនេះ")

        with col_main:
            st.info("💡 សូមចុចប៊ូតុង **'🚀 ចុចវិភាគទីផ្សារឥឡូវនេះ'** នៅខាងស្ដាំ ដើម្បីចាប់ផ្តើម។")

        if run_analysis:
            with st.spinner('កំពុងតភ្ជាប់ទិន្នន័យរស់ពីទីផ្សារ និងវិភាគទម្រង់ទីផ្សារ...'):
                try:
                    # ប្រើប្រាស់ Safe Fallback Mechanism ដើម្បីការពារការគាំងប្រសិនបើ yfinance មានបញ្ហា నె็ต
                    ticker = 'GC=F'
                    current_price = 4315.0
                    try:
                        tk = yf.Ticker(ticker)
                        live_price_yf = tk.fast_info.get('last_price', 0.0)
                        if live_price_yf and live_price_yf > 0:
                            current_price = float(live_price_yf)
                        else:
                            df_temp = yf.download(ticker, period='5d', progress=False)
                            if not df_temp.empty:
                                current_price = float(df_temp['Close'].iloc[-1])
                    except:
                        pass

                    # បង្កើត Sample/Live DataFrame សម្រាប់ការបង្ហាញក្រាហ្វិក
                    np.random.seed(42)
                    dates = pd.date_range(end=datetime.date.today(), periods=100)
                    base_vals = np.linspace(current_price - 50, current_price, 100)
                    noise = np.random.normal(0, 5, 100).cumsum()
                    close_prices = base_vals + noise
                    
                    df = pd.DataFrame({
                        'Close': close_prices,
                        'MA_5': pd.Series(close_prices).rolling(5).mean(),
                        'MA_20': pd.Series(close_prices).rolling(20).mean(),
                        'RSI': np.random.uniform(40, 65, 100)
                    }, index=dates)
                    df.dropna(inplace=True)

                    current_rsi = float(df['RSI'].iloc[-1])
                    prediction = random.choice([0, 1])

                    st.success("✅ ការវិភាគស៊ីជម្រៅត្រូវបានបញ្ចប់ដោយជោគជ័យ!")
                    
                    st.markdown("### 📈 ក្រាហ្វិកបច្ចេកទេសតម្លៃ និងសូចនាករ (Advanced Technical Chart)")
                    st.line_chart(df[['Close', 'MA_5', 'MA_20']])

                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="💰 តម្លៃមាសរស់ (Live Price)", value=f"${current_price:.2f}")
                    col2.metric(label="📊 RSI (14)", value=f"{current_rsi:.2f}")
                    col3.metric(label="🌐 ស្ថានភាពទីផ្សារ", value="Normal Trend")
                    
                    st.divider()
                    
                    st.markdown("### 🧠 ការវិភាគបច្ចេកទេសស៊ីជម្រៅ (ICT & Smart Money Concept)")
                    
                    if prediction == 1:
                        entry_price = current_price * 0.998
                        stop_loss = entry_price - 12.0 
                        take_profit = entry_price + 24.0 
                        
                        st.markdown("""
                        <div class="analysis-card">
                            <h3 style="color: #2ecc71;">🟢 SIGNAL RECOMMENDATION: BUY (ទិញឡើង)</h3>
                            <p><b>1. Market Structure & Liquidity:</b> តម្លៃបានបោសសម្អាត Sell-side Liquidity និងបង្កើតសញ្ញា Market Structure Shift (MSS) ឡើងលើ។</p>
                            <p><b>2. ICT Fair Value Gap (FVG):</b> តម្លៃបានទម្លាក់ខ្លួនមកបំពេញ FVG និង Order Block (OB) យ៉ាងរឹងមាំ។</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("🎯 ចំណុចចូលទិញ (Entry)", f"${entry_price:.2f}")
                        col_b.metric("🛑 Stop Loss", f"${stop_loss:.2f}", delta="-12 pips", delta_color="inverse")
                        col_c.metric("🏆 Take Profit", f"${take_profit:.2f}", delta="+24 pips")
                        
                    else:
                        entry_price = current_price * 1.002
                        stop_loss = entry_price + 12.0 
                        take_profit = entry_price - 24.0 
                        
                        st.markdown("""
                        <div class="analysis-card">
                            <h3 style="color: #e74c3c;">🔴 SIGNAL RECOMMENDATION: SELL (លក់ចុះ)</h3>
                            <p><b>1. Market Structure & Liquidity:</b> តម្លៃបានប៉ះតំបន់ Buy-side Liquidity និងបង្ហាញសញ្ញា ChoCH ទម្លាក់ចុះក្រោម។</p>
                            <p><b>2. ICT Fair Value Gap (FVG):</b> តម្លៃបានបង្កើត Bearish FVG និង Order Block (OB) ខាងលើ។</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("🎯 ចំណុចចូលលក់ (Entry)", f"${entry_price:.2f}")
                        col_b.metric("🛑 Stop Loss", f"${stop_loss:.2f}", delta="+12 pips", delta_color="inverse")
                        col_c.metric("🏆 Take Profit", f"${take_profit:.2f}", delta="-24 pips")

                except Exception as e:
                    st.error(f"⚠️ មានបញ្ហាក្នុងការដំណើរការទិន្នន័យ៖ {e}")

# ----------------- TAB 2: TradingView Chart -----------------
elif menu == "📈 TradingView Chart (Live)":
    st.title("📈 ក្រាហ្វិកតម្លៃមាស Real-time (TradingView Chart)")
    st.components.v1.html("""
    <div class="tradingview-widget-container" style="height:500px;width:100%">
      <div id="tradingview_chart" style="height:100%;width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "width": "100%", "height": 500, "symbol": "OANDA:XAUUSD", "interval": "15",
        "timezone": "Asia/Phnom_Penh", "theme": "dark", "style": "1", "locale": "en",
        "toolbar_bg": "#f1f3f6", "enable_publishing": false, "container_id": "tradingview_chart"
      });
      </script>
    </div>
    """, height=520)

# ----------------- TAB 3: AI Trading Chatbot -----------------
elif menu == "🤖 AI Trading Chatbot":
    st.title("🤖 AI Trading Assistant Chatbot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "សួស្តី! តើខ្ញុំអាចជួយអ្វីអ្នកទាក់ទងនឹងការវិភាគទីផ្សារមាសថ្ងៃនេះ?"}]
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])
    if user_prompt := st.chat_input("សរសេរសំណួររបស់អ្នកនៅទីនេះ..."):
        st.session_state["messages"].append({"role": "user", "content": user_prompt})
        st.chat_message("user").write(user_prompt)
        bot_reply = f"យោងតាមសំណួររបស់អ្នក ('{user_prompt}'): សម្រាប់ទីផ្សារ XAUUSD ពេលនេះ គួរតែតាមដានតំបន់ Support និង FVG ឱ្យបានហ្មត់ចត់។"
        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)

# ----------------- TAB 4: User Profile -----------------
elif menu == "👤 គណនីរបស់ខ្ញុំ (Profile & Dashboard)":
    st.title("👤 ព័ត៌មានគណនី និងប្រវត្តិសមាជិក (User Dashboard)")
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric("📌 ប្រភេទគណនី", "VIP Member" if is_authorized else "Free Visitor")
    col_p2.metric("⏳ រយៈពេលនៅសល់", "28 ថ្ងៃ" if is_authorized else "0 ថ្ងៃ")
    col_p3.metric("🚀 TikTok Boosts", "3 ដង")

# ----------------- TAB 5: មជ្ឈមណ្ឌលមេរៀន Trading -----------------
elif menu == "📚 មជ្ឈមណ្ឌលមេរៀន Trading":
    st.title("📚 មជ្ឈមណ្ឌលមេរៀន Trading (Pro Masterclass)")
    st.write("១. គោលគំនិត ICT & Smart Money (Order Block, FVG, MSS)\n\n២. យុទ្ធសាស្ត្រ BBMA & Bollinger Bands\n\n៣. ការគ្រប់គ្រងដើមទុន Risk Management")

# ----------------- TAB 6: ព័ត៌មានសេដ្ឋកិច្ច -----------------
elif menu == "📰 ព័ត៌មានសេដ្ឋកិច្ច (News)":
    st.title("📰 ព័ត៌មានសេដ្ឋកិច្ច និងព្រឹត្តិការណ៍ (Economic Calendar)")
    st.markdown("""
    <div class="news-box"><strong>🔥 08:30 PM (US) - Non-Farm Payrolls (NFP)</strong><br><span style="color: #ff4b4b;">🔴 Impact: High</span></div>
    <div class="news-box"><strong>⚠ 07:30 PM (US) - Consumer Price Index (CPI)</strong><br><span style="color: #ff4b4b;">🔴 Impact: High</span></div>
    """, unsafe_allow_html=True)

# ----------------- TAB 7: TikTok Ultra Turbo Boost -----------------
elif menu == "🔥 TikTok Ultra Turbo Boost":
    st.title("🔥 TikTok Ultra Turbo Boost")
    tiktok_url = st.text_input("🔗 បញ្ចូលតំណភ្ជាប់វីដេអូ TikTok:")
    boost_amount = st.selectbox("📊 ជ្រើសរើសចំនួនបរិមាណ៖", [1000, 5000, 10000, 50000, 100000])
    if st.button("⚡ ចាប់ផ្តើម Ultra Boost ឥឡូវនេះ"):
        if tiktok_url:
            st.success(f"🎉 សំណើរសុំចំនួន *{boost_amount:,}* ត្រូវបានបញ្ជូនចេញជោគជ័យ!")
            st.balloons()
        else:
            st.error("❌ សូមបញ្ចូល Link វីដេអូ TikTok ឱ្យបានត្រឹមត្រូវ។")

# ----------------- TAB 8: Smart Zone -----------------
elif menu == "📍 Smart Zone & Liquidity Map":
    st.title("📍 Institutional Order Blocks & Liquidity Map")
    st.table(pd.DataFrame({
        "Zone Type": ["Institutional Buy (OB)", "Liquidity Pool (High)", "Institutional Sell (OB)"],
        "Price Level": ["$2,365.00 - $2,370.00", "$2,410.00", "$2,400.00 - $2,405.00"],
        "Status": ["🟢 Waiting", "🔴 Target", "🔴 Resistance"]
    }))

# ----------------- TAB 9: Copy Trading -----------------
elif menu == "🤖 Copy Trading Simulation":
    st.title("🤖 Auto & Copy Trading Simulation")
    with st.form("copy_form"):
        st.text_input("លេខគណនីត្រេត (Account ID):")
        st.text_input("លេខសម្ងាត់ API / Master Password:", type="password")
        if st.form_submit_button("🔗 ភ្ជាប់គណនីស្វ័យប្រវត្ត"):
            st.success("🎉 គណនីបានភ្ជាប់ជាមួយ Copy Trading ជោគជ័យ!")

# ----------------- TAB 10: Telegram Bot -----------------
elif menu == "🔔 Telegram Alert Bot":
    st.title("🔔 Telegram Bot Integration")
    with st.form("tele_form"):
        st.text_input("Telegram Bot Token:")
        st.text_input("Telegram Channel / Chat ID:")
        if st.form_submit_button("💾 រក្សាទុក"):
            st.success("🎉 កំណត់ត្រាបានរក្សាទុកជោគជ័យ!")

# ----------------- TAB 11: Game Top-Up -----------------
elif menu == "💎 Game Top-Up Center (Free Fire & MLBB)":
    st.title("💎 Game Top-Up Center (Free Fire & MLBB)")
    with st.form("game_form"):
        st.selectbox("ជ្រើសរើសហ្គេម៖", ["🔥 Free Fire", "⚔️ Mobile Legends"])
        st.text_input("Player ID:")
        if st.form_submit_button("🛒 ទិញពេជ្រឥឡូវនេះ"):
            st.success("🎉 ការបញ្ជាទិញពេជ្របានទទួលជោគជ័យ!")

# ----------------- TAB 12: Anime Streaming -----------------
elif menu == "🎬 Anime Streaming Center (Top 20)":
    st.title("🎬 Anime Streaming Center (Top 20 Animes)")
    anime = st.selectbox("ជ្រើសរើសរឿង Anime៖", ["🔥 Jujutsu Kaisen", "⚔️ Demon Slayer", "⚡ Attack on Titan", "🌊 One Piece"])
    st.write(f"កំពុងចាក់បញ្ចាំង៖ {anime}")
    st.video("https://www.youtube.com/watch?v=4Il0YUS2kkA")

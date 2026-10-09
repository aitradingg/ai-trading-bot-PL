import datetime
import pandas as pd
import numpy as np
import streamlit as st

# កំណត់ទម្រង់ទំព័រវេបសាយ (Mobile & PC Responsive)
st.set_page_config(
    page_title="XAUUSD Trading Terminal Pro",
    page_icon="⚡",
    layout="wide"
)

# 🎨 Custom CSS រចនាបទខ្មៅបែប Trading Platform (Dark Mode Pro)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #ffffff; }
    
    /* Top Header Badges */
    .header-bar {
        background-color: #161b22;
        padding: 12px 15px;
        border-radius: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }
    
    .analysis-container {
        background-color: #12161f;
        border: 1px solid #262d3d;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        margin-top: 15px;
    }
    
    .status-badge-wait {
        background-color: rgba(231, 76, 60, 0.15);
        border-left: 4px solid #e74c3c;
        padding: 15px;
        border-radius: 8px;
        color: #ffffff;
        margin-top: 15px;
    }
    
    .status-badge-buy {
        background-color: rgba(46, 204, 113, 0.15);
        border-left: 4px solid #2ecc71;
        padding: 15px;
        border-radius: 8px;
        color: #ffffff;
        margin-top: 15px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #0b0e14;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# 🚀 Top Header Section (XAUUSD Terminal Info)
st.markdown("""
    <div class="header-bar">
        <div><b>🟡 XAUUSD</b> <span style="background-color: #2ecc71; color: #000; padding: 2px 6px; border-radius: 4px; font-size: 12px; font-weight: bold;">🟢 Open</span></div>
        <div style="font-size: 18px; font-weight: bold; color: #FFD700;">$4,125.60</div>
    </div>
""", unsafe_allow_html=True)

# ⏱️ Timeframe Selector (1m, 5m, 15m, 30m, 1h, 4h, 1d)
st.markdown("<b>⏱️ ជ្រើសរើសកម្រិតពេលវេលា (Timeframe):</b>", unsafe_allow_html=True)
tf_cols = st.columns(7)
timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]

if "selected_tf" not in st.session_state:
    st.session_state["selected_tf"] = "15m"

for i, tf in enumerate(timeframes):
    with tf_cols[i]:
        if st.button(tf, key=f"tf_btn_{tf}"):
            st.session_state["selected_tf"] = tf

st.info(f"📌 Timeframe ដែលបានជ្រើសរើសបច្ចុប្បន្ន៖ **{st.session_state['selected_tf']}**")
st.markdown("---")

# 📊 ផ្នែកបង្ហាញ Chart និងផ្ទាំងវិភាគ (Analysis Dashboard)
col_chart, col_panel = st.columns([2, 1.2])

with col_chart:
    st.markdown(f"#### 📈 XAUUSD Technical Chart ({st.session_state['selected_tf']})")
    
    # គណនាក្រាហ្វិកតាម Timeframe
    np.random.seed(42)
    dates = pd.date_range(end=datetime.date.today(), periods=40, freq='H')
    base_vals = np.linspace(4120.0, 4125.60, 40)
    noise = np.random.normal(0, 2.0, 40).cumsum()
    close_prices = base_vals + noise
    
    chart_df = pd.DataFrame({
        'Price': close_prices,
        'EMA_9': pd.Series(close_prices).ewm(span=9).mean(),
    }, index=dates)

    st.line_chart(chart_df)

with col_panel:
    st.markdown("### 🔍 Terminal Control & Analysis")
    
    current_price = st.number_input("💰 តម្លៃមាសបច្ចុប្បន្ន (Live Price):", value=4125.60, step=0.1)
    current_rsi = st.slider("📊 កម្រិត RSI (14):", min_value=0.0, max_value=100.0, value=48.5)
    
    st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
    st.write("📌 **Status:** `READY FOR ANALYSIS`")
    
    # 🎛️ ប៊ូតុង Analyze និង Best Setup នៅកន្លែងតែមួយយ៉ាងច្បាស់
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        analyze_btn = st.button("📊 Analyze")
    with col_b2:
        best_setup_btn = st.button("⚡ Best setup")
        
    if analyze_btn or best_setup_btn:
        if current_rsi < 50:
            st.markdown("""
                <div class="status-badge-buy">
                    <b>🟢 SIGNAL: BUY (ទិញឡើង)</b><br>
                    <small>Support / Bullish Order Block detected | Target: +15 pips</small><br>
                    <span style="color: #2ecc71; font-size: 12px;">● Completed</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="status-badge-wait">
                    <b>⏳ WAIT TO SELL — 4,129.00</b><br>
                    <small>Watch level — resistance zone | Intraday · No expiry</small><br>
                    <span style="color: #2ecc71; font-size: 12px;">● Completed</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background-color: #1a212d; padding: 12px; border-radius: 8px; margin-top: 10px; font-size: 13px;">
                💡 សូមចុចប៊ូតុង <b>Analyze</b> ឬ <b>Best setup</b> ដើម្បីឱ្យ AI ស្កេនរកសញ្ញា Trades ជូន។
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# 📱 Bottom Navigation Bar
st.markdown("---")
nav_cols = st.columns(5)
nav_cols[0].button("🏠 Overview")
nav_cols[1].button("📊 Terminal")
nav_cols[2].button("⚡ Generate")
nav_cols[3].button("🔔 Signals")
nav_cols[4].button("👤 My Trades")

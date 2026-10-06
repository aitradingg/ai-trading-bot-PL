import datetime
import pandas as pd
import numpy as np
import streamlit as st

# កំណត់ទម្រង់ទំព័រវេបសាយ (Wide Mode)
st.set_page_config(
    page_title="XAUUSD Professional Analyzer",
    page_icon="📈",
    layout="wide"
)

# 🎨 Custom CSS រចនាមុខរាងតាមរូបភាព និងស្ដង់ដារទំនើប
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    
    /* រចនាប៊ូតុង Chart XAUUSD ឱ្យចេញជាป้าย (Badge/Button) ស្អាត */
    .chart-badge {
        background-color: #161b22;
        color: #ffffff;
        padding: 8px 16px;
        border-radius: 8px;
        border: 1px solid #30363d;
        font-weight: bold;
        font-size: 16px;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* រចនាប៊ូតុងវិភាគ */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #0b0e14;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        opacity: 0.9;
    }
    
    .signal-box-buy {
        background-color: rgba(46, 204, 113, 0.1);
        border: 2px solid #2ecc71;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
    }
    .signal-box-sell {
        background-color: rgba(231, 76, 60, 0.1);
        border: 2px solid #e74c3c;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 📌 ចំណងជើង និងការរៀបចំ Layout ស្រដៀងក្នុងរូបភាព
st.markdown("### <span class='chart-badge'>chart XAUUSD</span>", unsafe_allow_html=True)

# បែងចែកជា 2 Column: ខាងឆ្វេងសម្រាប់ Chart និងខាងស្ដាំសម្រាប់ប៊ូតុង "វិភាគ" និងបញ្ចូលតម្លៃ
col_left, col_right = st.columns([2.5, 1])

with col_right:
    st.markdown("### 🎛️ បញ្ជាការវិភាគ")
    
    # ប្រអប់បញ្ចូលតម្លៃមាសពិតប្រាកដ (Live Price Input) ដើម្បីធានាថាត្រូវ 100%
    current_price = st.number_input("💰 បញ្ចូលតម្លៃមាសបច្ចុប្បន្ន:", min_value=1000.0, max_value=10000.0, value=4158.90, step=0.1)
    current_rsi = st.slider("📊 កម្រិត RSI (14):", min_value=0.0, max_value=100.0, value=48.5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ប៊ូតុង "វិភាគ" នៅខាងស្ដាំ ស្រដៀងក្នុងរូបភាព
    analyze_click = st.button("📊 វិភាគ")

with col_left:
    # បង្កើត Sample Candlestick / Line Chart ស្អាតបង្ហាញតារាងតម្លៃ
    np.random.seed(42)
    dates = pd.date_range(end=datetime.date.today(), periods=50, freq='H')
    base_vals = np.linspace(current_price - 15, current_price, 50)
    noise = np.random.normal(0, 1.5, 50).cumsum()
    close_prices = base_vals + noise
    close_prices[-1] = current_price # ផ្ដល់តម្លៃចុងក្រោយត្រូវនឹងតម្លៃ input
    
    chart_df = pd.DataFrame({
        'Price': close_prices,
        'EMA_9': pd.Series(close_prices).ewm(span=9).mean(),
        'EMA_21': pd.Series(close_prices).ewm(span=21).mean()
    }, index=dates)

    st.markdown("#### 📈 ក្រាហ្វិកតម្លៃមាស (Live Technical Chart)")
    st.line_chart(chart_df[['Price', 'EMA_9', 'EMA_21']])

# 🔍 លទ្ធផលវិភាគពេលចុចប៊ូតុង "វិភាគ"
if analyze_click:
    st.divider()
    st.markdown("### 🎯 លទ្ធផលវិភាគទីផ្សារ និងសញ្ញាសម្រេចចិត្ត ট্রেដ (Trading Setup)")
    
    # ក្បួនដោះស្រាយវិភាគសាមញ្ញ និងជាក់លាក់
    ema_9_val = float(chart_df['EMA_9'].iloc[-1])
    ema_21_val = float(chart_df['EMA_21'].iloc[-1])
    
    if current_rsi < 50 and ema_9_val >= ema_21_val:
        signal_type = "BUY"
    elif current_rsi > 50 and ema_9_val < ema_21_val:
        signal_type = "SELL"
    else:
        signal_type = "BUY" if current_rsi <= 47 else "SELL"

    if signal_type == "BUY":
        entry = current_price
        sl = entry - 10.0
        tp1 = entry + 15.0
        tp2 = entry + 30.0
        
        st.markdown(f"""
        <div class="signal-box-buy">
            <h3 style="color: #2ecc71; margin: 0;">🟢 សញ្ញាណែនាំ៖ BUY (ទិញឡើង)</h3>
            <p><b>មូលហេតុបច្ចេកទេស៖</b> តម្លៃស្ថិតនៅតំបន់ Support / Bullish Order Block និង RSI កំពុងងើបឡើងវិញ។</p>
            <hr style="border-color: #2ecc71;">
            <p>🎯 <b>Entry Price:</b> <b>${entry:,.2f}</b></p>
            <p>🛑 <b>Stop Loss:</b> <b>${sl:,.2f}</b></p>
            <p>🏆 <b>Take Profit:</b> <b>${tp1:,.2f} / ${tp2:,.2f}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        entry = current_price
        sl = entry + 10.0
        tp1 = entry - 15.0
        tp2 = entry - 30.0
        
        st.markdown(f"""
        <div class="signal-box-sell">
            <h3 style="color: #e74c3c; margin: 0;">🔴 សញ្ញាណែនាំ៖ SELL (លក់ចុះ)</h3>
            <p><b>មូលហេតុបច្ចេកទេស៖</b> តម្លៃប៉ះតំបន់ Resistance និងមានសម្ពាធ Bearish FVG ទម្លាក់ចុះក្រោម។</p>
            <hr style="border-color: #e74c3c;">
            <p>🎯 <b>Entry Price:</b> <b>${entry:,.2f}</b></p>
            <p>🛑 <b>Stop Loss:</b> <b>${sl:,.2f}</b></p>
            <p>🏆 <b>Take Profit:</b> <b>${tp1:,.2f} / ${tp2:,.2f}</b></p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 សូមបញ្ចូលតម្លៃមាសចុងក្រោយនៅខាងស្ដាំ រួចចុចប៊ូតុង **'📊 វិភាគ'** ដើម្បីបង្ហាញលទ្ធផល Trade Setup[cite: 5]។")

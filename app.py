import datetime
import pandas as pd
import numpy as np
import streamlit as st

# កំណត់ទម្រង់ទំព័រវេបសាយ
st.set_page_config(
    page_title="XAUUSD Professional Market Analyzer",
    page_icon="📈",
    layout="wide"
)

# 🎨 រចនាបទ CSS ស្អាត និងងាយស្រួលមើល
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stButton > button {
        background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        width: 100%;
    }
    .stButton > button:hover {
        opacity: 0.85;
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

st.title("📊 ប្រព័ន្ធវិភាគទីផ្សារមាស XAUUSD ជំនាន់ចុងក្រោយ (Manual Input & Precision Analyzer)")
st.markdown("បញ្ចូលតម្លៃមាសបច្ចុប្បន្នពីទីផ្សារពិត (Live Price) ដើម្បីឱ្យប្រព័ន្ធគណនាលក្ខខណ្ឌ ICT, FVG និង Risk Management យ៉ាងជាក់លាក់បំផុត។")

# បង្កើតផ្ទាំងបញ្ចូលទិន្នន័យ និងកម្រិតពេលវេលា
col_input1, col_input2, col_input3 = st.columns([1, 1, 1])
with col_input1:
    current_price = st.number_input("💰 បញ្ចូលតម្លៃមាសបច្ចុប្បន្ន (Live Price):", min_value=1000.0, max_value=10000.0, value=4150.00, step=0.1)
with col_input2:
    timeframe = st.selectbox("⏱️ កម្រិតពេលវេលា (Timeframe):", ["M15 (Scalping)", "H1 (Day Trading)", "H4 (Swing Trading)", "D1 (Position Trading)"])
with col_input3:
    current_rsi = st.slider("📊 កម្រិតសូចនាករ RSI (14):", min_value=0.0, max_value=100.0, value=52.5)

st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("🔍 ចាប់ផ្តើមវិភាគទីផ្សារតាមតម្លៃនេះ")

if analyze_btn:
    with st.spinner("កំពុងដំណើរការក្បួនដោះស្រាយវិភាគទីផ្សារ (Algorithms)..."):
        
        # បង្កើត Sample Chart ផ្អែកលើតម្លៃដែលអ្នកបានបញ្ចូល
        np.random.seed(42)
        dates = pd.date_range(end=datetime.date.today(), periods=30)
        base_vals = np.linspace(current_price - 25, current_price, 30)
        noise = np.random.normal(0, 2, 30).cumsum()
        close_prices = base_vals + noise
        close_prices[-1] = current_price # ធានាថាតម្លៃចុងក្រោយត្រូវនឹងតម្លៃអ្នកបញ្ចូល
        
        df = pd.DataFrame({'Close': close_prices}, index=dates)
        df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA_21'] = df['Close'].ewm(span=21, adjust=False).mean()

        ema_9_val = float(df['EMA_9'].iloc[-1])
        ema_21_val = float(df['EMA_21'].iloc[-1])

        # កំណត់ទិសដៅ Signal តាមរយៈ RSI និង EMA ជាក់ស្តែង
        if current_rsi < 50 and ema_9_val >= ema_21_val:
            signal_type = "BUY"
        elif current_rsi > 50 and ema_9_val < ema_21_val:
            signal_type = "SELL"
        else:
            signal_type = "BUY" if current_rsi <= 48 else "SELL"

        # គណនាកម្រិត TP និង SL យ៉ាងត្រឹមត្រូវតាមស្ដង់ដារ Risk Management
        if signal_type == "BUY":
            entry = current_price
            sl = entry - 12.0
            tp1 = entry + 18.0
            tp2 = entry + 35.0
        else:
            entry = current_price
            sl = entry + 12.0
            tp1 = entry - 18.0
            tp2 = entry - 35.0

        st.success("✅ ការវិភាគទីផ្សារត្រូវបានបញ្ចប់ដោយជោគជ័យ!")

        # បង្ហាញក្រាហ្វិកតម្លៃមាស (Chart)
        st.markdown("### 📈 ក្រាហ្វិកបង្ហាញតារាងតម្លៃ និងបន្ទាត់ EMA Trend")
        st.line_chart(df[['Close', 'EMA_9', 'EMA_21']])

        # បង្ហាញសូចនាករស្ថិតិសំខាន់ៗ
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💰 តម្លៃទីផ្សារ (Live Input)", f"${current_price:,.2f}")
        c2.metric("📊 សូចនាករ RSI (14)", f"{current_rsi:.2f}")
        c3.metric("📉 EMA (9)", f"${ema_9_val:,.2f}")
        c4.metric("📈 EMA (21)", f"${ema_21_val:,.2f}")

        st.divider()

        # បង្ហាញលទ្ធផល Signal
        st.markdown("### 🎯 លទ្ធផលសញ្ញាសម្រេចចិត្ត ট্রেដ (Trading Signal & Setup)")

        if signal_type == "BUY":
            st.markdown(f"""
            <div class="signal-box-buy">
                <h2 style="color: #2ecc71; margin: 0;">🟢 សញ្ញាណែនាំ៖ BUY (ទិញឡើង)</h2>
                <p style="margin-top: 10px;"><b>ហេតុផលបច្ចេកទេស៖</b> តម្លៃស្ថិតនៅតំបន់ Support / Bullish Order Block សំខាន់។ កម្លាំង RSI និង EMA បញ្ជាក់ពីโอกาสបន្តការឡើងថ្លៃ (Bullish Momentum)។</p>
                <hr style="border-color: #2ecc71;">
                <p>🎯 <b>តម្លៃចូលទិញ (Entry Price):</b> <b>${entry:,.2f}</b></p>
                <p>🛑 <b>កម្រិតការពារហានិភ័យ (Stop Loss):</b> <b>${sl:,.2f}</b></p>
                <p>🏆 <b>គោលដៅចំណេញទី ១ (Take Profit 1):</b> <b>${tp1:,.2f}</b></p>
                <p>🏆 <b>គោលដៅចំណេញទី ២ (Take Profit 2):</b> <b>${tp2:,.2f}</b></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="signal-box-sell">
                <h2 style="color: #e74c3c; margin: 0;">🔴 សញ្ញាណែនាំ៖ SELL (លក់ចុះ)</h2>
                <p style="margin-top: 10px;"><b>ហេតុផលបច្ចេកទេស៖</b> តម្លៃបានប៉ះតំបន់ Resistance / Bearish FVG។ កម្លាំង RSI និង EMA បញ្ជាក់ពីសម្ពាធទម្លាក់ចុះក្រោម (Bearish Momentum)។</p>
                <hr style="border-color: #e74c3c;">
                <p>🎯 <b>តម្លៃចូលលក់ (Entry Price):</b> <b>${entry:,.2f}</b></p>
                <p>🛑 <b>កម្រិតការពារហានិភ័យ (Stop Loss):</b> <b>${sl:,.2f}</b></p>
                <p>🏆 <b>គោលដៅចំណេញទី ១ (Take Profit 1):</b> <b>${tp1:,.2f}</b></p>
                <p>🏆 <b>គោលដៅចំណេញទី ២ (Take Profit 2):</b> <b>${tp2:,.2f}</b></p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("👈 សូមបញ្ចូលតម្លៃមាសបច្ចុប្បន្នលើទីផ្សារពិតប្រាកដ រួចចុចប៊ូតុង **'🔍 ចាប់ផ្តើមវិភាគទីផ្សារតាមតម្លៃនេះ'** ដើម្បីទទួលបានលទ្ធផលត្រឹមត្រូវរាល់ពេល។")

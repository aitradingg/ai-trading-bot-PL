import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. កំណត់ Configuration ទំព័រ Streamlit
st.set_page_config(
    page_title="XAUUSD AI Vision Analyzer",
    page_icon="🧠",
    layout="wide"
)

# 2. រចនាបទ Custom CSS ស្អាត និងទាន់សម័យ (Dark Mode Terminal)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #ffffff; }
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #0b0e14;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        width: 100%;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(255, 215, 0, 0.5);
    }
    .result-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar កន្លែងបញ្ចូល Gemini API Key
st.sidebar.title("⚙️ AI Vision Settings")
api_key = st.sidebar.text_input("🔑 បញ្ចូល Gemini API Key របស់អ្នក:", type="password")
st.sidebar.markdown("""
---
💡 **របៀបយក API Key ឥតគិតថ្លៃ:**
1. ចូលទៅកាន់ [Google AI Studio](https://aistudio.google.com/)
2. ចុចយក **Get API Key**
3. ចម្លង API Key មក Paste ដាក់ក្នុងប្រអប់ខាងលើជាការស្រេច!
""")

st.title("🧠 XAUUSD AI Vision Market Analyzer (Chart-to-Trade Engine)")
st.markdown("ទម្លាក់/Upload រូបភាព **Trading Chart (XAUUSD)** របស់អ្នកចូលទីនេះ ដើម្បីឱ្យ AI ពិនិត្យមើល Price Action, ICT/SMC ព្រមទាំងទាញយក **Entry, TP, SL** ដោយស្វ័យប្រវត្តិ។")

st.divider()

# 4. កន្លែង Upload រូបភាព Chart
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### 📤 ១. ទម្លាក់រូបភាព Chart (Screenshot)")
    uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាព Chart (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 រូបភាព Chart ដែលបាន Upload", use_container_width=True)

with col2:
    st.markdown("### 🎛️ ២. ការកំណត់ការវិភាគ")
    timeframe = st.selectbox("⏱️ Timeframe នៃ Chart ក្នុងរូបភាព:", ["M15 (Scalping)", "H1 (Day Trading)", "H4 (Swing Trading)", "D1 (Position)"])
    trading_style = st.selectbox("🎯 យុទ្ធសាស្ត្រវិភាគ:", ["ICT / Smart Money Concepts (SMC)", "Price Action & Trendlines", "RSI / Indicator Divergence"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 ចាប់ផ្តើមឱ្យ AI វិភាគរូបភាពឥឡូវនេះ")

# 5. ដំណើរការវិភាគរូបភាពដោយប្រើ Gemini LLM Vision
if analyze_btn:
    if not api_key:
        st.error("⚠️ សូមបញ្ចូល Gemini API Key នៅ Sidebar ខាងឆ្វេងជាមុនសិន!")
    elif uploaded_file is None:
        st.warning("⚠️ សូម Upload រូបភាព Chart ជាមុនសិន înainte ចុចវិភាគ!")
    else:
        with st.spinner("🧠 AI កំពុងពិនិត្យមើលCandlestick, Order Block, FVG, និងកំណត់ Entry/TP/SL..."):
            try:
                # Configure AI Model
                genai.configure(api_key=api_key)
                model = genai.GenerativeAIModel('gemini-1.5-flash')
                
                # Prompt សំខាន់សម្រាប់បញ្ជាឱ្យ AI គិតដូច Professional Trader
                system_prompt = f"""
You are an expert institutional Forex & Gold (XAUUSD) Trader specializing in ICT (Smart Money Concepts), Price Action, and Market Structure Analysis.

Analyze the uploaded XAUUSD chart image in detail for Timeframe: {timeframe} using strategy: {trading_style}.

Please analyze the chart and provide your response in clear, structured Khmer language (ភាសាខ្មែរ) with the following format:

---
### 📊 1. ការសម្គាល់រចនាសម្ព័ន្ធទីផ្សារ (Market Structure)
- **Trend បច្ចុប្បន្ន:** (Bullish / Bearish / Sideways)
- **តំបន់គន្លឹះ (Key Levels):** (Order Block, Fair Value Gap (FVG), Support/Resistance, Liquidity Pools)

### 🎯 2. សញ្ញាណែនាំជួញដូរ (Trading Setup)
- **Signal:** [BUY / SELL / WAIT (រង់ចាំ)]
- **🎯 ចំណុចចូល (Entry Price):** $....
- **🛑 ការពារហានិភ័យ (Stop Loss - SL):** $....
- **🏆 គោលដៅប្រាក់ចំណេញ 1 (Take Profit 1 - TP1):** $....
- **🏆 គោលដៅប្រាក់ចំណេញ 2 (Take Profit 2 - TP2):** $....

### 🧠 3. ហេតុផលបច្ចេកទេសស៊ីជម្រៅ (Technical Analysis Reason)
- រៀបរាប់ហេតុផលយ៉ាងលម្អិតថាហេតុអ្វីបានជាត្រូវ Buy ឬ Sell ផ្អែកលើរូបភាព Candle, Liquidity Sweep ឬ FVG ក្នុង Chart នេះ។
---
Provide precise price levels visible in the image. Be clear, direct, and practical.
"""

                # ផ្ញើ Prompt និងរូបភាពទៅកាន់ Gemini Vision
                response = model.generate_content([system_prompt, image])
                
                st.success("✅ ការវិភាគរូបភាពត្រូវបានបញ្ចប់!")
                st.markdown("---")
                st.markdown("## 📋 លទ្ធផលការវិភាគពី AI Vision Engine")
                st.markdown(f'<div class="result-card">{response.text}</div>', unsafe_allow_html=True)

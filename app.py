import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. កំណត់ទម្រង់ទំព័រវេបសាយ
st.set_page_config(
    page_title="XAUUSD Master Vision Trader",
    page_icon="🧠",
    layout="wide"
)

# 2. រចនាបទ CSS ទំនើបបែប Professional Terminal
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
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        opacity: 0.9;
    }
    .result-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar សម្រាប់បញ្ចូល API Key
st.sidebar.title("⚙️ AI Vision Configuration")
api_key = st.sidebar.text_input("🔑 បញ្ចូល Gemini API Key:", type="password")
st.sidebar.markdown("""
---
💡 **របៀបយក API Key ដោយឥតគិតថ្លៃ:**
1. ចូលទៅកាន់ [Google AI Studio](https://aistudio.google.com/)
2. ចុចយក **Get API Key**
3. យកមក Paste ដាក់ក្នុងប្រអប់ខាងលើ។
""")

st.title("🧠 XAUUSD AI Master Vision Analyzer (Chart-to-Trade)")
st.markdown("ទម្លាក់រូបភាព **Chart XAUUSD** របស់អ្នកចូលទីនេះ ដើម្បីឱ្យខួរក្បាល AI វិភាគកម្រិតខ្ពស់តាមបែប ICT/Price Action និងထုတ်ចេញជាតម្លៃ **Entry, TP, SL** យ៉ាងแม่นยำ។")

st.divider()

# 4. Layout សម្រាប់ Upload រូបភាព និងកំណត់ Option
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 📤 ១. Upload រូបភាព Chart (Screenshot)")
    uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាព Chart (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 រូបភាព Chart ដែលបានជ្រើសរើស", use_container_width=True)

with col_right:
    st.markdown("### 🎛️ ២. ការកំណត់ការវិភាគ")
    timeframe = st.selectbox("⏱️ កម្រិតពេលវេលា (Timeframe):", ["M15 (Scalping)", "H1 (Day Trading)", "H4 (Swing Trading)", "D1 (Position)"])
    trading_style = st.selectbox("🎯 យុទ្ធសាស្ត្រវិភាគ:", ["ICT (Order Block & FVG)", "Price Action & Trendlines", "Support & Resistance / Liquidity"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 ឱ្យ AI វិភាគរូបភាព Chart នេះឥឡូវនេះ")

# 5. ដំណើរការវិភាគដោយប្រើ Gemini Vision
if analyze_btn:
    if not api_key:
        st.error("⚠️ សូមបញ្ចូល Gemini API Key នៅ Sidebar ខាងឆ្វេងជាមុនសិន!")
    elif uploaded_file is None:
        st.warning("⚠️ សូម Upload រូបភាព Chart ចូលជាមុនសិន ទើបអាចចុចវិភាគបាន!")
    else:
        with st.spinner("🧠 AI កំពុងវិភាគទម្រង់ទៀន (Candlestick), Order Block, FVG និងគណនា TP/SL..."):
            try:
                genai.configure(api_key=api_key)
                
                # ប្រើប្រាស់โมเดล gemini-1.5-flash ដែលមានសមត្ថភាពខ្លាំងខាង Vision
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Prompt បញ្ជាឱ្យ AI គិតដូច Professional Trader
                prompt = f"""
You are an expert institutional Forex & Gold (XAUUSD) Trader and ICT (Smart Money Concepts) master.
Analyze this XAUUSD chart image thoroughly for Timeframe: {timeframe} and Strategy: {trading_style}.

Provide your professional market breakdown and trading setup clearly in **Khmer language (ភាសាខ្មែរ)** following this structure:

---
### 📊 1. ការវិភាគរចនាសម្ព័ន្ធទីផ្សារ (Market Structure)
- **Trend បច្ចុប្បន្ន:** (Bullish / Bearish / Sideways)
- **តំបន់គន្លឹះ (Key Zones):** (Order Block, Fair Value Gap (FVG), Support/Resistance, Liquidity Pools ที่ເຫັນໃນរូប)

### 🎯 2. កម្រិតពាណិជ្ជកម្ម (Trading Setup)
- **សញ្ញាណែនាំ (Signal):** [BUY / SELL / WAIT]
- **🎯 ចំណុចចូល (Entry Price):** $....
- **🛑 ការពារហានិភ័យ (Stop Loss - SL):** $....
- **🏆 គោលដៅប្រាក់ចំណេញ ១ (Take Profit 1 - TP1):** $....
- **🏆 គោលដៅប្រាក់ចំណេញ ២ (Take Profit 2 - TP2):** $....

### 🧠 3. មូលហេតុបច្ចេកទេស (Technical Reasoning)
- ពន្យល់លម្អិតជាភាសាខ្មែរថាហេតុអ្វីបានជាសម្រេចចិត្ត BUY ឬ SELL ផ្អែកលើរូបភាព Chart នេះ (ឧ. ការបោស liquidity, การเด้ງចេញពី OB, ឬការទម្លុះ BOS)។
---
Be extremely precise with price numbers visible or estimated from the chart context.
"""

                response = model.generate_content([prompt, image])
                
                st.success("✅ ការវិភាគដោយ AI Vision ត្រូវបានបញ្ចប់ដោយជោគជ័យ!")
                st.markdown("---")
                st.markdown("## 📋 លទ្ធផលវិភាគស៊ីជម្រៅពី AI Master Trader")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ មានបញ្តាក្នុងការតភ្ជាប់ជាមួយ AI: {e}")

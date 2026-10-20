import streamlit as st
from PIL import Image
import google.generativeai as genai

# កំណត់ទម្រង់ទំព័រវេបសាយ
st.set_page_config(
    page_title="XAUUSD AI Vision Analyzer",
    page_icon="📈",
    layout="centered"
)

st.title("📈 XAUUSD Chart Vision Analyzer")
st.markdown("ទម្លាក់រូបភាព **Chart XAUUSD** របស់អ្នកចូលខាងក្រោម ដើម្បីឱ្យ AI វិភាគ និងបង្ហាញតម្លៃ Entry, TP, SL យ៉ាងត្រឹមត្រូវដោយស្វ័យប្រវត្តិ។")

# ដាក់ API Key របស់អ្នកផ្ទាល់នៅទីនេះ ដើម្បីមិនបាច់វាយបញ្ចូលម្ដងទៀតពេលប្រើ
# (ជំនួសអត្ថបទ YOUR_GEMINI_API_KEY ដោយ API Key ពិតប្រាកដរបស់អ្នក)
HARDCODED_API_KEY = "YOUR_GEMINI_API_KEY"

# កន្លែង Upload រូបភាព Chart
uploaded_file = st.file_uploader("📤 ជ្រើសរើសរូបភាព Chart (PNG, JPG):", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 រូបភាព Chart ដែលបានជ្រើសរើស", use_container_width=True)
    
    if st.button("🔍 វិភាគទីផ្សារឥឡូវនេះ"):
        if HARDCODED_API_KEY == "YOUR_GEMINI_API_KEY":
            st.error("⚠️ សូមជំនួស 'YOUR_GEMINI_API_KEY' ក្នុងកូដដោយ API Key របស់អ្នកជាមុនសិន!")
        else:
            with st.spinner("🧠 AI កំពុងវិភាគរចនាសម្ព័ន្ធទីផ្សារ និងគណនា TP/SL..."):
                try:
                    genai.configure(api_key=HARDCODED_API_KEY)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = """
You are an expert institutional Gold (XAUUSD) Trader and ICT/Price Action master.
Analyze this XAUUSD chart image thoroughly. 

Provide your professional analysis clearly in **Khmer language (ភាសាខ្មែរ)** using this exact format:

---
### 📊 1. ការវិភាគរចនាសម្ព័ន្ធទីផ្សារ (Market Structure)
- **Trend បច្ចុប្បន្ន:** (Bullish / Bearish / Sideways)
- **តំបន់គន្លឹះ (Key Zones):** (Order Block, FVG, Support/Resistance)

### 🎯 2. កម្រិតពាណិជ្ជកម្ម (Trading Setup)
- **សញ្ញាណែនាំ (Signal):** [BUY / SELL]
- **🎯 Entry Price:** $....
- **🛑 Stop Loss (SL):** $....
- **🏆 Take Profit 1 (TP1):** $....
- **🏆 Take Profit 2 (TP2):** $....

### 🧠 3. មូលហេតុបច្ចេកទេស (Technical Reasoning)
- ពន្យល់សង្ខេបជាភាសាខ្មែរពីមូលហេតុនៃការសម្រេចចិត្តនេះ។
---
"""
                    response = model.generate_content([prompt, image])
                    
                    st.success("✅ ការវិភាគបានជោគជ័យ!")
                    st.markdown("### 📋 លទ្ធផលវិភាគពី AI:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"❌ កំហុសឆ្គង: {e}")

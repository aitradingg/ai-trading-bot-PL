import streamlit as st
from PIL import Image
import google.generativeai as genai

# កំណត់ទម្រង់ទំព័រវេបសាយ
st.set_page_config(
    page_title="XAUUSD AI Chart Analyzer",
    page_icon="📈",
    layout="centered"
)

st.title("📈 XAUUSD Chart Vision Analyzer")
st.markdown("ទម្លាក់រូបភាព **Chart XAUUSD** របស់អ្នកចូលខាងក្រោម ដើម្បីឱ្យ AI វិភាគ និងបង្ហាញតម្លៃ Entry, TP, SL យ៉ាងត្រឹមត្រូវ។")

# ទាញយក API Key ពី st.secrets ដោយសុវត្ថិភាពខ្ពស់
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# បើគ្មានក្នុង secrets ទេ ផ្តល់ប្រអប់បញ្ចូលសុវត្ថិភាពនៅ Sidebar
if not api_key:
    api_key = st.sidebar.text_input("🔑 Gemini API Key:", type="password")

# កន្លែង Upload រូបភាព Chart
uploaded_file = st.file_uploader("📤 ជ្រើសរើសរូបភាព Chart (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 រូបភាព Chart ដែលបានជ្រើសរើស", use_container_width=True)
    
    if st.button("🔍 វិភាគទីផ្សារឥឡូវនេះ"):
        if not api_key:
            st.error("⚠️ សូមកំណត់ Gemini API Key ជាមុនសិន (អាចដាក់ក្នុង Streamlit Secrets ឬ Sidebar)!")
        else:
            with st.spinner("🧠 AI កំពុងវិភាគរចនាសម្ព័ន្ធទីផ្សារ និងគណនា TP/SL..."):
                try:
                    genai.configure(api_key=api_key)
                    # ប្រើប្រាស់โมเดល gemini-1.5-flash ដែលមានសមត្ថភាពខ្ពស់លើការមើលរូបភាព
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

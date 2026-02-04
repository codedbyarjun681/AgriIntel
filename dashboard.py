import streamlit as st
from recommendation import get_crop_and_fertilizer_recommendation
from groq import Groq

# =========================================================
# ✅ MUST BE FIRST STREAMLIT COMMAND
# =========================================================
st.set_page_config(
    page_title="Smart Agriculture System",
    layout="wide"
)

# =========================================================
# 1. Language Translations
# =========================================================
LANGUAGES = {
    "English": {
        "title": "Smart Agriculture Recommendation System",
        "subtitle": "Enter your farm's data to receive a comprehensive analysis powered by our AI and a free Large Language Model.",
        "sidebar_header": "Enter Sensor & Climate Data",
        "n_label": "Nitrogen (N) Content (kg/ha)",
        "p_label": "Phosphorus (P) Content (kg/ha)",
        "k_label": "Potassium (K) Content (kg/ha)",
        "temp_label": "Temperature (°C)",
        "humidity_label": "Humidity (%)",
        "ph_label": "Soil pH",
        "rainfall_label": "Rainfall (mm)",
        "button_text": "Generate Comprehensive Report",
        "report_header": "Your Comprehensive Agricultural Report",
        "spinner_text": "Analyzing data and generating your report...",
        "info_text": "Please enter your farm's data in the sidebar and click 'Generate Comprehensive Report'."
    },
    "हिन्दी (Hindi)": {
        "title": "स्मार्ट कृषि सिफारिश प्रणाली",
        "subtitle": "AI द्वारा संचालित व्यापक विश्लेषण प्राप्त करने के लिए अपने खेत का डेटा दर्ज करें।",
        "sidebar_header": "सेंसर और जलवायु डेटा दर्ज करें",
        "n_label": "नाइट्रोजन (N) सामग्री (किग्रा/हेक्टेयर)",
        "p_label": "फॉस्फोरस (P) सामग्री (किग्रा/हेक्टेयर)",
        "k_label": "पोटेशियम (K) सामग्री (किग्रा/हेक्टेयर)",
        "temp_label": "तापमान (°C)",
        "humidity_label": "आर्द्रता (%)",
        "ph_label": "मिट्टी का pH",
        "rainfall_label": "वर्षा (मिमी)",
        "button_text": "व्यापक रिपोर्ट तैयार करें",
        "report_header": "आपकी व्यापक कृषि रिपोर्ट",
        "spinner_text": "डेटा का विश्लेषण किया जा रहा है...",
        "info_text": "कृपया साइडबार में अपने खेत का डेटा दर्ज करें।"
    },
    "বাংলা (Bengali)": {
        "title": "স্মার্ট কৃষি সুপারিশ সিস্টেম",
        "subtitle": "AI দ্বারা চালিত একটি বিস্তারিত বিশ্লেষণ পেতে আপনার খামারের ডেটা প্রবেশ করান।",
        "sidebar_header": "সেন্সর এবং জলবায়ু ডেটা প্রবেশ করান",
        "n_label": "নাইট্রোজেন (N) উপাদান (কেজি/হেক্টর)",
        "p_label": "ফসফরাস (P) উপাদান (কেজি/হেক্টর)",
        "k_label": "পটাশিয়াম (K) উপাদান (কেজি/হেক্টর)",
        "temp_label": "তাপমাত্রা (°C)",
        "humidity_label": "আর্দ্রতা (%)",
        "ph_label": "মাটির pH",
        "rainfall_label": "বৃষ্টিপাত (মিমি)",
        "button_text": "বিস্তারিত রিপোর্ট তৈরি করুন",
        "report_header": "আপনার বিস্তারিত কৃষি রিপোর্ট",
        "spinner_text": "ডেটা বিশ্লেষণ করা হচ্ছে...",
        "info_text": "অনুগ্রহ করে সাইডবারে আপনার খামারের ডেটা প্রবেশ করান।"
    },
    "தமிழ் (Tamil)": {
        "title": "ஸ்மார்ட் விவசாய பரிந்துரை அமைப்பு",
        "subtitle": "AI மூலம் விரிவான பகுப்பாய்வைப் பெற உங்கள் பண்ணை தரவை உள்ளிடவும்.",
        "sidebar_header": "சென்சார் மற்றும் காலநிலை தரவை உள்ளிடவும்",
        "n_label": "நைட்ரஜன் (N) உள்ளடக்கம் (கிலோ/ஹெக்டேர்)",
        "p_label": "பாஸ்பரஸ் (P) உள்ளடக்கம் (கிலோ/ஹெக்டேர்)",
        "k_label": "பொட்டாசியம் (K) உள்ளடக்கம் (கிலோ/ஹெக்டேர்)",
        "temp_label": "வெப்பநிலை (°C)",
        "humidity_label": "ஈரப்பதம் (%)",
        "ph_label": "மண் pH",
        "rainfall_label": "மழைப்பொழிவு (மிமீ)",
        "button_text": "விரிவான அறிக்கையை உருவாக்கவும்",
        "report_header": "உங்கள் விரிவான விவசாய அறிக்கை",
        "spinner_text": "தரவு பகுப்பாய்வு செய்யப்படுகிறது...",
        "info_text": "பக்கப்பட்டியில் உங்கள் பண்ணை தரவை உள்ளிடவும்."
    },
    "తెలుగు (Telugu)": {
        "title": "స్మార్ట్ వ్యవసాయ సిఫార్సు వ్యవస్థ",
        "subtitle": "AI ద్వారా సమగ్ర విశ్లేషణను స్వీకరించడానికి మీ వ్యవసాయ క్షేత్రం డేటాను నమోదు చేయండి.",
        "sidebar_header": "సెన్సార్ మరియు వాతావరణ డేటాను నమోదు చేయండి",
        "n_label": "నత్రజని (N) కంటెంట్ (కిలోలు/హెక్టారు)",
        "p_label": "భాస్వరం (P) కంటెంట్ (కిలోలు/హెక్టారు)",
        "k_label": "పొటాషియం (K) కంటెంట్ (కిలోలు/హెక్టారు)",
        "temp_label": "ఉష్ణోగ్రత (°C)",
        "humidity_label": "తేమ (%)",
        "ph_label": "నేల pH",
        "rainfall_label": "వర్షపాతం (మిమీ)",
        "button_text": "సమగ్ర నివేదికను రూపొందించండి",
        "report_header": "మీ సమగ్ర వ్యవసాయ నివేదిక",
        "spinner_text": "డేటాను విశ్లేషిస్తోంది...",
        "info_text": "దయచేసి మీ వ్యవసాయ క్షేత్రం డేటాను నమోదు చేయండి."
    },
    "मराठी (Marathi)": {
        "title": "स्मार्ट कृषी शिफारस प्रणाली",
        "subtitle": "AI द्वारे समर्थित सर्वसमावेशक विश्लेषण मिळविण्यासाठी तुमच्या शेताचा डेटा प्रविष्ट करा.",
        "sidebar_header": "सेन्सर आणि हवामान डेटा प्रविष्ट करा",
        "n_label": "नायट्रोजन (N) सामग्री (किलो/हेक्टर)",
        "p_label": "फॉस्फरस (P) सामग्री (किलो/हेक्टर)",
        "k_label": "पोटॅशियम (K) सामग्री (किलो/हेक्टर)",
        "temp_label": "तापमान (°C)",
        "humidity_label": "आर्द्रता (%)",
        "ph_label": "मातीचा pH",
        "rainfall_label": "पर्जन्यमान (मिमी)",
        "button_text": "सर्वसमावेशक अहवाल तयार करा",
        "report_header": "तुमचा सर्वसमावेशक कृषी अहवाल",
        "spinner_text": "डेटाचे विश्लेषण होत आहे...",
        "info_text": "कृपया तुमच्या शेताचा डेटा प्रविष्ट करा."
    }
}

# =========================================================
# 2. Groq API Configuration (SAFE)
# =========================================================
client = None
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.warning("Groq API key not found. LLM report will be unavailable.")

# =========================================================
# 3. Report Generation
# =========================================================
def generate_llm_report(user_data, model_predictions, language):
    if client is None:
        return "LLM report unavailable. Please configure GROQ_API_KEY."

    if language != "English":
        language_rule = f"""
IMPORTANT RULES (MUST FOLLOW):
- Write the ENTIRE report ONLY in {language}
- DO NOT include English anywhere
- DO NOT provide bilingual or mixed-language output
- Use proper native grammar and terminology of {language}
"""
    else:
        language_rule = ""

    prompt = f"""
You are an expert agricultural scientist and agronomist.

Farmer Inputs:
- Nitrogen (N): {user_data['N']} kg/ha
- Phosphorus (P): {user_data['P']} kg/ha
- Potassium (K): {user_data['K']} kg/ha
- Soil pH: {user_data['ph']}
- Temperature: {user_data['temperature']} °C
- Humidity: {user_data['humidity']} %
- Rainfall: {user_data['rainfall']} mm

AI Model Predictions:
- Soil Health Status: {model_predictions['soil_health_status']}
- Recommended Crop: {model_predictions['recommended_crop']}
- Fertilizer Recommendation: {model_predictions['fertilizer_products']}

Generate a detailed Markdown report with:
1. Executive Summary
2. Soil Health Analysis
3. Crop Recommendation & Reasoning
4. Actionable Fertilizer Plan
5. Long-Term Soil Management
6. Estimated Yield Potential

{language_rule}
"""

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return completion.choices[0].message.content


# =========================================================
# 4. Streamlit UI
# =========================================================
selected_language = st.sidebar.selectbox(
    "Choose Language / भाषा चुनें", options=list(LANGUAGES.keys())
)
lang = LANGUAGES[selected_language]

st.title(lang["title"])
st.markdown(lang["subtitle"])

st.sidebar.header(lang["sidebar_header"])

user_inputs = {
    "N": st.sidebar.number_input(lang["n_label"], 0, 140, 20),
    "P": st.sidebar.number_input(lang["p_label"], 5, 145, 125),
    "K": st.sidebar.number_input(lang["k_label"], 5, 205, 200),
    "temperature": st.sidebar.number_input(lang["temp_label"], 0.0, 50.0, 22.0),
    "humidity": st.sidebar.number_input(lang["humidity_label"], 0.0, 100.0, 90.0),
    "ph": st.sidebar.number_input(lang["ph_label"], 0.0, 14.0, 6.0),
    "rainfall": st.sidebar.number_input(lang["rainfall_label"], 0.0, 300.0, 115.0),
}

if st.sidebar.button(lang["button_text"]):
    local_report = get_crop_and_fertilizer_recommendation(**user_inputs)
    st.subheader(lang["report_header"])
    with st.spinner(lang["spinner_text"]):
        st.markdown(
            generate_llm_report(user_inputs, local_report, selected_language)
        )
else:
    st.info(lang["info_text"])

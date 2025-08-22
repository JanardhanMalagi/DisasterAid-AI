import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder

# Page config
st.set_page_config(page_title="DisasterAid AI", page_icon="🎙️", layout="wide")

# Custom CSS
page_bg = """
<style>
.stApp {
    background: linear-gradient(to right, #A0522D, #DEB887));
    color: white;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>🎙️ Disaster Relief Suggestion System</h1>", unsafe_allow_html=True)

# Input + Voice Button
col1, col2 = st.columns([8, 1])

with col1:
    area = st.text_input("Enter Area Name:", key="city_input")

with col2:
    # 🎤 Microphone Recorder
    audio = mic_recorder(
        start_prompt="🎤 Speak",
        stop_prompt="⏹️ Stop",
        key="recorder"
    )

# If audio recorded → send to STT API (e.g. Google, Whisper, etc.)
if audio:
    st.success("✅ Voice captured successfully (now send it to Speech-to-Text API).")
    # TODO: integrate speech-to-text here
    # Example: area = speech_to_text(audio["bytes"])

# Fetch & Display Results
if area.strip():
    try:
        backend_url = f"http://127.0.0.1:5000/relief-suggestion?area={area}"
        response = requests.get(backend_url)

        if response.status_code == 200:
            data = response.json()

            if "info" in data:
                for city in data["info"]:
                    disaster_info = city.get('disaster_info', 'No disaster info available')
                    st.markdown(
                        f"**{city['city']}, {city['country']}**  \n"
                        f"Population: {city.get('population', 'N/A')}  \n"
                        f"Disaster Info: {disaster_info}"
                    )
            else:
                st.warning(data.get("message", "No data available"))

        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to backend. Please make sure Flask server is running.")

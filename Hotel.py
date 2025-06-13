import streamlit as st
import requests
import subprocess
from pathlib import Path
import base64

# Page Setup
st.set_page_config(page_title="Hotel AI Assistant", layout="wide")



with open("/Users/fairchan/Downloads/FaceRecognitionProgram-main/SecondModel/music/1.mp3", "rb") as music_file:#❗️Absolute path modification
    music_base64 = base64.b64encode(music_file.read()).decode()
with open("/Users/fairchan/Downloads/FaceRecognitionProgram-main/SecondModel/backgrounds/1.mp4", "rb") as video_file:#❗️Absolute path modification
    video_base64 = base64.b64encode(video_file.read()).decode()


video_background_html = f"""
<style>
.stApp {{
    background: transparent;
}}

#video-container {{
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    overflow: hidden;
    z-index: -1000;
}}

#video-container video {{
    min-width: 100%;
    min-height: 100%;
    object-fit: cover;
}}
</style>

<div id="video-container">
    <video autoplay muted loop playsinline>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
</div>
"""


music_html = f"""
<audio autoplay loop>
    <source src="data:audio/mp3;base64,{music_base64}" type="audio/mp3">
    Your browser does not support the audio element.
</audio>
"""

st.markdown(video_background_html + music_html, unsafe_allow_html=True)



st.title("🏨 Welcome to Hotel AI Assistant")
st.markdown("Please select a function：")

#Function Selection
option = st.radio("Function Selection", ["Check-in Face Recognition", "Chatbot Q&A on Hotel Issues"], index=0)

#Check-in function
if option == "Check-in Face Recognition":
    st.header("📸 Check-in Face Recognition")
    st.write("Click the button below to activate the camera for recognition:")

    if st.button("Start recognizing"):
        try:
            # Call the existing recognize.py as a separate process to run the camera recognition.
            subprocess.Popen(["python", "/Users/fairchan/Downloads/FaceRecognitionProgram-main/SecondModel/recognize.py"])#❗️Absolute path modification
            st.success("Camera recognition has been activated, please check the pop-up window. Press q to exit.")
        except Exception as e:
            st.error(f"❌ Startup failed:{e}")

#Chatbot
elif option == "Chatbot Q&A on Hotel Issues":
    st.header("🤖 Chatbot Hotel Assistant")
    st.write("Enter your question below and our robots will answer it for you:")

    # Welcome Content Button
    if st.button("📢 See what can be asked"):
        try:
            response = requests.get("http://127.0.0.1:5000/welcome")
            if response.status_code == 200:
                st.markdown(response.json().get("response", ""), unsafe_allow_html=True)
            else:
                st.warning("‼️Welcome message failed to load.")
        except:
            st.error("‼️Cannot connect to the Chatbot backend, make sure Flask is running.")

    # User input question
    user_input = st.text_input("✍️ Please enter your question:")
    if user_input:
        try:
            result = requests.post("http://127.0.0.1:5000/chat", json={"message": user_input})
            if result.status_code == 200:
                reply = result.json().get("response", "Sorry, the bot didn't reply.")
                st.markdown(f"🤖 responsive：**{reply}**")
            else:
                st.warning("❗️The robot did not respond correctly.")
        except:
            st.error("❗️Cannot connect to the Chatbot backend, make sure Flask is running.")

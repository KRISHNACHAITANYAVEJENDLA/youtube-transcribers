import streamlit as st
import yt_dlp
from faster_whisper import WhisperModel
import os

# Initialize model
model = WhisperModel("base", device="cpu", compute_type="int8")

# Streamlit UI setup
st.set_page_config(page_title="YouTube Transcriber", layout="centered")
st.title("🎧 YouTube Video Transcriber")
st.markdown("Paste a **YouTube URL** below and get a full transcript using Whisper.")

# Input field
url = st.text_input("📺 Enter YouTube URL:")

# On button click
if st.button("Transcribe") and url:
    with st.spinner("⏳ Downloading and transcribing... please wait."):
        try:
            # Set download path
            output_path = "downloaded_audio.%(ext)s"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
            }

            # Download audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            audio_path = output_path + ".mp3"

            # Transcribe audio
            segments, info = model.transcribe(audio_path)
            transcript = " ".join([seg.text for seg in segments])

            # Show transcript
            st.success("✅ Transcription complete!")
            st.markdown("### 📝 Transcript")
            st.text_area("", transcript, height=300)

        except Exception as e:
            st.error(f"❌ Something went wrong:\n{e}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Created by <b>V. Krishna Chaitanya</b>, <b>N. Bhuvanesh</b>, and <b>KV Pavan Kumar</b></p>",
    unsafe_allow_html=True
)

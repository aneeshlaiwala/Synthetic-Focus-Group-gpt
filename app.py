
import streamlit as st
from docx import Document
from io import BytesIO
import random

st.set_page_config(page_title="Synthetic Focus Group Transcript Generator", layout="wide")

st.markdown("## 🧠 Synthetic Focus Group Transcript Generator")
st.markdown("A professional tool for qualitative researchers to generate realistic, AI-powered discussion transcripts.")

# -----------------------------
# Session state initialization
# -----------------------------
if "moderator_prompt" not in st.session_state:
    st.session_state["moderator_prompt"] = ""

# -----------------------------
# Participant Composition
# -----------------------------
st.subheader("📂 Participant Composition")

cols = st.columns([1, 1, 1])

with cols[0]:
    total_participants = st.number_input("👥 Total Participants", min_value=1, value=6, step=1)

with cols[1]:
    male_participants = st.number_input("🧔 Male Participants", min_value=0, value=2, step=1)

with cols[2]:
    female_participants = st.number_input("👩 Female Participants", min_value=0, value=2, step=1)

non_binary_participants = total_participants - male_participants - female_participants
non_binary_participants = max(non_binary_participants, 0)

st.markdown(f"<span style='color: purple;'>🧑‍🤝‍🧑 <b>Non-Binary Participants:</b> {non_binary_participants} (auto-calculated)</span>", unsafe_allow_html=True)

# -----------------------------
# Group Profile & Session Settings
# -----------------------------
st.subheader("🌍 Group Profile & Session Settings")

location = st.text_input("City/Location (for local names)", "Mumbai")
language = st.selectbox("Discussion Language", ["English", "Hindi", "Hinglish", "Spanish", "French"])
duration = st.slider("Duration of Discussion (minutes)", min_value=10, max_value=120, value=60)
moderator_name = st.text_input("Moderator Name", "Priya")

# -----------------------------
# Moderator Prompt Editor
# -----------------------------
st.subheader("📝 Edit the Moderator Prompt")
default_prompt = f"""You are a skilled qualitative moderator. You will conduct a synthetic focus group with {total_participants} participants 
({male_participants} male, {female_participants} female, {non_binary_participants} non-binary) from {location}. The discussion will last {duration} minutes 
and be in {language}. Moderator name is {moderator_name}.

Discussion should reflect opinions typical of {location}, based on online research from multiple reliable sources. Use natural, diverse speech and personality styles. 
Add minor disagreements, digressions, local slang, and emotion. The transcript should look real, informal, and spontaneous.

Participants should have realistic names from {location} (e.g., common local names). Include filler words, interruptions, and varied grammar.

Use the following structure:
- Introduction by the moderator
- Participant introductions
- Ice-breaker round
- Key discussion themes (from real-world opinions)
- Closing remarks by the moderator

Avoid obvious AI markers. Don't use perfect grammar. Add character-specific quirks and natural transitions.
"""

st.session_state["moderator_prompt"] = st.text_area("Moderator Prompt", value=default_prompt, height=300)

# -----------------------------
# Generate Transcript
# -----------------------------
if st.button("🎬 Generate Transcript"):
    st.success("Transcript generated! (Placeholder text shown below for now)")

    transcript = f"{moderator_name}: Welcome everyone, let’s begin!
" +                  "Participant 1: Sure, excited to be here.
...
[Transcript continues...]"

    st.text_area("Generated Transcript", value=transcript, height=300)

    # Save as .txt
    txt_bytes = BytesIO()
    txt_bytes.write(transcript.encode())
    txt_bytes.seek(0)

    # Save as .docx
    doc = Document()
    doc.add_heading("Synthetic Focus Group Transcript", 0)
    for line in transcript.split("\n"):
        doc.add_paragraph(line)
    docx_bytes = BytesIO()
    doc.save(docx_bytes)
    docx_bytes.seek(0)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📄 Download as .txt", data=txt_bytes, file_name="transcript.txt", mime="text/plain")
    with col2:
        st.download_button("📄 Download as .docx", data=docx_bytes, file_name="transcript.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

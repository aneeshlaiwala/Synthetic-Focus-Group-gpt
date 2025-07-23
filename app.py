# app.py
import streamlit as st
import base64
from docx import Document
from io import BytesIO

# Page config
st.set_page_config(page_title="Synthetic FGD Generator", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #6A1B9A;'>🧠 Synthetic Focus Group Discussion Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.header("🧠 AI Engine Settings")
ai_tool = st.sidebar.selectbox("Select AI Tool", ["OpenAI", "Anthropic", "Google Gemini", "Mistral", "HuggingFace"])
model_options = {
    "OpenAI": ["gpt-4", "gpt-4o"],
    "Anthropic": ["claude-3-opus"],
    "Google Gemini": ["gemini-1.5-pro"],
    "Mistral": ["mixtral-8x7b"],
    "HuggingFace": ["llama3-8b"]
}
model = st.sidebar.selectbox("Select Model", model_options[ai_tool])
api_key = st.sidebar.text_input("Enter API Key", type="password")

# Main input form
st.subheader("👥 Participant & Session Details")
with st.form("fgd_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        num_participants = st.number_input("Number of Participants", 2, 20, 6)
        male_count = st.number_input("Male Participants", 0, num_participants, 3)
        female_count = num_participants - male_count
    with col2:
        age_range = st.text_input("Age Range", "25–35")
        location = st.text_input("Participant Location", "Mumbai, India")
    with col3:
        language = st.multiselect("Discussion Language(s)", ["English", "Hindi", "Hinglish", "French"], default=["Hinglish"])
        mode = st.selectbox("Discussion Mode", ["Online", "Offline"])
        duration_min = st.slider("Discussion Duration (minutes)", 10, 120, 60)

    topic = st.text_input("Discussion Topic", "Electric Vehicles in Tier 2 Indian Cities")
    demographic_profile = st.text_area("Demographic Profile", "Mid-income professionals, EV-aware, mix of adopters and skeptics")
    study_objective = st.text_area("Study Objective", "Understand attitudes, barriers, and motivations for EV adoption.")
    submitted = st.form_submit_button("🔍 Generate Prompt")

# Prompt builder
if submitted:
    estimated_words = int(duration_min * 140)
    prompt = f"""
You are an expert qualitative researcher. Simulate a synthetic focus group discussion transcript based on the following details:

- Location: {location}
- Number of participants: {num_participants} ({male_count} male, {female_count} female)
- Age range: {age_range}
- Languages: {", ".join(language)}
- Mode: {mode}
- Duration: {duration_min} minutes (~{estimated_words} words)
- Topic: {topic}
- Demographic profile: {demographic_profile}
- Study objective: {study_objective}

Structure the discussion into:
1. Opening (introductions, ground rules)
2. Warm-up
3. Core discussion with moderator and participant interactions
4. Closing summary

Use realistic participant names from {location}. Include occasional slang, dialect, or minor grammar imperfections based on language mix. Output as a natural, readable transcript.

Ensure moderator remains neutral and encourages varied viewpoints.
    """
    st.markdown("### 🧾 Prompt (editable before submission)")
    edited_prompt = st.text_area("✏️ Edit Prompt if Needed", prompt, height=300)
    st.session_state["final_prompt"] = edited_prompt

    if st.button("🚀 Generate Transcript (Demo Mode)"):
        # Simulated result
        transcript = f"""
MODERATOR: Welcome everyone! Let’s start by introducing ourselves.

RAHUL (Male, 28): Hi, I’m Rahul from Andheri. I work in IT. Glad to be here!

SUNITA (Female, 31): Hello! I’m Sunita, a school teacher. I’ve always been curious about electric vehicles...

...

MODERATOR: Thank you all for your insights today. This was a great discussion on {topic}.
        """.strip()

        st.markdown("### 📄 Generated Transcript")
        st.text_area("Transcript", transcript, height=300)

        # .txt download
        b64_txt = base64.b64encode(transcript.encode()).decode()
        st.download_button("⬇️ Download TXT", data=transcript, file_name="transcript.txt", mime="text/plain")

        # .docx download
        doc = Document()
        doc.add_heading("Focus Group Transcript", 0)
        for line in transcript.split("\n"):
            doc.add_paragraph(line.strip())
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button("⬇️ Download DOCX", data=buffer, file_name="transcript.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

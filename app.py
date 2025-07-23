import streamlit as st
import base64
from io import BytesIO
from docx import Document
from docx.shared import Pt
from PyPDF2 import PdfReader
import docx2txt

# Page setup
st.set_page_config(page_title="FGD Generator", layout="wide")
st.markdown("<h1 style='text-align: center; color: #6A1B9A;'>🎤 Synthetic Focus Group Discussion Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar settings
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

# Main Form
st.subheader("📋 Discussion Setup")
with st.form("fgd_form"):
    st.markdown("### 🗂️ Participant Composition")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        num_participants = st.number_input("👥 Total Participants", min_value=2, max_value=20, value=6)
    with col2:
        male_count = st.number_input("👨 Male Participants", 0, num_participants, 2)
    with col3:
        female_count = st.number_input("👩 Female Participants", 0, num_participants - male_count, 2)

    nb_count = num_participants - male_count - female_count
    st.markdown(f"""
    <div style="text-align:right; font-size:16px; padding-top:5px;">
    🧑‍🎤 <span style="color:#7B1FA2"><strong>Non-Binary Participants:</strong> {nb_count}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🌍 Group Profile & Session Settings")
    col4, col5, col6 = st.columns([1, 1, 1])
    with col4:
        age_range = st.text_input("📅 Age Range", "25–35")
    with col5:
        location = st.text_input("📍 Location (City, Country)", "Mumbai, India")
    with col6:
        language = st.multiselect("🗣️ Language(s)", ["English", "Hindi", "Hinglish", "French"], default=["Hinglish"])

    mode = st.selectbox("🧭 Mode of Discussion", ["Online", "Offline"])
    duration_min = st.slider("⏱️ Duration (minutes)", 10, 120, 60)

    st.markdown("### 🧩 Topic & Demographics")
    topic = st.text_input("📌 Discussion Topic", "Electric Vehicles in Tier 2 Indian Cities")
    demo_profile = st.text_area("👤 Demographic Profile", "Mid-income professionals, mix of adopters and skeptics")

    st.markdown("### 📄 Study Objective")
    study_objective = st.text_area("✍️ Write Study Objective", "")
    uploaded_file = st.file_uploader("📎 Or Upload a File (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            study_objective += "\n\n" + "\n".join([page.extract_text() for page in reader.pages])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            study_objective += "\n\n" + docx2txt.process(uploaded_file)
        else:
            study_objective += "\n\n" + uploaded_file.read().decode("utf-8")

    submitted = st.form_submit_button("Generate Prompt")

# Prompt
if submitted:
    word_count = int(duration_min * 140)
    prompt = f"""You are an expert qualitative researcher and focus group moderator.

Simulate a highly realistic and detailed synthetic focus group discussion (FGD) transcript.

--- PARTICIPANT PROFILE ---
- Total Participants: {num_participants} ({male_count} male, {female_count} female, {nb_count} non-binary)
- Age Range: {age_range}
- Location: {location}
- Demographic: {demo_profile}
- Languages spoken: {', '.join(language)}
- Mode: {mode}
- Duration: {duration_min} minutes (~{word_count} words)
- Discussion Topic: {topic}
- Study Objective: {study_objective.strip()}

--- STRUCTURE TO FOLLOW ---
1. Opening (welcome, intros, ground rules, consent)
2. Warm-up (icebreaker, general thoughts)
3. Core Discussion (key Qs, probing, opposing views)
4. Closing (summary, final comments, thank you)

--- MODERATOR BEHAVIOR ---
- Remain neutral and professional
- Use natural transitions
- Encourage quieter participants
- Handle dominant voices politely
- Use real participant names typical of {location}
- Allow grammatical imperfections and local dialects

--- RESEARCH REQUIREMENT ---
Thoroughly research the discussion topic using multiple reputable sources specific to the location. Reflect realistic, localized views based on what people are actually discussing or facing in this region. Do not rely on generic or single-source assumptions.

Format the output as a readable transcript with MODERATOR and PARTICIPANT names."""

    st.markdown("### ✏️ Editable Prompt")
    final_prompt = st.text_area("You may revise the prompt before submission", prompt, height=400)
    st.session_state["final_prompt"] = final_prompt

    if st.button("🚀 Generate Transcript (Simulated Demo)"):
        demo_transcript = f"""
MODERATOR: Welcome everyone. Let's introduce ourselves briefly.

RAHUL (Male, 28): I'm Rahul from Dadar. I work as a software engineer. Curious about EVs.

SNEHA (Female, 30): Hi! I'm Sneha. I’ve started thinking about switching to an EV recently.

AADI (Non-Binary, 26): Hello! I live in Thane and ride a scooter. Wondering if an EV makes sense...

...

MODERATOR: Thank you all for your views today. Your inputs on "{topic}" were incredibly helpful.
        """.strip()

        st.markdown("### 📄 Synthetic Transcript")
        st.text_area("Transcript", demo_transcript, height=300)

        # TXT download
        st.download_button("⬇️ Download TXT", data=demo_transcript, file_name="transcript.txt", mime="text/plain")

        # DOCX download
        doc = Document()
        doc.add_heading("Focus Group Discussion Transcript", 0)
        for line in demo_transcript.split("\n"):
            para = doc.add_paragraph(line.strip())
            if "MODERATOR:" in line:
                para.runs[0].bold = True
            para.style.font.size = Pt(11)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button("⬇️ Download DOCX", data=buffer, file_name="transcript.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

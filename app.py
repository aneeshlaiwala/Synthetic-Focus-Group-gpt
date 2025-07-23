
import streamlit as st
import base64
import os
import json
import random
from docx import Document
from datetime import datetime
from PyPDF2 import PdfReader

st.set_page_config(page_title="Synthetic FGD Generator", layout="wide")

# --- Functions ---

def get_names_by_location(location, gender, count):
    sample_names = {
        "Mumbai": {
            "male": ["Aarav", "Vivaan", "Reyansh", "Kabir", "Arjun"],
            "female": ["Aanya", "Kiara", "Myra", "Saanvi", "Anaya"],
            "non-binary": ["Ravi", "Dev", "Sam", "Toni", "Alex"]
        },
        "Paris": {
            "male": ["Louis", "Hugo", "Lucas", "Nathan", "Leo"],
            "female": ["Emma", "Lea", "Manon", "Chloe", "Camille"],
            "non-binary": ["Alex", "Charlie", "Sasha", "Morgan", "Lou"]
        }
    }
    names = sample_names.get(location, sample_names["Mumbai"])
    return random.sample(names.get(gender, []), min(count, len(names.get(gender, []))))

def download_button(data, filename, label):
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'
    return href

def create_docx(text, filename):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(filename)

def read_uploaded_file(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".txt"):
        return str(file.read(), 'utf-8')
    else:
        return ""

# --- UI ---

st.title("🧠 Synthetic Focus Group Transcript Generator")
st.markdown("A professional tool for qualitative researchers to generate realistic, AI-powered discussion transcripts.")

with st.sidebar:
    st.header("🛠️ Configuration")
    ai_tool = st.selectbox("Select AI Tool", ["OpenAI", "Anthropic", "Gemini", "Mistral", "Hugging Face"])
    model = st.text_input("Model Name (e.g., gpt-4o, claude-3-opus)", "")
    api_key = st.text_input("Enter API Key", type="password")

    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Study Objective (.pdf/.docx/.txt)", type=["pdf", "docx", "txt"])

col1, col2, col3 = st.columns(3)
with col1:
    location = st.text_input("City/Location (for local names)", "Mumbai")
with col2:
    language = st.selectbox("Discussion Language", ["English", "Hindi", "French", "Spanish"])
with col3:
    total_participants = st.number_input("Total Participants", min_value=3, max_value=20, value=8)

gender_col1, gender_col2, gender_col3 = st.columns(3)
with gender_col1:
    male = st.number_input("Male Participants", min_value=0, max_value=int(total_participants), value=3, key="male")
with gender_col2:
    female = st.number_input("Female Participants", min_value=0, max_value=int(total_participants - male), value=3, key="female")
with gender_col3:
    non_binary = int(total_participants - male - female)
    st.markdown(f"**Non-Binary Participants:** {non_binary} (auto-calculated)")

duration = st.slider("Duration of Discussion (minutes)", 10, 120, 60, step=10)
moderator_name = st.text_input("Moderator Name", "Priya")

st.markdown("---")
st.subheader("📝 Edit the Moderator Prompt")
if uploaded_file:
    objective_text = read_uploaded_file(uploaded_file)
else:
    objective_text = ""

default_prompt = f"""You are an expert qualitative researcher and focus group moderator.

Study Objective:
{objective_text or '[Insert study objective here...]'}

Moderator Guidelines:
- Use a structured guide: Opening → Warm-up → Core → Closing
- Ensure diversity of opinions (based on gender & location)
- Respond in the selected language: {language}
- Reflect regional tone, slang, and references for {location}
- Each participant must sound unique (tone, grammar, personality)
- Names should be culturally relevant to {location}
- Introduce the moderator and participants with a warm-up round
- Include informal, realistic dialogue (interruptions, slang)
- Avoid repetition
- Time: {duration} mins worth of transcript (~750-900 words per 10 mins)
- Research the discussion topic deeply from multiple local sources
- Behaviors should reflect gender mix: {male} Male, {female} Female, {non_binary} Non-Binary
- Simulate full discussion with depth of opinion across phases
- Output format: MODERATOR: ..., PARTICIPANT_NAME: ...

Begin with moderator’s welcome line.
"""

prompt_text = st.text_area("🔧 Modify your prompt before generating", value=default_prompt, height=400)

if st.button("🚀 Generate Synthetic Transcript"):
    st.success("Transcript generation initiated (mockup for now – real API integration coming).")
    names = get_names_by_location(location, "male", male) +             get_names_by_location(location, "female", female) +             get_names_by_location(location, "non-binary", non_binary)
    random.shuffle(names)
    mock_transcript = f"MODERATOR {moderator_name}: Welcome everyone!\n"
    for name in names:
        mock_transcript += f"{name}: Hi, I’m {name}, excited to be part of this.\n"
    mock_transcript += "\n[Mock discussion content here – real model integration coming soon...]"

    st.markdown("---")
    st.subheader("📄 Generated Transcript")
    st.text_area("Transcript", mock_transcript, height=300)

    st.markdown(download_button(mock_transcript, "transcript.txt", "📥 Download .txt"), unsafe_allow_html=True)
    create_docx(mock_transcript, "/mnt/data/transcript.docx")
    with open("/mnt/data/transcript.docx", "rb") as f:
        st.download_button(label="📄 Download .docx", data=f, file_name="transcript.docx")

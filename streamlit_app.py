import streamlit as st
import os
import tempfile
from app import ResumeScreenerApp

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

# Custom CSS for "humanized" look as requested
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        color: #212529;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #357abd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .card {
        background: black;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    h1 { color: #2c3e50; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_app():
    return ResumeScreenerApp()

st.title("📄 Hybrid Resume Screener AI")
st.write("Upload resumes and a job description to find the best match using semantic AI.")

app = load_app()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Job Description")
    jd_text = st.text_area("Paste the Job Description here...", height=300)

with col2:
    st.subheader("2. Resumes")
    uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX)", accept_multiple_files=True)

if st.button("Start Screening") and jd_text and uploaded_files:
    results = []
    
    with st.spinner("Analyzing resumes..."):
        for uploaded_file in uploaded_files:
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            try:
                result = app.screen(tmp_path, jd_text)
                results.append(result)
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            finally:
                os.unlink(tmp_path)

    if results:
        st.subheader("Results")
        # Sort results by overall match
        results.sort(key=lambda x: x.overall_match, reverse=True)
        
        for res in results:
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3>{res.candidate_name} - <span style="color: #4a90e2;">{res.overall_match}% Match</span></h3>
                    <p><b>Hard Skills Match:</b> {res.hard_skills_match}% | <b>Semantic Match:</b> {res.semantic_match}% | <b>Soft Skills Match:</b> {res.soft_skills_match}%</p>
                    <p><b>Matched Skills:</b> {", ".join(res.matched_skills) if res.matched_skills else "None"}</p>
                    <p style="color: #e74c3c;"><b>Missing Skills:</b> {", ".join(res.missing_skills) if res.missing_skills else "None"}</p>
                    <p><i>"{res.explanation}"</i></p>
                </div>
                """, unsafe_allow_html=True)
else:
    if not jd_text or not uploaded_files:
        st.info("Please provide both a job description and at least one resume.")

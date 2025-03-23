import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Config
st.set_page_config(page_title="AI Resume Screening", page_icon="📄", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        .big-font { font-size:24px !important; font-weight: bold; color: #4A90E2; }
        .small-font { font-size:16px !important; color: #666; }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
st.sidebar.title("🔍 AI Resume Ranker")
st.sidebar.markdown("Compare resumes against job descriptions using AI.")

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip() if text else "No readable text found."

# Function to compare resumes with job description
def rank_resumes(job_description, resumes):
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()

    return cosine_similarities

# Main UI
st.markdown("<p class='big-font'>📄 AI Resume Screening & Ranking System</p>", unsafe_allow_html=True)
st.markdown("<p class='small-font'>Upload resumes and compare them with a job description to find the best match.</p>", unsafe_allow_html=True)

# Input Fields
job_description = st.text_area("✍️ Enter the Job Description", height=200)
uploaded_files = st.file_uploader("📂 Upload Resume(s) (PDF format)", type=["pdf"], accept_multiple_files=True)

# Process resumes
if uploaded_files and job_description:
    st.divider()
    with st.spinner("🔍 Analyzing resumes..."):
        resumes = [extract_text_from_pdf(file) for file in uploaded_files]
        scores = rank_resumes(job_description, resumes)

        ranked_resumes = sorted(zip(uploaded_files, scores), key=lambda x: x[1], reverse=True)

    # Display ranked results
    st.subheader("🏆 Ranked Resumes")
    for i, (file, score) in enumerate(ranked_resumes, start=1):
        st.write(f"### {i}. {file.name} - Score: {score:.2f}")
        st.progress(score)  # Progress bar for score visualization

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 Developed by Sahil Singh")

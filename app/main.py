import streamlit as st
from pdf_parser import extract_text_from_pdf


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# Main title
st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and paste a job description to analyze "
    "how well your profile matches the job."
)

st.divider()


# Create two columns
col1, col2 = st.columns(2)


# Resume upload section
with col1:
    st.subheader("📤 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"]
    )


# Job description section
with col2:
    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the Job Description here",
        height=300,
        placeholder="Paste the complete job description..."
    )


st.divider()


# Analyze button
if st.button("🔍 Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.warning("Please upload a resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            with st.spinner("Extracting text from resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text:
                st.error(
                    "No text could be extracted from this PDF. "
                    "Please upload a text-based PDF."
                )

            else:
                st.success("Resume text extracted successfully!")

                st.subheader("📄 Extracted Resume Text")

                with st.expander("View Extracted Resume Text"):
                    st.text(resume_text)

                st.info(
                    f"Successfully extracted {len(resume_text):,} "
                    "characters from the resume."
                )

        except Exception as error:
            st.error(f"Error reading PDF: {error}")
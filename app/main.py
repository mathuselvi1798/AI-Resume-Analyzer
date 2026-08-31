import streamlit as st
import re

from pdf_parser import extract_text_from_pdf


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# BPO SKILLS DATABASE
# --------------------------------------------------
BPO_SKILLS = [
    "communication",
    "customer service",
    "customer support",
    "voice process",
    "non voice",
    "chat support",
    "email support",
    "problem solving",
    "problem-solving",
    "computer",
    "ms office",
    "excel",
    "word",
    "crm",
    "english",
    "teamwork",
    "team work",
    "team player",
    "rotational shifts",
    "shift",
    "typing",
    "data entry",
    "sales",
    "customer handling"
]


# --------------------------------------------------
# FUNCTION: NORMALIZE TEXT
# --------------------------------------------------
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text


# --------------------------------------------------
# FUNCTION: FIND MATCHING SKILLS
# --------------------------------------------------
def find_matching_skills(resume_text, job_description):

    resume_text = normalize_text(resume_text)
    job_description = normalize_text(job_description)

    matching_skills = []
    missing_skills = []
    required_skills = []

    for skill in BPO_SKILLS:

        if skill in job_description:

            required_skills.append(skill)

            if skill in resume_text:
                matching_skills.append(skill)
            else:
                missing_skills.append(skill)

    return matching_skills, missing_skills, required_skills


# --------------------------------------------------
# FUNCTION: CALCULATE MATCH SCORE
# --------------------------------------------------
def calculate_match_score(matching_skills, required_skills):

    if len(required_skills) == 0:
        return 0

    score = (
        len(matching_skills)
        / len(required_skills)
    ) * 100

    return round(score)


# --------------------------------------------------
# APP HEADER
# --------------------------------------------------
st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and paste a job description to analyze "
    "how well your profile matches the job."
)

st.divider()


# --------------------------------------------------
# TWO COLUMNS
# --------------------------------------------------
left_column, right_column = st.columns(2)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------
with left_column:

    st.subheader("📤 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"]
    )


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------
with right_column:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the Job Description here",
        placeholder="Paste the complete BPO job description...",
        height=250
    )


st.divider()


# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------
if uploaded_file is not None and job_description.strip():

    if st.button(
        "🔍 Analyze Resume Match",
        use_container_width=True
    ):

        try:

            # ------------------------------------------
            # EXTRACT TEXT FROM RESUME
            # ------------------------------------------
            resume_text = extract_text_from_pdf(
                uploaded_file
            )

            if not resume_text or not resume_text.strip():

                st.error(
                    "Could not extract text from the resume PDF."
                )

            else:

                st.success(
                    "Resume analyzed successfully!"
                )


                # --------------------------------------
                # FIND MATCHING SKILLS
                # --------------------------------------
                (
                    matching_skills,
                    missing_skills,
                    required_skills
                ) = find_matching_skills(
                    resume_text,
                    job_description
                )


                # --------------------------------------
                # CALCULATE MATCH SCORE
                # --------------------------------------
                match_score = calculate_match_score(
                    matching_skills,
                    required_skills
                )


                # --------------------------------------
                # RESULTS HEADER
                # --------------------------------------
                st.divider()

                st.header(
                    "📊 Resume Match Results"
                )


                # --------------------------------------
                # METRICS
                # --------------------------------------
                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Match Score",
                        f"{match_score}%"
                    )


                with col2:

                    st.metric(
                        "Matching Skills",
                        len(matching_skills)
                    )


                with col3:

                    st.metric(
                        "Missing Skills",
                        len(missing_skills)
                    )


                # --------------------------------------
                # MATCHING AND MISSING SKILLS
                # --------------------------------------
                left_result, right_result = st.columns(2)


                # --------------------------------------
                # MATCHING SKILLS
                # --------------------------------------
                with left_result:

                    st.subheader(
                        "✅ Matching Skills"
                    )

                    if matching_skills:

                        for skill in matching_skills:

                            st.write(
                                f"✓ {skill.title()}"
                            )

                    else:

                        st.warning(
                            "No matching skills found."
                        )


                # --------------------------------------
                # MISSING SKILLS
                # --------------------------------------
                with right_result:

                    st.subheader(
                        "❌ Missing Skills"
                    )

                    if missing_skills:

                        for skill in missing_skills:

                            st.write(
                                f"✗ {skill.title()}"
                            )

                    else:

                        st.success(
                            "No important skills are missing!"
                        )


                # --------------------------------------
                # RESUME IMPROVEMENT SUGGESTIONS
                # --------------------------------------
                st.divider()

                st.subheader(
                    "💡 Resume Improvement Suggestions"
                )

                if missing_skills:

                    st.write(
                        "To improve the resume match score, "
                        "consider adding the following skills "
                        "or relevant experience if they genuinely "
                        "apply to the candidate:"
                    )

                    for skill in missing_skills:

                        st.write(
                            f"• {skill.title()}"
                        )

                    st.info(
                        "Tip: Add these skills to the Skills, "
                        "Experience, or Professional Summary "
                        "section of the resume only if the "
                        "candidate genuinely has these skills "
                        "or relevant experience."
                    )

                else:

                    st.success(
                        "Excellent! No important skills from "
                        "this job description are missing."
                    )


                # --------------------------------------
                # AI RECOMMENDATION
                # --------------------------------------
                st.divider()

                st.subheader(
                    "🤖 AI Recommendation"
                )


                if match_score >= 75:

                    st.success(
                        "Excellent Match! This candidate appears "
                        "to be a strong fit for this BPO position."
                    )


                elif match_score >= 50:

                    st.info(
                        "Good Match. The candidate has several "
                        "relevant skills but may need improvement "
                        "in some areas."
                    )


                elif match_score >= 25:

                    st.warning(
                        "Moderate Match. The candidate has limited "
                        "matching skills for this BPO position."
                    )


                else:

                    st.error(
                        "Low Match. The candidate currently does "
                        "not have many of the required BPO skills."
                    )


                # --------------------------------------
                # EXTRACTED RESUME TEXT
                # --------------------------------------
                st.divider()

                with st.expander(
                    "📄 View Extracted Resume Text"
                ):

                    st.text(
                        resume_text
                    )


        except Exception as error:

            st.error(
                f"Error analyzing resume: {error}"
            )


# --------------------------------------------------
# DEFAULT MESSAGE
# --------------------------------------------------
else:

    st.info(
        "Please upload a Resume PDF and enter a Job Description "
        "to start the analysis."
    )
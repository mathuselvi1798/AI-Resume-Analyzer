import streamlit as st
import re

from pdf_parser import extract_text_from_pdf


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# PROFESSIONAL CUSTOM CSS
# --------------------------------------------------
st.markdown(
    """
    <style>

    /* Main Application */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #111827);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Hide Streamlit Branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Hero Section */
    .hero-container {
        background: linear-gradient(
            135deg,
            #1e293b,
            #0f172a
        );
        border: 1px solid #334155;
        border-radius: 24px;
        padding: 45px;
        margin-bottom: 35px;
    }

    .hero-badge {
        display: inline-block;
        background: #1d4ed8;
        color: white;
        padding: 8px 18px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        color: white;
        margin-bottom: 15px;
    }

    .hero-description {
        font-size: 18px;
        color: #cbd5e1;
        max-width: 800px;
        line-height: 1.7;
    }

    /* Section Cards */
    .section-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 28px;
        min-height: 340px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    }

    .section-description {
        color: #94a3b8;
        margin-bottom: 20px;
        font-size: 15px;
    }

    /* Result Cards */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-bottom: 15px;
    }

    .metric-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }

    .metric-title {
        font-size: 15px;
        color: #94a3b8;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: white;
    }

    /* Result Panels */
    .result-panel {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 28px;
        min-height: 280px;
    }

    .result-title {
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin-bottom: 20px;
    }

    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        padding: 8px 14px;
        margin: 5px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
    }

    .matching-skill {
        background: rgba(34, 197, 94, 0.15);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }

    .missing-skill {
        background: rgba(239, 68, 68, 0.15);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    /* Recommendation Card */
    .recommendation-card {
        background: linear-gradient(
            135deg,
            #1e293b,
            #172033
        );
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
    }

    .recommendation-title {
        font-size: 25px;
        font-weight: 700;
        color: white;
        margin-bottom: 15px;
    }

    /* Progress */
    .progress-container {
        background: #334155;
        border-radius: 20px;
        height: 16px;
        overflow: hidden;
        margin-top: 15px;
    }

    .progress-bar {
        height: 100%;
        border-radius: 20px;
    }

    /* Streamlit Button */
    .stButton > button {
        background: linear-gradient(
            135deg,
            #2563eb,
            #4f46e5
        );
        color: white;
        font-size: 18px;
        font-weight: 700;
        border: none;
        border-radius: 14px;
        padding: 14px;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #1d4ed8,
            #4338ca
        );
        transform: translateY(-2px);
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #0f172a;
        border-radius: 15px;
        padding: 15px;
    }

    /* Text Area */
    textarea {
        border-radius: 12px !important;
    }

    /* Divider */
    hr {
        border-color: #334155 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
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
# FUNCTION: GET SCORE COLOR
# --------------------------------------------------
def get_score_color(score):

    if score >= 75:

        return "#22c55e"

    elif score >= 50:

        return "#3b82f6"

    elif score >= 25:

        return "#f59e0b"

    else:

        return "#ef4444"


# --------------------------------------------------
# FUNCTION: GET SCORE STATUS
# --------------------------------------------------
def get_score_status(score):

    if score >= 75:

        return "Excellent Match"

    elif score >= 50:

        return "Good Match"

    elif score >= 25:

        return "Moderate Match"

    else:

        return "Low Match"


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
st.markdown(
    """
    <div class="hero-container">

        <div class="hero-badge">
            🤖 AI POWERED CAREER ANALYSIS
        </div>

        <div class="hero-title">
            📄 AI Resume Analyzer
        </div>

        <div class="hero-description">
            Upload your resume and compare it with a job description.
            Discover matching skills, identify missing skills, and get
            professional recommendations to improve your resume.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# UPLOAD AND JOB DESCRIPTION SECTION
# --------------------------------------------------
left_column, right_column = st.columns(2, gap="large")


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------
with left_column:

    st.markdown(
        """
        <div class="section-card">

            <div class="section-title">
                📤 Upload Resume
            </div>

            <div class="section-description">
                Upload your resume in PDF format. The application will
                extract and analyze the text from your resume.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose your Resume PDF",
        type=["pdf"],
        label_visibility="visible"
    )


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------
with right_column:

    st.markdown(
        """
        <div class="section-card">

            <div class="section-title">
                💼 Job Description
            </div>

            <div class="section-description">
                Paste the complete job description below to compare the
                required skills with your resume.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Paste Job Description",
        placeholder=(
            "Paste the complete BPO job description here...\n\n"
            "Example:\n"
            "We are looking for candidates with excellent communication "
            "skills, customer service experience, computer knowledge, "
            "English proficiency, typing skills and willingness to work "
            "rotational shifts."
        ),
        height=220
    )


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

can_analyze = (
    uploaded_file is not None
    and job_description.strip()
)

analyze_button = st.button(
    "🔍 Analyze Resume Match",
    use_container_width=True,
    disabled=not can_analyze
)


# --------------------------------------------------
# DEFAULT MESSAGE
# --------------------------------------------------
if not can_analyze:

    st.info(
        "👆 Upload a Resume PDF and enter a Job Description "
        "to start the analysis."
    )


# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------
if analyze_button:

    try:

        with st.spinner("🤖 AI is analyzing the resume..."):

            # ------------------------------------------
            # EXTRACT TEXT FROM RESUME
            # ------------------------------------------
            resume_text = extract_text_from_pdf(
                uploaded_file
            )

        # ----------------------------------------------
        # VALIDATE RESUME TEXT
        # ----------------------------------------------
        if not resume_text or not resume_text.strip():

            st.error(
                "Could not extract text from the resume PDF. "
                "Please upload a valid text-based PDF."
            )

        else:

            # ------------------------------------------
            # FIND SKILLS
            # ------------------------------------------
            (
                matching_skills,
                missing_skills,
                required_skills
            ) = find_matching_skills(
                resume_text,
                job_description
            )


            # ------------------------------------------
            # CALCULATE SCORE
            # ------------------------------------------
            match_score = calculate_match_score(
                matching_skills,
                required_skills
            )

            score_color = get_score_color(
                match_score
            )

            score_status = get_score_status(
                match_score
            )


            # ------------------------------------------
            # RESULTS HEADER
            # ------------------------------------------
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.markdown(
                """
                <div class="hero-container">

                    <div class="hero-badge">
                        📊 ANALYSIS COMPLETE
                    </div>

                    <div class="hero-title" style="font-size: 38px;">
                        Resume Match Results
                    </div>

                    <div class="hero-description">
                        Here's how well your resume matches the skills
                        identified in the job description.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------
            # METRICS
            # ------------------------------------------
            metric1, metric2, metric3 = st.columns(
                3,
                gap="large"
            )


            with metric1:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            📊
                        </div>

                        <div class="metric-title">
                            Resume Match Score
                        </div>

                        <div class="metric-value"
                             style="color: {score_color};">
                            {match_score}%
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with metric2:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            ✅
                        </div>

                        <div class="metric-title">
                            Matching Skills
                        </div>

                        <div class="metric-value">
                            {len(matching_skills)}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with metric3:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            ⚠️
                        </div>

                        <div class="metric-title">
                            Missing Skills
                        </div>

                        <div class="metric-value">
                            {len(missing_skills)}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ------------------------------------------
            # SCORE PROGRESS BAR
            # ------------------------------------------
            st.markdown(
                f"""
                <div class="recommendation-card">

                    <div class="recommendation-title">
                        🎯 Overall Match: {score_status}
                    </div>

                    <div class="progress-container">

                        <div class="progress-bar"
                             style="
                             width: {match_score}%;
                             background: {score_color};
                             ">
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------
            # MATCHING AND MISSING SKILLS
            # ------------------------------------------
            st.markdown("<br>", unsafe_allow_html=True)

            left_result, right_result = st.columns(
                2,
                gap="large"
            )


            # ------------------------------------------
            # MATCHING SKILLS
            # ------------------------------------------
            with left_result:

                st.markdown(
                    """
                    <div class="result-panel">

                        <div class="result-title">
                            ✅ Matching Skills
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                if matching_skills:

                    for skill in matching_skills:

                        st.markdown(
                            f"""
                            <span class="
                            skill-tag matching-skill">
                                ✓ {skill.title()}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.warning(
                        "No matching skills were found."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # ------------------------------------------
            # MISSING SKILLS
            # ------------------------------------------
            with right_result:

                st.markdown(
                    """
                    <div class="result-panel">

                        <div class="result-title">
                            ⚠️ Skills to Improve
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                if missing_skills:

                    for skill in missing_skills:

                        st.markdown(
                            f"""
                            <span class="
                            skill-tag missing-skill">
                                ✗ {skill.title()}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.success(
                        "Excellent! No important skills are missing."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # ------------------------------------------
            # RESUME IMPROVEMENT SUGGESTIONS
            # ------------------------------------------
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.markdown(
                """
                <div class="recommendation-card">

                    <div class="recommendation-title">
                        💡 Resume Improvement Suggestions
                    </div>
                """,
                unsafe_allow_html=True
            )

            if missing_skills:

                st.write(
                    "Consider adding the following skills or relevant "
                    "experience to your resume only if they genuinely "
                    "apply to the candidate:"
                )

                for skill in missing_skills:

                    st.write(
                        f"• **{skill.title()}**"
                    )

                st.info(
                    "Tip: Add relevant skills to the Skills, "
                    "Professional Summary, Experience, or "
                    "Achievements section of your resume."
                )

            else:

                st.success(
                    "Excellent! Your resume contains all the important "
                    "skills identified from this job description."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # ------------------------------------------
            # AI RECOMMENDATION
            # ------------------------------------------
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                """
                <div class="recommendation-card">

                    <div class="recommendation-title">
                        🤖 AI Recommendation
                    </div>
                """,
                unsafe_allow_html=True
            )

            if match_score >= 75:

                st.success(
                    "Excellent Match! 🎉 This candidate appears to be "
                    "a strong fit for this BPO position. The resume "
                    "contains most of the important skills required "
                    "for the role."
                )

            elif match_score >= 50:

                st.info(
                    "Good Match! 👍 The candidate has several relevant "
                    "skills but could improve the resume by highlighting "
                    "the missing job-related skills and experience."
                )

            elif match_score >= 25:

                st.warning(
                    "Moderate Match. ⚠️ The candidate has some relevant "
                    "skills but may need additional experience or skills "
                    "to become a stronger fit for this position."
                )

            else:

                st.error(
                    "Low Match. ❌ The resume currently does not show "
                    "many of the important skills identified in this "
                    "job description."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # ------------------------------------------
            # EXTRACTED RESUME TEXT
            # ------------------------------------------
            st.markdown("<br>", unsafe_allow_html=True)

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

                st.text(
                    resume_text
                )


            # ------------------------------------------
            # ANALYSIS SUMMARY
            # ------------------------------------------
            st.markdown("<br>", unsafe_allow_html=True)

            st.caption(
                "AI Resume Analyzer • Resume-to-Job Description "
                "Skill Matching System"
            )


    except Exception as error:

        st.error(
            f"Error analyzing resume: {error}"
        )
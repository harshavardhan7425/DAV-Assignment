# app.py

import streamlit as st
import json
from advisor import main

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="AI Student Performance Advisor",
    page_icon="🎓",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: white;
}

.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
}

.result-box {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #333;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.title("🎓 AI Student Performance Advisor")

st.markdown("""
Predict student academic performance and receive personalized AI-generated recommendations.
""")

st.divider()

# =========================================
# INPUT SECTIONS
# =========================================

col1, col2 = st.columns(2)

# -----------------------------------------
# LEFT COLUMN
# -----------------------------------------
with col1:

    st.subheader("📚 Academic & Lifestyle")

    age = st.slider(
        "Age",
        min_value=17,
        max_value=30,
        value=20
    )

    study_hours = st.slider(
        "Study Hours Per Day",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5
    )

    social_media = st.slider(
        "Social Media Hours",
        min_value=0.0,
        max_value=12.0,
        value=3.0,
        step=0.5
    )

    passive_entertainment = st.slider(
        "Passive Entertainment Hours",
        min_value=0.0,
        max_value=12.0,
        value=2.0,
        step=0.5
    )

    attendance = st.slider(
        "Attendance Percentage",
        min_value=0,
        max_value=100,
        value=80
    )

    sleep_hours = st.slider(
        "Sleep Hours Per Night",
        min_value=3.0,
        max_value=12.0,
        value=7.0,
        step=0.5
    )

# -----------------------------------------
# RIGHT COLUMN
# -----------------------------------------
with col2:

    st.subheader("🧠 Personal & Environment")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    diet_quality = st.selectbox(
        "Diet Quality",
        ["Poor", "Average", "Good"]
    )

    exercise_frequency = st.selectbox(
        "Exercise Frequency",
        [
            "0 times/week",
            "1 time/week",
            "2 times/week",
            "3 times/week",
            "4 times/week",
            "5 times/week",
            "Daily"
        ]
    )

    parental_education = st.selectbox(
        "Parental Education Level",
        [
            "High School",
            "Undergraduate",
            "Postgraduate",
            "PhD"
        ]
    )

    internet_quality = st.selectbox(
        "Internet Quality",
        ["Poor", "Average", "Good"]
    )

    mental_health = st.slider(
        "Mental Health Rating",
        min_value=1,
        max_value=10,
        value=7
    )

    extracurricular = st.selectbox(
        "Extracurricular Participation",
        ["Yes", "No"]
    )

    por = st.selectbox(
        "Position of Responsibility (PoR)",
        ["Yes", "No"]
    )

# =========================================
# PREDICT BUTTON
# =========================================

st.divider()

predict_button = st.button(
    "🚀 Predict Performance",
    use_container_width=True
)

# =========================================
# PREDICTION
# =========================================

if predict_button:

    try:

        # ---------------------------------
        # INPUT JSON
        # ---------------------------------
        input_json = json.dumps({

            "Age": age,
            "Gender": gender,
            "StudyHoursPerDay": study_hours,
            "SocialMediaHours": social_media,
            "PassiveEntertainmentHrs": passive_entertainment,
            "PoR": por,
            "AttendancePercentage": attendance,
            "SleepHoursPerNight": sleep_hours,
            "Diet_Quality": diet_quality,
            "Exercise_frequency": exercise_frequency,
            "parental_education_level": parental_education,
            "internet_quality": internet_quality,
            "mental_health_rating": mental_health,
            "extracurricular_participation": extracurricular

        })

        # ---------------------------------
        # MODEL CALL
        # ---------------------------------
        with st.spinner("Generating prediction and recommendations..."):

            result = main(input_json)

        predicted_grade = result["predicted_grade"]
        recommendation = result["recommendation"]

        # =================================
        # RESULTS
        # =================================

        st.divider()

        st.header("📈 Prediction Results")

        metric_col1, metric_col2 = st.columns(2)

        # ---------------------------------
        # PERFORMANCE SCORE
        # ---------------------------------
        with metric_col1:

            st.metric(
                "Predicted Cumulative Grade",
                f"{predicted_grade:.2f}/100"
            )

        # ---------------------------------
        # STATUS
        # ---------------------------------
        with metric_col2:

            if predicted_grade >= 75:
                st.success("Excellent Academic Performance")

            elif predicted_grade >= 50:
                st.warning("Average Academic Performance")

            else:
                st.error("Academic Performance Needs Improvement")

        # ---------------------------------
        # PROGRESS BAR
        # ---------------------------------
        st.subheader("📊 Performance Score")

        st.progress(min(predicted_grade / 100, 1.0))

        # ---------------------------------
        # TOP FEATURES
        # ---------------------------------
        st.subheader("🔍 Most Influential Features")

        top_features = result["top_features"]

        for item in top_features:

            st.markdown(
                f"""
                <div class="result-box">
                <b>{item['feature']}</b><br>
                Current Value: {item['value']}
                </div>
                """,
                unsafe_allow_html=True
            )

        # ---------------------------------
        # AI RECOMMENDATION
        # ---------------------------------
        st.subheader("🤖 AI Recommendation")

        st.markdown(
            f"""
            <div class="result-box">
            {recommendation}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error(f"Error: {str(e)}")
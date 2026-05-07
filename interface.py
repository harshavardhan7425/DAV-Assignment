import streamlit as st
import json
from advisor import main

st.set_page_config(
    page_title="Student Performance Predictor and Advisor",
    page_icon="👨🏻‍🏫",
    layout="wide"
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #0F172A,
        #111827,
        #1E293B
    );
    color: white;
}

/* Section cards */
[data-testid="stVerticalBlock"] > div:has(.card) {
    background-color: #161B22;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #30363D;
}

/* Metric card */
[data-testid="metric-container"] {
    background-color: #161B22;
    border: 1px solid #30363D;
    padding: 15px;
    border-radius: 16px;
}

/* Buttons */
.stButton>button {
    background-color: #2563EB;
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 18px;
    font-weight: 600;
    border: none;
}

/* Button hover */
.stButton>button:hover {
    background-color: #1D4ED8;
    color: white;
}

/* Sliders */
.stSlider {
    padding-top: 10px;
    padding-bottom: 10px;
}

/* Recommendation card */
.result-box {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);

    padding: 20px;
    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.1);
}
            
/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Hide toolbar */
[data-testid="stToolbar"] {
    display: none;
}

/* Remove top spacing */
.block-container {
    padding-top: 1rem;
}
            



</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='text-align: center;'>
    👨🏻‍🏫 AI Student Performance Advisor
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <p style='text-align: center; font-size:18px;'>
    Predict your academic performance and receive personalized AI-generated recommendations.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📖 Academic & Lifestyle")

    age = st.slider(
        "Age",
        min_value=15,
        max_value=30,
        value=20,
        step = 1
    )

    study_hours = st.slider(
        "Study Hours Per Day",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.1
    )

    social_media = st.slider(
        "Social Media Hours",
        min_value=0.0,
        max_value=12.0,
        value=3.0,
        step=0.1
    )

    passive_entertainment = st.slider(
        "Passive Entertainment Hours",
        min_value=0.0,
        max_value=12.0,
        value=2.0,
        step=0.1
    )

    attendance = st.slider(
        "Attendance Percentage",
        min_value=0,
        max_value=100,
        value=80,
        step = 1
    )

    sleep_hours = st.slider(
        "Sleep Hours Per Night",
        min_value=3.0,
        max_value=12.0,
        value=7.0,
        step=0.5
    )

with col2:
    st.subheader("⛹🏻 Personal & Environment")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    diet_quality = st.selectbox(
        "Diet Quality",
        ["Poor", "Average", "Good"]
    )

    exercise_frequency = st.slider(
        "Exercise Frequency (Per Week)",
        min_value=0,
        max_value=7,
        value=0,
        step=1
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
        value=7,
        step = 1
    )

    extracurricular = st.selectbox(
        "Extracurricular Participation",
        ["Yes", "No"]
    )

    por = st.selectbox(
        "Position of Responsibility (PoR)",
        ["Yes", "No"]
    )

st.divider()

predict_button = st.button(
    "💡 Predict Performance",
    use_container_width=True
)

if predict_button:
    try:
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

        with st.spinner("Generating prediction and recommendations..."):

            result = main(input_json)

        predicted_grade = result["predicted_grade"]
        recommendation = result["recommendation"]

        st.divider()

        st.header("Prediction Results")

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                "Predicted Cumulative Grade",
                f"{predicted_grade:.2f}/100"
            )

        with metric_col2:

            if predicted_grade >= 75:
                st.success("Excellent Academic Performance")

            elif predicted_grade >= 50:
                st.warning("Average Academic Performance")

            else:
                st.error("Academic Performance Needs Improvement")

        st.subheader("📊 Performance Score")

        st.progress(min(predicted_grade / 100, 1.0))

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
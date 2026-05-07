import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import json
from groq import Groq
import os
import streamlit as st

# Retrieving model
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")

client = Groq(
    st.secrets["GROQ_API_KEY"]
)

# Input preprocessing
def prepro_input(data: dict):
    df = pd.DataFrame([data])
    df = pd.get_dummies(df, drop_first=True)
    df = df.reindex(columns=columns, fill_value=0)
    return df

def get_top_features(input_df, importances, feature_names, top_n=3):
    values = input_df.iloc[0]
    feature_impact = []

    for i, feature in enumerate(feature_names):
        val = values[feature]
        imp = importances[i]
        impact_score = abs(val * imp)
        feature_impact.append((feature, val, impact_score))

    feature_impact.sort(key=lambda x: x[2], reverse=True)
    return feature_impact[:top_n]

def get_prompt(cgpa, top_features):

    feature_text = ""
    for feat, val, _ in top_features:
        feature_text += f"- {feat}: {val}\n"
    
    prompt = f"""
    You are an academic advisor. Address the student directly as "you".

    Predicted CGPA: {cgpa:.2f}

    Student profile (current values):
    {feature_text}

    Task:
    1) Perform a brief sensitivity check: slightly vary each listed feature (increase/decrease within realistic bounds) and determine which single change most improves CGPA.
    2) Identify the MOST impactful feature for improvement.
    3) Also identify TWO other helpful features.

    Output rules (strict):
    - Write a short description (3–4 sentences total).
    - First sentence: clearly state which feature change most improves the CGPA and why.
    - Next sentences: give actionable advice for TWO other features.
    - Use direct, practical language (talk to the student as "you").
    - Do NOT mention “model”, “feature importance”, or “sensitivity analysis”.
    - Do NOT use bullet points or JSON.

    Style:
    - Concrete, actionable (e.g., “increase study hours from 3→5”).
    - Keep it concise and specific.

    Write the description now.
    """
    return prompt


input_json = json.dumps({
    "Age": 20,
    "StudyHoursPerDay": 5,
    "SocialMediaHours": 4,
    "SleepHours": 7,
    "Exercise_frequency": "2 times/week"
})


def main(input):
    data = json.loads(input)
    tuned_data = prepro_input(data)
    cgpa = model.predict(tuned_data)[0]
    importances = model.feature_importances_
    top_features = get_top_features(tuned_data, importances, columns)

    prompt = get_prompt(cgpa, top_features)

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
    )
    recommendation = response.choices[0].message.content.strip()
    
    Output_dict = {
        "predicted_grade": float(cgpa),
        "top_features": [
            {"feature": f, "value": float(v)} for f, v, _ in top_features
        ],
        "recommendation": recommendation if recommendation else "No response generated"
    }

    return Output_dict

if __name__ == "__main__":
    print(main(input_json))


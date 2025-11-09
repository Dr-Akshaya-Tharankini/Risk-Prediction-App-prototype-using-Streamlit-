import streamlit as st
import pandas as pd

st.set_page_config(page_title="LifeRisk.AI - Advanced Health Risk Assessment", layout="wide")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 1

# App Title
st.title("📋 Preventra – Advanced Health Risk Assessment")
st.markdown("Comprehensive lifestyle and health analysis with disease-specific morbidity risk calculations.")

# ----------------------------
# Step 1: Basic Information
# ----------------------------
if st.session_state.page == 1:
    st.header("Step 1: Basic Information")

    col1, col2 = st.columns(2)
    with col1:
        age_input = st.text_input("Age", placeholder="e.g., 35")
        try:
            age = int(age_input) if age_input else 0
        except ValueError:
            age = 0

        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])

        height_input = st.text_input("Height (cm)", placeholder="e.g., 170")
        try:
            height = int(height_input) if height_input else 0
        except ValueError:
            height = 0

        weight_input = st.text_input("Weight (kg)", placeholder="e.g., 65")
        try:
            weight = int(weight_input) if weight_input else 0
        except ValueError:
            weight = 0

    with col2:
        city = st.text_input("City", placeholder="e.g., Dubai, Abu Dhabi")
        occupation = st.selectbox("Occupation Type", ["Select",
                                                      "Sedentary/Desk Job (IT, Finance, Clerical)",
                                                      "Moderate Activity (Teacher, Driver, Shop Keeper)",
                                                      "Physically demanding (Laborer, Farmer, Construction)",
                                                      "High Stress (Business, Doctor, Police, Pilot, Night Shift)",
                                                      "Unemployed / Student / Home maker / Retired"])
        income = st.selectbox("Income Level", ["Select", "0 income", "Low income", "Middle income", "High income"])
        education = st.selectbox("Education Level", ["Select", "No Formal Education", "High School or Less",
                                                     "Graduate (Bachelor's)", "Post Graduate or Higher"])

    if st.button("Next ➡️", key="next1"):
        if gender == "Select" or occupation == "Select" or income == "Select" or city == "" or height == 0 or weight == 0 or age == 0:
            st.warning("🚨 Please complete all required fields before continuing.")
        else:
            bmi = round(weight / ((height / 100) ** 2), 1)
            bmi_status = "Normal" if 18.5 <= bmi <= 24.9 else ("Overweight" if bmi > 24.9 else "Underweight")

            st.session_state.age = age
            st.session_state.gender = gender
            st.session_state.height = height
            st.session_state.weight = weight
            st.session_state.city = city
            st.session_state.occupation = occupation
            st.session_state.income = income
            st.session_state.education = education
            st.session_state.bmi = bmi
            st.session_state.bmi_status = bmi_status

            st.session_state.page = 2

# ----------------------------
# Step 2: Health History
# ----------------------------
if st.session_state.page == 2:
    st.header("Step 2: Health History")

    smoking = st.radio("Smoking/Vaping Status", ["Never", "Former (quit)", "Current smoker"])
    alcohol = st.selectbox("Alcohol Consumption", ["Never", "Former (quit)", "Occasional drinker", "Regular drinker"])

    st.subheader("Current Health Conditions")
    health_conditions = st.multiselect("Select any conditions you have:", [
        "Diabetes", "Hypertension", "Heart Disease", "Kidney Disease", "Liver Disease",
        "Asthma / COPD", "Hormonal Imbalances", "Autoimmune disease", "Congenital Conditions", "None"])

    medications = st.text_area("Current Medications", placeholder="List your regular medications...")

    st.subheader("Family History")
    family_history = st.multiselect("Family history of:", [
        "Diabetes", "Hypertension", "Heart Disease", "Cancer", "Stroke", "None"])

    st.subheader("Lifestyle Factors")
    exercise_freq = st.selectbox("Exercise Frequency", ["Never", "Rarely", "Occasionally", "Regularly"])
    exercise_intensity = st.selectbox("Exercise Intensity", ["Light", "Moderate", "Intense"])
    sleep_hours = st.slider("Average Sleep Hours", 3, 12, 7)
    sleep_quality = st.selectbox("Sleep Quality", ["Poor", "Fair", "Good"])
    stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)

    st.subheader("Diet & Nutrition")
    diet_type = st.selectbox("Diet Type", ["Non Vegetarian", "Vegetarian", "Vegan"])
    processed_food = st.selectbox("Processed/Junk Food Consumption", ["Never", "Rarely", "Often", "Daily"])

    if st.button("Next ➡️", key="next2"):
        st.session_state.smoking = smoking
        st.session_state.alcohol = alcohol
        st.session_state.health_conditions = health_conditions
        st.session_state.medications = medications
        st.session_state.family_history = family_history
        st.session_state.exercise_freq = exercise_freq
        st.session_state.exercise_intensity = exercise_intensity
        st.session_state.sleep_hours = sleep_hours
        st.session_state.sleep_quality = sleep_quality
        st.session_state.stress_level = stress_level
        st.session_state.diet_type = diet_type
        st.session_state.processed_food = processed_food

        st.session_state.page = 3

# ----------------------------
# Step 3: Risk Score Calculation (hidden)
# ----------------------------
if st.session_state.page == 3:
    risk_score = 0
    age = st.session_state.age
    bmi = st.session_state.bmi
    smoking = st.session_state.smoking
    alcohol = st.session_state.alcohol
    exercise_freq = st.session_state.exercise_freq
    sleep_hours = st.session_state.sleep_hours
    sleep_quality = st.session_state.sleep_quality
    stress_level = st.session_state.stress_level
    health_conditions = st.session_state.health_conditions

    if age > 50: risk_score += 2
    elif age > 35: risk_score += 1
    if bmi >= 30: risk_score += 2
    elif bmi >= 25: risk_score += 1
    if smoking == "Current smoker": risk_score += 2
    elif smoking == "Former (quit)": risk_score += 1
    if alcohol == "Regular drinker": risk_score += 1
    if exercise_freq == "Never": risk_score += 1
    if sleep_hours < 6: risk_score += 1
    if sleep_quality == "Poor": risk_score += 1
    if stress_level >= 7: risk_score += 1
    if any(cond in health_conditions for cond in ["Diabetes", "Hypertension", "Heart Disease"]):
        risk_score += 2

    st.session_state.risk_score = risk_score

    st.session_state.page = 4

# ----------------------------
# Step 4: Digital Questions + Final Assessment only shows health risk
# ----------------------------
if st.session_state.page == 4:
    st.header("Step 3: Digital Health Readiness")

    wearable_use = st.selectbox(
        "Do you currently use a smartwatch / fitness band / health wearable?",
        ["Select", "Yes — regularly (daily or almost daily)", "Yes — but occasionally",
         "Not yet — but planning to start", "No — and not interested"]
    )

    health_metrics_check = st.selectbox(
        "How often do you check any health metrics (steps, heart rate, sleep, BP, SpO₂, etc.)?",
        ["Select", "Daily / almost daily", "Few times per week", "Rarely", "Never"]
    )

    motivation_orientation = st.selectbox(
        "How would you describe your attitude toward tracking your health digitally?",
        ["Select", "I like monitoring and optimizing my health with tech",
         "Neutral — I don’t mind tracking but not consistent",
         "I’m curious but not sure how useful it is for me",
         "I don’t think digital tracking is useful"]
    )

    if st.button("See Final Assessment ➡️", key="final_assessment"):
        if "Select" in [wearable_use, health_metrics_check, motivation_orientation]:
            st.warning("🚨 Please answer all digital health questions before continuing.")
        else:
            # ONLY SHOW HEALTH RISK - DO NOT include digital score result
            risk_score = st.session_state.risk_score

            if risk_score >= 7:
                risk_category = "HIGH"
            elif risk_score >= 4:
                risk_category = "MODERATE"
            else:
                risk_category = "LOW"

            st.subheader("📊 Final Health Risk Assessment")

            st.markdown(f"## 🔢 Your Risk Score: **{risk_score}**")

            if risk_category == "HIGH":
                st.error("You fall into the **HIGH risk** category. You are at high risk - immediate attention to your health is recommended. You should begin lifestyle changes and regular monitoring.")
            elif risk_category == "MODERATE":
                st.warning("You fall into the **MODERATE risk** category. You should pay attention and take care of your health. Improve lifestyle habits and keep monitoring your health.")
            else:
                st.success("You fall into the **LOW risk** category. You are healthy - keep up the good habits! Maintain your current lifestyle!")

            st.markdown(
                """
            **Risk Scoring Scale**
            | Score Range | Category   |
            |-------------|------------|
            | 0 – 3       | Low        |
            | 4 – 6       | Moderate   |
            | 7 – 10      | High       |
            """
            )

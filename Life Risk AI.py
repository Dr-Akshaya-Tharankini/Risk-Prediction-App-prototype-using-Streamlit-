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

            # Save in session_state
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
        # Save Step 2 inputs
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
    # Calculate Health Risk Score and save to session_state
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

    # Save in session_state
    st.session_state.risk_score = risk_score
    if risk_score >= 7:
        st.session_state.risk_category = "HIGH"
    elif risk_score >= 4:
        st.session_state.risk_category = "MODERATE"
    else:
        st.session_state.risk_category = "LOW"

    # Next button to Step 4
    st.session_state.page = 4

# ----------------------------
# Step 4: Digital Health Readiness + Final Assessment
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
            # Map scores
            wearable_score_map = {
                "Yes — regularly (daily or almost daily)": 3,
                "Yes — but occasionally": 1,
                "Not yet — but planning to start": 0,
                "No — and not interested": -1
            }
            metrics_score_map = {
                "Daily / almost daily": 3,
                "Few times per week": 1,
                "Rarely": 0,
                "Never": -1
            }
            motivation_score_map = {
                "I like monitoring and optimizing my health with tech": 2,
                "Neutral — I don’t mind tracking but not consistent": 1,
                "I’m curious but not sure how useful it is for me": 0,
                "I don’t think digital tracking is useful": -1
            }

            digital_score = (
                wearable_score_map[wearable_use] +
                metrics_score_map[health_metrics_check] +
                motivation_score_map[motivation_orientation]
            )

            # Categorize readiness
            if digital_score <= 3:
                readiness_category = "LOW"
            elif digital_score <= 6:
                readiness_category = "MED"
            else:
                readiness_category = "HIGH"

            # Retrieve saved health risk
            risk_score = st.session_state.risk_score
            risk_category = st.session_state.risk_category

            # Display final assessment
            st.subheader("📊 Final Health & Digital Readiness Assessment")
            st.markdown(f"**Health Risk Score:** {risk_score} → {risk_category}")
            st.markdown(f"**Digital Health Readiness Score:** {digital_score} → {readiness_category}")

            # Final messages
            final_message = ""
            if risk_category == "HIGH" and readiness_category == "HIGH":
                final_message = "Your health risk is high, and your digital readiness is high. This means you are open to using technology and tracking to improve your lifestyle. Stay consistent with tracking health metrics and continue making positive choices."
            elif risk_category == "HIGH" and readiness_category == "MED":
                final_message = "Your health risk is high, and your digital readiness is moderate. Try to improve basic daily routines consistently. You may try digital tracking later if you become more comfortable with it."
            elif risk_category == "HIGH" and readiness_category == "LOW":
                final_message = "Your health risk is high, but your digital readiness is low. Try to focus on a few simple lifestyle changes first. You can slowly explore digital tracking tools in the future if comfortable."
            elif risk_category == "MODERATE" and readiness_category == "HIGH":
                final_message = "Your health risk is moderate, and your digital readiness is high. You are well suited for using technology to understand your habits better. Tracking may help prevent your risk from increasing over time."
            elif risk_category == "MODERATE" and readiness_category == "MED":
                final_message = "Your health risk is moderate, and your digital readiness is moderate. Focus on strengthening day-to-day lifestyle habits. Digital tracking can be introduced gradually if you find it useful."
            elif risk_category == "MODERATE" and readiness_category == "LOW":
                final_message = "Your health risk is moderate, and your digital readiness is low. Focus on building healthier daily habits such as better sleep, regular activity, and balanced diet. Digital tracking can always be added later if needed."
            elif risk_category == "LOW" and readiness_category == "HIGH":
                final_message = "Your health risk is low, and your digital readiness is high. This is a great profile for preventive lifestyle monitoring. Keep using your interest in tracking to maintain your current healthy baseline."
            elif risk_category == "LOW" and readiness_category == "MED":
                final_message = "Your health risk is low, and your digital readiness is moderate. You can continue your current habits comfortably. You may explore simple digital tracking later if you feel the need."
            elif risk_category == "LOW" and readiness_category == "LOW":
                final_message = "Your health risk is low, and your digital readiness is low. You are doing fine with your current habits. Tracking your health is optional — but small efforts can still support long-term wellness."

            st.info(final_message)





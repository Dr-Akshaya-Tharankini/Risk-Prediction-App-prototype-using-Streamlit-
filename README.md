# Preventra – Advanced Health Risk Assessment (Streamlit App)

Preventra is an interactive health risk scoring application.  
It collects an individual's lifestyle, medical, and demographic profiles → then calculates a **Health Risk Score** (Biomedical Risk Estimate).

The application is designed for preventive health coaching workflows & early risk stratification for wellness programs.

---

## Features

| Module | Description |
|-------|-------------|
| Step 1 | Basic Demographics (Age, Height, Weight, City, Occupation, Income etc.) |
| Step 2 | Health History, Lifestyle & Sleep Factors |
| Step 3 | Backend Risk Score Calculation (hidden from user) |
| Step 4 | Digital Readiness Questions (stored but not included in risk scoring) |
| Final Result | Displays only the **Health Risk Score** & Risk Category |

---

## Risk Score Logic

The model assigns weighted points based on:

- Age
- BMI
- Smoking
- Alcohol
- Sleep
- Exercise
- Stress
- Comorbidities (Diabetes, Hypertension, Heart Disease)

### Risk Category Mapping

| Score Range | Category  |
|-------------|-----------|
| **0 – 3**   | LOW       |
| **4 – 6**   | MODERATE  |
| **7 – 10**  | HIGH      |

The final result shows only:
- The Health Risk Score
- The Risk Category
- Descriptive interpretation

Digital wellness score questions exist but are not shown or used in the final scoring display.

--- 

## Author

**Dr. Akshaya Tharankini A**  
Healthcare Data & AI Specialist | SQL | Python | Power BI  
*Email: drakshayatharankini@gmail.com*  
*LinkedIn: https://www.linkedin.com/in/dr-akshaya-tharankini/*

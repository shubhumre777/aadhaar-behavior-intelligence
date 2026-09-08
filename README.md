# 🧠 Aadhaar Biometric Behaviour Intelligence System

Live Demo:  
👉 https://aadhaar-behavior-intelligence-z6cfp99ncoissjukvbr4mh.streamlit.app/

---

🇮🇳 Aadhaar Behaviour Intelligence Platform
AI-Powered National Identity Analytics System
<p align="center"> <img src="https://img.shields.io/badge/AI-Powered-blueviolet"/> <img src="https://img.shields.io/badge/India-UIDAI-orange"/> <img src="https://img.shields.io/badge/Status-Deployed-success"/> <img src="https://img.shields.io/badge/Tech-Streamlit%20%7C%20ML%20%7C%20Forecasting-blue"/> </p> <p align="center"> 🧠 Turning Aadhaar data into National Intelligence <br/> 📊 Detecting anomalies • Forecasting risk • Supporting governance </p>

## --Vision

To transform raw Aadhaar update logs into actionable national intelligence that enables proactive governance, infrastructure planning, and improved citizen experience.

India’s digital identity system is the largest in the world. Monitoring it using simple reports is not enough.

This project builds an AI-powered decision support platform for UIDAI.

## --Problem Statement

Unlock societal trends in Aadhaar enrolment and updates by identifying meaningful patterns, anomalies, and predictive indicators to support informed decision-making and system improvements.


---

## --Project Objective

To design a data-driven intelligence system that:

- Detects abnormal biometric update behaviour using Machine Learning  
- Identifies high-risk districts and regions  
- Discovers temporal trends and behavioural shifts  
- Translates raw data into actionable geographic and policy insights  

---

## -- Datasets Used

Two official UIDAI datasets:

1. Aadhaar Demographic Update Dataset  
2. Aadhaar Biometric Update Dataset  

Each dataset was provided in multiple CSV chunks and merged during preprocessing.

## --Key Columns Used:

- `date`
- `state`
- `district`
- `pincode`
- `demo_age_5_17`
- `demo_age_17_`
- `bio_age_5_17`
- `bio_age_17_`

---

##  --Data Pipeline

1. Merge multiple CSV files  
2. Clean invalid dates & missing values  
3. Monthly aggregation at district level  
4. Feature engineering  
5. Machine learning anomaly detection  
6. Risk scoring & classification  
7. Visualization via Streamlit dashboard  

---

## --Feature Engineering (Predictive Indicators)

| Feature | Description |
|--------|-------------|
| `demo_total` | Total demographic updates |
| `bio_total` | Total biometric updates |
| `bio_demo_ratio` | Behavioural indicator (biometric / demographic) |
| `risk_score` | ML-weighted anomaly severity |
| `risk_level` | LOW / MEDIUM / HIGH |

These features enable early detection of abnormal behavioural patterns.

---

## --Machine Learning Model

**Isolation Forest** (unsupervised anomaly detection)

Why Isolation Forest?

- Works well on large-scale numeric data  
- Detects rare abnormal behaviour  
- No labeled data required  
- Scalable for national datasets  

Output:

- `anomaly_flag` → normal or abnormal  
- Risk score per district-month  

---

## --Key Insights

- Major nationwide biometric anomaly spike detected in **January 2025**
- ~800 districts showed abnormal behaviour in the same month
- Certain districts repeatedly exhibit extremely high biometric-to-demographic ratios
- Multiple states show persistent high-risk behaviour patterns

---

## --Geographic Intelligence

The system visualizes biometric risk using a point-based geo map:

- Each point represents a state  
- Size & color represent biometric risk intensity  
- Enables quick identification of national stress hotspots  

---

## --Decision Support Framework

| Risk Level | Interpretation | Recommended Action |
|-----------|----------------|--------------------|
| LOW | Normal behaviour | Routine monitoring |
| MEDIUM | Moderate anomaly | Infrastructure review |
| HIGH | Severe anomaly | Immediate investigation & resource allocation |

---

## --Dashboard Features

- Monthly trend visualization  
- Anomaly detection chart  
- Interactive filters (month & state)  
- Abnormal district ranking table  
- Risk ranking table  
- Geographic hotspot map  
- Summary metrics  

---

## --Tech Stack

- Python  
- Pandas, NumPy  
- Scikit-learn  
- Matplotlib  
- Plotly  
- Streamlit  
- GitHub  
- Streamlit Community Cloud  

---

## --Deployment

The project is deployed using **Streamlit Cloud**.

Live App:  
👉 https://aadhaar-behavior-intelligence-z6cfp99ncoissjukvbr4mh.streamlit.app/

---

📁 Project Structure

<img src="images/https://github.com/shubhumre777/aadhaar-behavior-intelligence/blob/main/project%20structure.png" alt="Project Structure" width="400">


## --Conclusion

This project demonstrates how large-scale Aadhaar update data can be transformed into:

- Behavioural intelligence  
- Early warning systems  
- Geographic risk monitoring  
- Policy-support tools  

It bridges **raw public infrastructure data** with **AI-driven decision support systems**.

---

## --License

This project is developed for educational and hackathon purposes.









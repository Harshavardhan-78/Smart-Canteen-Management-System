import streamlit as st
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from utils.db_handler import fetch_sales_data

st.title("🔮 Weekly Demand Predictor")

if "owner_id" not in st.session_state:
    st.error("Please login")
    st.stop()

# Load model
@st.cache_resource
def load_model():
    BASE_DIR = Path(__file__).resolve().parent.parent
    MODEL_PATH = BASE_DIR / "models" / "rf_classifier.pkl"
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model = load_model()

# Fetch owner data
df = fetch_sales_data(st.session_state["owner_id"])

if df.empty:
    st.warning("No sales data available")
    st.stop()

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Require minimum 7 days
if df["date"].nunique() < 7:
    st.warning("Minimum 7 days of data required for prediction.")
    st.stop()

# Take last 7 days
last_7_days = df.tail(7)

weekly_total = last_7_days["quantity"].sum()

st.write(f"Last 7 Days Total Sales: {weekly_total}")

weather = st.selectbox("Next Week Weather", ["Sunny", "Rainy", "Cloudy"])
exams = st.selectbox("Next Week Exams", ["None", "Midterms", "Finals"])
region = st.selectbox("Region", ["Urban", "Rural"])

mapping_weather = {"Sunny": 0, "Rainy": 1, "Cloudy": 2}
mapping_exams = {"None": 0, "Midterms": 1, "Finals": 2}
mapping_region = {"Urban": 0, "Rural": 1}

if st.button("Predict Next Week Demand"):

    features = np.array([[
        mapping_weather[weather],
        mapping_exams[exams],
        mapping_region[region]
    ]])

    prediction = model.predict(features)[0]

    st.success(f"Suggested Inventory Level for Next Week: {prediction}")

    if prediction == "HIGH":
        st.info("📈 Increase procurement by 20%")
    elif prediction == "MEDIUM":
        st.info("📦 Maintain normal stock")
    else:
        st.info("📉 Reduce stock to prevent wastage")

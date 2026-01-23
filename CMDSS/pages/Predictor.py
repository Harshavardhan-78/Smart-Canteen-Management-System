import streamlit as st
import pickle
from pathlib import Path
from utils.processor import (
    encode_inputs,
    generate_historical_insights,
    recommend_tomorrow_menu
)
from utils.db_handler import fetch_sales_data

st.title("🤖 Demand Predictor")

@st.cache_resource
def load_model():
    # Get absolute path to project root
    BASE_DIR = Path(__file__).resolve().parent.parent
    MODEL_PATH = BASE_DIR / "models" / "rf_classifier.pkl"

    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model = load_model()

weather = st.selectbox("Weather", ["Sunny", "Rainy", "Cloudy"])
exams = st.selectbox("Exam Schedule", ["None", "Midterms", "Finals"])
region = st.selectbox("Region", ["Urban", "Rural"])

if st.button("Predict & Recommend"):
    features = encode_inputs(weather, exams, region)
    prediction = model.predict([features])[0]

    st.success(f"📦 Suggested Inventory Level: {prediction}")

    df = fetch_sales_data(st.session_state["owner_id"])

    st.subheader("📌 Insights from History")
    for i in generate_historical_insights(df)[:4]:
        st.info(i)

    st.subheader("🍽 Tomorrow’s Menu Recommendation")
    for item in recommend_tomorrow_menu(df, weather, exams):
        st.success(f"✔ Prepare more {item}")

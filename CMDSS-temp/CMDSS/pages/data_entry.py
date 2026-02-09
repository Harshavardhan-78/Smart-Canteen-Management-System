import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db_handler import get_db

st.title("📥 Data Management")

if "owner_id" not in st.session_state:
    st.error("Please login first")
    st.stop()

db = get_db()

mode = st.radio(
    "Select Data Entry Mode",
    ["📂 Upload Historical CSV", "📝 Daily Journal Entry"]
)

# =====================================
# MODE 1 — CSV UPLOAD
# =====================================
if mode == "📂 Upload Historical CSV":

    st.subheader("Upload Historical Sales Data (CSV)")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        required_columns = [
            "item", "quantity", "weather",
            "exams", "region", "time_slot", "date"
        ]

        if not all(col in df.columns for col in required_columns):
            st.error("CSV format incorrect. Missing required columns.")
            st.stop()

        df["owner_id"] = st.session_state["owner_id"]
        df["date"] = pd.to_datetime(df["date"])

        if st.button("Upload to Database"):

            records = df.to_dict("records")
            db.sales.insert_many(records)

            st.success("Historical data uploaded successfully!")
            st.write(f"{len(records)} records inserted.")


# =====================================
# MODE 2 — DAILY JOURNAL ENTRY
# =====================================
else:

    st.subheader("Enter Daily Sales Journal")

    with st.form("daily_entry_form"):

        item = st.text_input("Item Name")
        quantity = st.number_input("Quantity Sold", min_value=0)
        weather = st.selectbox("Weather", ["Sunny", "Rainy", "Cloudy"])
        exams = st.selectbox("Exam Schedule", ["None", "Midterms", "Finals"])
        region = st.selectbox("Region", ["Urban", "Rural"])
        time_slot = st.selectbox(
            "Time Slot",
            ["Morning", "Afternoon", "Evening", "Night"]
        )
        date = st.date_input("Date", value=datetime.today())

        submit = st.form_submit_button("Save Daily Entry")

        if submit:

            db.sales.insert_one({
                "owner_id": st.session_state["owner_id"],
                "item": item,
                "quantity": int(quantity),
                "weather": weather,
                "exams": exams,
                "region": region,
                "time_slot": time_slot,
                "date": datetime.combine(date, datetime.min.time())
            })

            st.success("Daily journal entry saved!")

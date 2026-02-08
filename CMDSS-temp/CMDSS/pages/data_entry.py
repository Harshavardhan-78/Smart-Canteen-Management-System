import streamlit as st
from datetime import datetime, timedelta
from utils.db_handler import get_db

st.title("📥 Weekly Sales Data Entry")

if "owner_id" not in st.session_state:
    st.error("Please login first")
    st.stop()

db = get_db()

# Initialize session storage
if "weekly_items" not in st.session_state:
    st.session_state.weekly_items = []

st.subheader("Step 1: Select Week Start Date")
start_date = st.date_input("Week Start Date")

st.subheader("Step 2: Enter Item Data")

with st.form("item_form"):

    item_name = st.text_input("Item Name")

    weekly_data = []

    for i in range(7):
        st.markdown(f"### Day {i+1}")
        weather = st.selectbox(
            f"Weather Day {i+1}",
            ["Sunny", "Rainy", "Cloudy"],
            key=f"weather_{i}"
        )
        exams = st.selectbox(
            f"Exams Day {i+1}",
            ["None", "Midterms", "Finals"],
            key=f"exams_{i}"
        )
        quantity = st.number_input(
            f"Quantity Day {i+1}",
            min_value=0,
            key=f"qty_{i}"
        )

        weekly_data.append({
            "weather": weather,
            "exams": exams,
            "quantity": quantity
        })
        time_slot = st.selectbox(f"Time Slot Day {i+1}",["Morning", "Afternoon", "Evening"],key=f"time_{i}")


    add_item = st.form_submit_button("Add Item to Week")

    if add_item:
        st.session_state.weekly_items.append({
            "item_name": item_name,
            "weekly_data": weekly_data
        })
        st.success(f"{item_name} added for this week!")

# Show added items
if st.session_state.weekly_items:
    st.subheader("Items Added This Week")
    for item in st.session_state.weekly_items:
        st.write("•", item["item_name"])

# Final Submit
if st.button("✅ End Week Entry & Save to Database"):

    for item in st.session_state.weekly_items:
        for i in range(7):
            db.sales.insert_one({
                "owner_id": st.session_state["owner_id"],
                "item": item["item_name"],
                "quantity": int(item["weekly_data"][i]["quantity"]),
                "weather": item["weekly_data"][i]["weather"],
                "exams": item["weekly_data"][i]["exams"],
                "region": "Urban",  # You can make this dynamic
                "date": datetime.combine(
                    start_date + timedelta(days=i),
                    datetime.min.time()
                ),
                "time_slot":time_slot
            })

    st.success("🎉 Weekly data saved successfully!")

    # Clear session storage
    st.session_state.weekly_items = []

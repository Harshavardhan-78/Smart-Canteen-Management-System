import streamlit as st
import pandas as pd
from pymongo import MongoClient

@st.cache_resource
def get_db():
    client = MongoClient(st.secrets["MONGO_URI"])
    return client[st.secrets["DB_NAME"]]

db = get_db()

def verify_owner(username, password):
    user = db.users.find_one({"username": username})
    return user and user["password"] == password

def fetch_sales_data(owner_id):
    data = list(db.sales.find({"owner_id": owner_id}, {"_id": 0}))
    return pd.DataFrame(data)

def save_sales_record(owner_id, record):
    record["owner_id"] = owner_id
    db.sales.insert_one(record)

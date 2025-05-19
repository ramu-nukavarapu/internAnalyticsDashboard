import streamlit as st
from data import fetch_data
from script import display_data

API_TOKEN = st.secrets["API_TOKEN"]
API_URL = st.secrets["API_URL"]

HEADERS = {
    "accept": "application/json",
    "xc-token": API_TOKEN
}

# Streamlit App
st.set_page_config(page_title="Intern Registrations Dashboard", layout="wide")
st.title("🎓 Intern Registrations Dashboard")

with st.spinner("Fetching data from database..."):
    data = fetch_data(API_URL, HEADERS)

# ✅ Button to clear the cache and refresh data
if st.button("🔄 Refresh"):
    fetch_data.clear()  # This clears the cached result

if data:
    display_data(data)
else:
    st.warning("No data found from the API.")

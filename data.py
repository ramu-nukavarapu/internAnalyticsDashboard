import requests
import streamlit as st

# Fetch data from NocoDB
@st.cache_data(show_spinner=False)
def fetch_data(url, headers):
    try:
        offset = 0
        total_data = []

        while True:
            response = requests.get(
                url,
                headers=headers,
                params={
                    "limit": 1000,
                    "offset": offset,
                    "fields": "Full Name,Affiliation (College/Company/Organization Name),Id,Age,Gender"
                }
            )
            response.raise_for_status()
            data = response.json().get("list", [])
            total_data.extend(data)
            offset += 1000
            if len(data) < 1000:
                break

        return total_data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []
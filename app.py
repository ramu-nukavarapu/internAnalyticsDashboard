import streamlit as st
from data import fetch_data
from script import display_data

API_TOKEN = st.secrets["API_TOKEN"]
API_URL = st.secrets["API_URL"]
LEAD_URL = st.secrets["LEAD_URL"]

HEADERS = {
    "accept": "application/json",
    "xc-token": API_TOKEN
}

# Streamlit App
st.set_page_config(page_title="Intern Registrations Dashboard", layout="wide")
st.title("🎓 Intern Registrations Dashboard")

# Custom CSS to center and highlight the text
st.markdown(
    """
    <div style='display: flex; justify-content: center; align-items: center; background-color: #B8CFCE; padding: 20px; border-radius: 10px;'>
        <h2 style='color: black;'>🌟 This site is deprecated. Refer the official site here - <a href="https://soai-2025.streamlit.app/">soai-2025 intern analytics</a>! 🌟</h2>
    </div>
    """,
    unsafe_allow_html=True
)


# Session state setup
if "intern_type" not in st.session_state:
    st.session_state.intern_type = None
if "data" not in st.session_state:
    st.session_state.data = None

# Buttons for intern types
col1, col2 = st.columns(2)
with col1:
    if st.button("🤖 AI Developer Intern"):
        st.session_state.intern_type = "ai"
        # with st.spinner("Fetching AI Developer Intern data..."):
            # st.session_state.data = fetch_data(API_URL, HEADERS)

with col2:
    if st.button("🧑‍💻 Tech Lead Intern"):
        st.session_state.intern_type = "techlead"
        # with st.spinner("Fetching Tech Lead Intern data..."):
            # st.session_state.data = fetch_data(LEAD_URL, HEADERS)

# Refresh button
if st.button("🔄 Refresh"):
    fetch_data.clear()
    if st.session_state.intern_type:
        with st.spinner("Refreshing data..."):
            if st.session_state.intern_type == "techlead":
                st.session_state.data = fetch_data(LEAD_URL, HEADERS)
            else:
                st.session_state.data = fetch_data(API_URL, HEADERS)

# Display data if loaded
if st.session_state.data is not None:
    display_data(st.session_state.data)
else:
    st.info("Please select an intern type to load data.")

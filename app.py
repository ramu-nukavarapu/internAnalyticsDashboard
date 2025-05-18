import streamlit as st
import pandas as pd
import altair as alt
from data import fetch_data

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

if not data:
    st.warning("No data found from the API.")
else:
    df = pd.DataFrame(data)

    # Rename columns for easier access
    df.rename(columns={
        'Affiliation (College/Company/Organization Name)': 'CollegeName',
        'Full Name': 'FullName',
        'Id': 'StudentID'
    }, inplace=True)

    # Clean and type-cast
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Gender'] = df['Gender'].str.strip().str.title()
    df['CollegeName'] = df['CollegeName'].str.strip()

    st.header("📊 College Wise Registrations")

    college_data = df.groupby('CollegeName')['StudentID'].count().reset_index()
    college_data.rename(columns={'StudentID': 'TotalRegistrations'}, inplace=True)

    total_registrations = college_data['TotalRegistrations'].sum()
    total_colleges = college_data['CollegeName'].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total Registrations", f"{total_registrations:,}")
    col2.metric("Number of Colleges", f"{total_colleges}")

    st.subheader("🏆 Registrations by College")
    top_n = st.slider("Select number of top colleges", min_value=5, max_value=50, value=10)
    top_df = college_data.sort_values(by="TotalRegistrations", ascending=False).head(top_n)

    top_df_display = top_df.reset_index(drop=True)
    top_df_display.index = top_df_display.index + 1
    st.dataframe(top_df_display, use_container_width=True)

    st.subheader("📈 Bar Chart - Top Colleges")
    chart = alt.Chart(top_df).mark_bar().encode(
        x=alt.X('TotalRegistrations:Q', title='Registrations'),
        y=alt.Y('CollegeName:N', sort='-x', title='College Name'),
        tooltip=['CollegeName', 'TotalRegistrations']
    )
    st.altair_chart(chart, use_container_width=True)

    # Age Analysis
    st.header("🎂 Registrations by Age")
    age_df = df.dropna(subset=['Age'])
    bins = [15, 18, 21, 24, 27, 30, float('inf')]
    labels = ['15-18', '19-21', '22-24', '25-27', '28-30', '30-above']
    age_df['AgeGroup'] = pd.cut(age_df['Age'], bins=bins, labels=labels, right=False)

    age_group_data = age_df.groupby('AgeGroup', observed=False)['StudentID'].count().reset_index()
    age_group_data.rename(columns={'StudentID': 'TotalStudents'}, inplace=True)

    st.dataframe(age_group_data, use_container_width=True)

    age_chart = alt.Chart(age_group_data).mark_bar().encode(
        x=alt.X('AgeGroup:N', title='Age Group'),
        y=alt.Y('TotalStudents:Q', title='Total Students'),
        color='AgeGroup:N',
        tooltip=['AgeGroup', 'TotalStudents']
    ).properties(width=700, height=400)

    st.altair_chart(age_chart, use_container_width=True)

    # Gender Analysis
    st.header("🚻 Registrations by Gender")
    gender_data = df.groupby('Gender')['StudentID'].count().reset_index()
    gender_data.rename(columns={'StudentID': 'TotalStudents'}, inplace=True)

    st.dataframe(gender_data, use_container_width=True)

    gender_chart = alt.Chart(gender_data).mark_bar().encode(
        x=alt.X('Gender:N', title='Gender'),
        y=alt.Y('TotalStudents:Q', title='Total Students'),
        color='Gender:N',
        tooltip=['Gender', 'TotalStudents']
    ).properties(width=700, height=400)

    st.altair_chart(gender_chart, use_container_width=True)

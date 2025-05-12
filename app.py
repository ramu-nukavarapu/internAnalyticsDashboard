import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Intern Registrations Dashboard", layout="wide")

st.title("🎓 Intern Registrations Dashboard")

# Read the local CSV file directly
try:
    df = pd.read_csv("collegeAnalytics.csv")
    filtered_df = df.copy()

    # Display metrics
    st.header("📊 College Wise Registrations")
    total_registrations = filtered_df['TotalRegistrations'].sum()
    total_colleges = filtered_df['CollegeName'].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total Registrations", f"{total_registrations:,}")
    col2.metric("Number of Colleges", f"{total_colleges}")

    # Top N colleges
    st.subheader("🏆 Registrations by College")
    top_n = st.slider("Select number of top colleges", min_value=5, max_value=50, value=10)
    top_df = filtered_df.sort_values(by="TotalRegistrations", ascending=False).head(top_n)

    top_df_display = top_df.reset_index(drop=True)
    top_df_display.index = top_df_display.index + 1  # start index from 1
    st.dataframe(top_df_display, use_container_width=True)


    # Bar chart
    st.subheader("📈 Bar Chart - Top Colleges")
    chart = alt.Chart(top_df).mark_bar().encode(
        x=alt.X('TotalRegistrations:Q', title='Registrations'),
        y=alt.Y('CollegeName:N', sort='-x', title='College Name'),
        tooltip=['CollegeName', 'TotalRegistrations']
    )
    st.altair_chart(chart, use_container_width=True)

    st.header("🎂 Registrations by Age")

    # Load age analytics CSV
    age_df = pd.read_csv("ageAnalytics.csv")  # Columns: Age, TotalStudents

    # Convert Age to numeric and clean invalid rows
    age_df['Age'] = pd.to_numeric(age_df['Age'], errors='coerce')
    age_df = age_df.dropna(subset=['Age'])

    # Define updated bins and labels including 30-above
    bins = [15, 18, 21, 24, 27, 30, float('inf')]
    labels = ['15-18', '19-21', '22-24', '25-27', '28-30', '30-above']
    age_df['AgeGroup'] = pd.cut(age_df['Age'], bins=bins, labels=labels, right=False)

    # Group by AgeGroup
    age_group_data = age_df.groupby('AgeGroup')['TotalStudents'].sum().reset_index()

    # Display as table
    age_group_table = age_group_data.sort_values(by="TotalStudents", ascending=False).reset_index(drop=True)
    age_group_table.index = age_group_table.index + 1
    st.dataframe(age_group_table, use_container_width=True)

    # Bar chart
    age_chart = alt.Chart(age_group_data).mark_bar().encode(
        x=alt.X('AgeGroup:N', title='Age Group'),
        y=alt.Y('TotalStudents:Q', title='Total Students'),
        color='AgeGroup:N',
        tooltip=['AgeGroup', 'TotalStudents']
    ).properties(width=700, height=400)

    st.altair_chart(age_chart, use_container_width=True)

    st.header("🚻 Registrations by Gender")

    # Load gender analytics CSV
    gender_df = pd.read_csv("genderAnalytics.csv")  # Columns: Gender, TotalStudents

    # Group by Gender
    gender_group_data = gender_df.groupby('Gender')['TotalStudents'].sum().reset_index()

    # Display as table
    gender_group_table = gender_group_data.sort_values(by="TotalStudents", ascending=False).reset_index(drop=True)
    gender_group_table.index = gender_group_table.index + 1
    st.dataframe(gender_group_table, use_container_width=True)

    # Bar chart
    gender_chart = alt.Chart(gender_group_data).mark_bar().encode(
        x=alt.X('Gender:N', title='Gender'),
        y=alt.Y('TotalStudents:Q', title='Total Students'),
        color='Gender:N',
        tooltip=['Gender', 'TotalStudents']
    ).properties(width=700, height=400)

    st.altair_chart(gender_chart, use_container_width=True)

except FileNotFoundError:
    st.error("CSV file not found. Make sure 'college_data.csv' is in the same folder as this app.")

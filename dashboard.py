import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(page_title="College Info Dashboard", layout="wide")
st.title("College Information Dashboard")
alt.themes.enable("dark")


df = pd.read_csv("colleges.csv")


df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace('\u00a0', '', regex=True)
df.columns = df.columns.str.encode('ascii', 'ignore').str.decode('ascii')


with st.sidebar:
    st.header("Filters")
    districts = sorted(df['District'].dropna().unique())
    selected_district = st.selectbox("Select District", ["ALL"] + districts)
    if selected_district != "ALL":
        df = df[df['District'] == selected_district]

    talukas = sorted(df['Taluka'].dropna().unique())
    selected_taluka = st.selectbox("Select Taluka", ["ALL"] + talukas)
    if selected_taluka != "ALL":
        df = df[df['Taluka'] == selected_taluka]

    universities = sorted(df['University Name'].dropna().unique())
    selected_university = st.selectbox("Select University", ["ALL"] + universities)
    if selected_university != "ALL":
        df = df[df['University Name'] == selected_university]


with st.container():
    col1, col2, col3 ,col4 = st.columns(4)
    col1.metric("Total Colleges", df['College Name'].nunique())
    col2.metric("Universities", df['University Name'].nunique())
    col3.metric("Talukas", df['Taluka'].nunique())
    col4.metric("Districts", df['District'].nunique())


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### College Type Distribution")
        type_data = df['College Type'].value_counts().reset_index()
        type_data.columns = ['College Type', 'Count']
        chart1 = alt.Chart(type_data).mark_bar(color='teal').encode(
            x=alt.X('College Type', sort='-y'),
            y='Count',
            tooltip=['College Type', 'Count']
        ).properties(height=250)
        st.altair_chart(chart1, use_container_width=True)

    with col2:
        st.markdown("#### Urban vs Rural")
        area_data = df['College Types'].value_counts().reset_index()
        area_data.columns = ['College Types', 'Count']
        chart2 = alt.Chart(area_data).mark_bar(color='orange').encode(
            x=alt.X('College Types', sort='-y'),
            y='Count',
            tooltip=['College Types', 'Count']
        ).properties(height=250)
        st.altair_chart(chart2, use_container_width=True)


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Women's Colleges Distribution")
        women_data = df['Exclusively in Womens Colleges'].value_counts().reset_index()
        women_data.columns = ['Exclusively for Women', 'Count']
        chart4 = alt.Chart(women_data).mark_arc(innerRadius=50).encode(
            theta='Count',
            color='Exclusively for Women',
            tooltip=['Exclusively for Women', 'Count']
        ).properties(height=300)
        st.altair_chart(chart4, use_container_width=True)

    with col2:
        st.markdown("#### Top 10 Universities by Colleges")
        top_uni = df['University Name'].value_counts().nlargest(10).reset_index()
        top_uni.columns = ['University Name', 'College Count']
        chart3 = alt.Chart(top_uni).mark_bar(color='purple').encode(
            x=alt.X('University Name', sort='-y'),
            y='College Count',
            tooltip=['University Name', 'College Count']
        ).properties(height=300)
        st.altair_chart(chart3, use_container_width=True)


if selected_university != "ALL":
    st.markdown(f"### Colleges under **{selected_university}**")
    st.dataframe(df[['College Name', 'College Type', 'College Types',
                     'Exclusively in Womens Colleges', 'Email', 'Mobile', 'Principal Name']],
                 use_container_width=True)

    

    



    

    


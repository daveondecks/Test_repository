import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import time

# Set the layout to wide
st.set_page_config(layout="wide")

st.title("Dave's First Streamlit Page")
st.write("Welcome to my simple Streamlit app - with sidebar & expander form!")

# Add a sidebar
st.sidebar.title("Sidebar")
st.sidebar.write("This is the sidebar.")
sidebar_option = st.sidebar.selectbox("Choose a sidebar option", ["Sidebar Option 1", "Sidebar Option 2", "Sidebar Option 3"])
sidebar_slider = st.sidebar.slider("Sidebar Slider", min_value=0, max_value=50)

# Add image upload in the sidebar
uploaded_image = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)
    st.balloons()  # Show balloons when an image is uploaded

if st.button("Click me"):
    st.write("Button clicked!")

# Add a line chart
st.header("Random Data Line Chart")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

# Add a map
st.header("Map")
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)
st.map(map_data)

# Add a file downloader
st.header("File Downloader")
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(chart_data)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)

# Add a progress bar
st.header("Progress Bar")
progress_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.1)
    progress_bar.progress(percent_complete + 1)

# Add a form
with st.form(key='my_form'):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Enter your name 😊")
        email = st.text_input("Enter your email 📧")
        gender = st.radio("Select your gender 🚻", ["Male", "Female", "Other"])
    with col2:
        age = st.number_input("Enter your age 🎂", min_value=0, max_value=120)
        occupation = st.text_input("Enter your occupation 💼")
        country = st.selectbox("Select your country 🌍", ["Country 1", "Country 2", "Country 3"])
    
    with st.expander("Additional Information ℹ️"):
        address = st.text_area("Enter your address 🏠")
        phone = st.text_input("Enter your phone number 📞")
        date_of_birth = st.date_input("Enter your date of birth 📅")
        options = st.selectbox("Choose an option 🔽", ["Option 1", "Option 2", "Option 3"])
        checkboxes = st.multiselect("Select multiple options ✅", ["Option A", "Option B", "Option C"])
        slider_value = st.slider("Select a value 🎚️", min_value=0, max_value=100)
    
    submit_button = st.form_submit_button(label='Submit 📨')

if submit_button:
    st.write(f"Name: {name}")
    st.write(f"Email: {email}")
    st.write(f"Gender: {gender}")
    st.write(f"Age: {age}")
    st.write(f"Occupation: {occupation}")
    st.write(f"Country: {country}")
    st.write(f"Address: {address}")
    st.write(f"Phone: {phone}")
    st.write(f"Date of Birth: {date_of_birth}")
    st.write(f"Selected Option: {options}")
    st.write(f"Selected Multiple Options: {checkboxes}")
    st.write(f"Slider Value: {slider_value}")
    st.write(f"Sidebar Option: {sidebar_option}")
    st.write(f"Sidebar Slider Value: {sidebar_slider}")

# Add a data table with sorting and filtering
st.header("Sortable and Filterable Data Table")

# Sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [24, 30, 22, 35, 29],
    'Occupation': ['Engineer', 'Doctor', 'Artist', 'Engineer', 'Doctor'],
    'Country': ['USA', 'Canada', 'UK', 'Australia', 'USA']
}
df = pd.DataFrame(data)

# Display the data table
st.dataframe(df)

# Add filters
name_filter = st.text_input("Filter by name")
age_filter = st.slider("Filter by age", min_value=0, max_value=100, value=(0, 100))
occupation_filter = st.multiselect("Filter by occupation", options=df['Occupation'].unique())
country_filter = st.multiselect("Filter by country", options=df['Country'].unique())

# Apply filters
filtered_df = df[
    (df['Name'].str.contains(name_filter, case=False)) &
    (df['Age'].between(age_filter[0], age_filter[1])) &
    (df['Occupation'].isin(occupation_filter) if occupation_filter else True) &
    (df['Country'].isin(country_filter) if country_filter else True)
]

# Display the filtered data table
st.dataframe(filtered_df)

# Display summary of the filtered data
st.write("Summary of Filtered Data")
st.write(f"Total Rows: {len(filtered_df)}")
st.write(f"Average Age: {filtered_df['Age'].mean() if not filtered_df.empty else 'N/A'}")
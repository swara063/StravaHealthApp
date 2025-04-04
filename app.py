
python
Copy
Edit
import streamlit as st
import requests

# Function to fetch Strava data from the backend
def fetch_strava_data_from_backend(access_token):
    url = f"http://localhost:5000/fetch-data?access_token={access_token}"
    response = requests.get(url)
    return response.json()

# Streamlit Interface
st.title("Strava Health Integration")

# Step 1: Input Access Token
access_token = st.text_input("Enter your Strava Access Token:")

if access_token:
    st.session_state['access_token'] = access_token
    st.success("Access token saved successfully!")

# Step 2: Fetch and display data
if 'access_token' in st.session_state:
    if st.button("Fetch Strava Data"):
        data = fetch_strava_data_from_backend(st.session_state['access_token'])
        if 'error' in data:
            st.error(data['error'])
        else:
            st.subheader("Activity Data:")
            st.write(f"Distance: {data['distance']} km")
            st.write(f"Heart Rate: {data['heart_rate']}")
            st.write(f"Calories Burned: {data['calories_burned']} kcal")

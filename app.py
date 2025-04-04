import streamlit as st
import requests
import os

# Function to fetch Strava data from the backend
def fetch_strava_data_from_backend(access_token):
    url = f"{os.getenv('BACKEND_URL')}/fetch-data?access_token={access_token}"
    response = requests.get(url)
    return response.json()

# Streamlit Interface
st.title("Strava Health Integration")

# Display login button
if st.button("Login with Strava"):
    st.write("Redirecting to Strava for authentication...")
    # This will trigger the backend to handle Strava OAuth flow
    st.query_params = {"url": f"{os.getenv('BACKEND_URL')}/login"}


# If access token exists in session, allow fetching of data
if 'access_token' in st.session_state:
    st.success("Access token saved successfully!")

    # Fetch and display Strava data
    if st.button("Fetch Strava Data"):
        data = fetch_strava_data_from_backend(st.session_state['access_token'])
        if 'error' in data:
            st.error(data['error'])
        else:
            st.subheader("Activity Data:")
            st.write(f"Distance: {data['distance']} km")
            st.write(f"Heart Rate: {data['heart_rate']}")
            st.write(f"Calories Burned: {data['calories_burned']} kcal")

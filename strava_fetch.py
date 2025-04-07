import requests
import streamlit as st

def fetch_strava_data(access_token):
    st.write(f"Using access token: {access_token}")

    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        st.write("Fetched activities:", data)
        return data
    except Exception as e:
        st.error(f"Error fetching activities: {e}")
        return None


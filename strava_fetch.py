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
        st.write("✅ Data fetched successfully")
        st.json(data)
    except Exception as e:
        st.write(f"❌ Error fetching Strava data: {e}")
        data = None

    return data


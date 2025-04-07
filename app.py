import streamlit as st
import requests
import os
import time

# Environment variable for backend URL
BACKEND_URL = os.getenv('BACKEND_URL', 'https://stravahealthapp-production.up.railway.app')

st.title("🚴‍♂️ Strava Health Integration")

# Step 1: Check for access token in URL query params and save to session
query_params = st.query_params
if 'access_token' in query_params:
    st.session_state['access_token'] = query_params['access_token'][0]
    st.success("✅ Access token received!")

    # Clean URL to prevent infinite loop
    js = """
    <script>
        const newUrl = window.location.origin + window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
    </script>
    """
    st.components.v1.html(js)

    # Optional: trigger rerun to continue flow automatically
    st.experimental_rerun()

# Step 2: If no token, show login button
if 'access_token' not in st.session_state:
    if st.button("Login with Strava 🚴‍♀️"):
        auth_url = f"{BACKEND_URL}/login"
        js = f"window.location.href = '{auth_url}';"  # Redirect in same tab
        st.components.v1.html(f"<script>{js}</script>")

else:
    st.success("🎉 You are logged in!")

    # Auto-fetch data immediately when access_token exists
    with st.spinner("Fetching your Strava data..."):
        try:
            url = f"{BACKEND_URL}/fetch-data?access_token={st.session_state['access_token']}"
            response = requests.get(url, timeout=10)
            data = response.json()
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
            st.stop()

        # Progress bar (faster)
        progress = st.progress(0)
        for percent_complete in range(0, 101, 10):
            time.sleep(0.05)
            progress.progress(percent_complete)
        progress.empty()

        # Display data
        if 'error' in data:
            st.error(data['error'])
        else:
            st.subheader("🏃 Your Activity Data:")
            st.write(f"🏞️ Distance: {data.get('distance', 0)} km")
            st.write(f"🔥 Total Energy: {data.get('energy', 0)} kJ")
            st.write(f"🕒 Moving Time: {data.get('moving_time', 0)} seconds")
            st.write(f"💓 Average Heart Rate: {data.get('average_heartrate', 'N/A')} bpm")

            st.success("🚴 Data fetched successfully!")


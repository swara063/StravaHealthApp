import streamlit as st
import requests
import os
import time

# Environment variable for backend URL
BACKEND_URL = os.getenv('BACKEND_URL')

st.title("🚴‍♂️ Strava Health Integration")

# Check for access token in URL query params and save to session
query_params = st.experimental_get_query_params()
if 'access_token' in query_params:
    st.session_state['access_token'] = query_params['access_token'][0]
    st.success("Access token received successfully!")

# Login button
if 'access_token' not in st.session_state:
    if st.button("Login with Strava"):
        st.write("Redirecting to Strava for authentication...")
        auth_url = f"{BACKEND_URL}/login"
        js = f"window.open('{auth_url}')"  # Open in new tab
        st.components.v1.html(f"<script>{js}</script>")
else:
    st.success("You are logged in!")

    if st.button("Fetch Strava Data"):
        with st.spinner("Fetching your Strava data..."):
            try:
                url = f"{BACKEND_URL}/fetch-data?access_token={st.session_state['access_token']}"
                response = requests.get(url, timeout=10)
                data = response.json()
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")
                st.stop()

            # Progress bar
            progress = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress.progress(percent_complete + 1)
            progress.empty()

            # Display data
            if 'error' in data:
                st.error(data['error'])
            else:
                st.subheader("Activity Data:")
                st.write(f"🏃 Distance: {data.get('distance', 0)} km")
                st.write(f"❤️ Heart Rate: {data.get('heart_rate', 'N/A')}")
                st.write(f"🔥 Calories Burned: {data.get('calories_burned', 'N/A')} kcal")


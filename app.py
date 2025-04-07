import streamlit as st
import requests
import os
import time

# Backend URL
BACKEND_URL = os.getenv('BACKEND_URL', 'https://stravahealthapp-production.up.railway.app')

st.set_page_config(page_title="Strava Health App", page_icon="🚴‍♂️", layout="centered")
st.title("🚴‍♂️ Strava Health Integration")
st.markdown("Get insights from your latest Strava activity!")

# Step 1: Handle access token in URL params
query_params = st.query_params
if 'access_token' in query_params:
    st.session_state['access_token'] = query_params['access_token'][0]
    st.session_state['refresh_token'] = query_params.get('refresh_token', [''])[0]
    st.session_state['expires_at'] = int(query_params.get('expires_at', ['0'])[0])

    st.success("✅ Access token received!")

    # Clean URL to avoid reload loops
    js = """
    <script>
        const newUrl = window.location.origin + window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
        window.location.reload();
    </script>
    """
    st.components.v1.html(js)

# Step 2: If no token, show login button
if 'access_token' not in st.session_state:
    st.info("🔑 Please login to connect your Strava account.")
    if st.button("Login with Strava 🚴‍♀️"):
        auth_url = f"{BACKEND_URL}/login"
        js = f"window.open('{auth_url}', '_blank', 'width=800,height=800');"
        st.components.v1.html(f"<script>{js}</script>")
else:
    st.success("🎉 You are logged in!")

    # Step 3: Auto-fetch data
    with st.spinner("Fetching your latest Strava activity..."):
        try:
            response = requests.get(f"{BACKEND_URL}/fetch-data", params={"access_token": st.session_state['access_token']}, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                st.error(f"⚠️ Error: {data['error']}")
            else:
                st.subheader("📊 Your Activity Summary:")

                distance_km = data['distance']
                heart_rate = data['heart_rate']
                calories = data['calories_burned']

                # Distance
                st.markdown("**Total Distance (km):**")
                st.progress(min(int(distance_km), 100) / 100)

                st.metric(label="Distance Covered", value=f"{distance_km:.2f} km")

                # Heart Rate
                if heart_rate != "N/A":
                    st.markdown("**Average Heart Rate (bpm):**")
                    st.progress(min(int(heart_rate), 200) / 200)
                    st.metric(label="Avg Heart Rate", value=f"{heart_rate} bpm")
                else:
                    st.warning("💓 Heart rate data not available.")

                # Calories
                if calories != "N/A":
                    st.markdown("**Calories Burned:**")
                    st.progress(min(int(calories), 1000) / 1000)
                    st.metric(label="Calories", value=f"{calories} kcal")
                else:
                    st.warning("🔥 Calories data not available.")

        except Exception as e:
            st.error(f"🚨 Failed to fetch data: {e}")

    # Optional: Refresh data button
    if st.button("🔄 Refresh Data"):
        st.experimental_rerun()


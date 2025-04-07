import streamlit as st
import requests
import os

# Backend URL of your Flask app
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
        window.location.reload();
    </script>
    """
    st.components.v1.html(js)

# Step 2: If no token, show login button
if 'access_token' not in st.session_state:
    if st.button("Login with Strava 🚴‍♀️"):
        auth_url = f"{BACKEND_URL}/login"
        js = f"window.location.href = '{auth_url}';"
        st.components.v1.html(f"<script>{js}</script>")
else:
    st.success("🎉 You are logged in!")

    # Fetch Strava data function
    def fetch_strava_data(access_token):
        st.write(f"🔑 Using access token: {access_token}")

        url = "https://www.strava.com/api/v3/athlete/activities"
        headers = {'Authorization': f'Bearer {access_token}'}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            st.write(f"🌐 Strava response: {response.status_code} - {response.text}")

            response.raise_for_status()

            activities = response.json()

            if not activities:
                return {'error': 'No activities found'}

            latest_activity = activities[0]

            return {
                'distance': latest_activity.get('distance', 0) / 1000,  # meters to km
                'heart_rate': latest_activity.get('average_heartrate', 'N/A'),
                'calories_burned': latest_activity.get('kilojoules', 'N/A')
            }

        except requests.RequestException as e:
            st.error(f"❌ Error fetching Strava data: {e}")
            return {'error': str(e)}

    # Auto-fetch data immediately
    with st.spinner("Fetching your Strava data..."):
        data = fetch_strava_data(st.session_state['access_token'])

        if 'error' in data:
            st.error(data['error'])
        else:
            st.subheader("🏃 Latest Activity Data")
            st.write(f"**Distance:** {data['distance']} km")
            st.write(f"**Average Heart Rate:** {data['heart_rate']} bpm")
            st.write(f"**Calories Burned:** {data['calories_burned']} kJ")


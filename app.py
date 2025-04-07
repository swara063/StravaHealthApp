import streamlit as st
import requests
import os
import time
from datetime import datetime, timedelta

# Env variable for backend URL
BACKEND_URL = os.getenv('BACKEND_URL', 'https://stravahealthapp-production.up.railway.app')

st.set_page_config(page_title="Strava Health Dashboard 🚴‍♂️", layout="wide")

# --- STYLES ---
st.markdown("""
    <style>
        .big-font { font-size:30px !important; font-weight: bold; }
        .small-font { font-size:14px; color: grey; }
        .metric-style { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
        .css-18e3th9 { padding-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚴‍♂️ Strava Health Integration")

# --- HANDLE QUERY PARAMS ---
query_params = st.query_params

if 'access_token' in query_params:
    st.session_state['access_token'] = query_params['access_token'][0]
    st.success("✅ Access token received!")

    # Clean URL
    js = """
    <script>
        const newUrl = window.location.origin + window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
        window.location.reload();
    </script>
    """
    st.components.v1.html(js)

# --- TOKEN CHECK ---
if 'access_token' not in st.session_state:
    st.warning("🔒 Please log in to access your Strava data.")
    if st.button("Login with Strava 🚴‍♀️"):
        auth_url = f"{BACKEND_URL}/login"
        js = f"window.open('{auth_url}', '_blank', 'width=800,height=800');"
        st.components.v1.html(f"<script>{js}</script>")
    st.stop()


# --- AUTO REFRESH EVERY 15 MINUTES ---
if 'token_acquired_time' not in st.session_state:
    st.session_state['token_acquired_time'] = datetime.now()

# Check if 15 minutes have passed
if datetime.now() - st.session_state['token_acquired_time'] > timedelta(minutes=15):
    st.warning("🔄 Token expired, please log in again.")
    if st.button("Re-login with Strava 🚴‍♀️"):
        auth_url = f"{BACKEND_URL}/login"
        js = f"window.open('{auth_url}', '_blank', 'width=800,height=800');"
        st.components.v1.html(f"<script>{js}</script>")
    st.stop()


# --- FETCH USER DATA ---
st.success("🎉 You are logged in!")

with st.spinner("Fetching your Strava data..."):
    try:
        response = requests.get(f"{BACKEND_URL}/fetch-data", params={'access_token': st.session_state['access_token']})
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        st.stop()

# --- DISPLAY DATA ---

if not data or 'activities' not in data or len(data['activities']) == 0:
    st.warning("No activities found. Try logging another ride!")
    st.stop()

activities = data['activities']
profile = data.get('profile', {})

# Profile section
st.subheader("🏅 Athlete Profile")
cols = st.columns(3)

cols[0].metric("Name", profile.get('firstname', '') + " " + profile.get('lastname', ''))
cols[1].metric("City", profile.get('city', 'Unknown'))
cols[2].metric("Followers", profile.get('follower_count', 0))

st.image(profile.get('profile', ''), width=100)

st.markdown("---")

# Latest activity
latest = activities[0]
st.subheader("🚴 Latest Activity")
st.markdown(f"**{latest.get('name', 'No name')}** on {latest.get('start_date_local', '')}")

cols = st.columns(4)
cols[0].metric("Distance (km)", round(latest.get('distance', 0) / 1000, 2))
cols[1].metric("Time (min)", round(latest.get('moving_time', 0) / 60, 2))
cols[2].metric("Speed (km/h)", round(latest.get('average_speed', 0) * 3.6, 2))
cols[3].metric("Elevation (m)", latest.get('total_elevation_gain', 0))

# Progress bar for total distance this week
total_distance = sum([act.get('distance', 0) for act in activities]) / 1000  # in km
goal = 100  # Example goal

st.markdown("### 🎯 Weekly Goal Progress")
progress = min(total_distance / goal, 1.0)
st.progress(progress)
st.markdown(f"**{total_distance:.2f} km** out of **{goal} km**")

# Activities table
st.markdown("### 📋 Recent Activities")
activity_data = [{
    "Name": act.get('name'),
    "Distance (km)": round(act.get('distance', 0) / 1000, 2),
    "Time (min)": round(act.get('moving_time', 0) / 60, 2),
    "Speed (km/h)": round(act.get('average_speed', 0) * 3.6, 2),
    "Date": act.get('start_date_local', '')
} for act in activities[:10]]

st.dataframe(activity_data)

st.markdown("---")
st.caption("Built with ❤️ for Strava athletes.")



